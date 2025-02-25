import asyncio
import logging
import time
from collections.abc import Collection
from http import HTTPStatus
from typing import Any, BinaryIO, TypeAlias
from uuid import UUID

import aiohttp
import requests
import tenacity
from paperqa.types import PQASession
from pydantic import BaseModel, Field

from .models import (
    AgentStatus,
    DocsStatus,
    PaperDetails,
    QueryRequest,
    QueryRequestMinimal,
    UploadMetadata,
    UserModel,
    handle_legacy_query,
)
from .utils import get_pqa_key, get_pqa_url

logger = logging.getLogger(__name__)
PQA_URL = get_pqa_url()

AioHTTPTimeout: TypeAlias = aiohttp.ClientTimeout | aiohttp.helpers._SENTINEL


def coerce_request(
    query: str | QueryRequest | dict, named_template: str | None = None
) -> QueryRequest | QueryRequestMinimal:
    if isinstance(query, str):
        return QueryRequestMinimal(query=query, named_template=named_template)
    if isinstance(query, QueryRequest):
        return query
    if isinstance(query, dict):
        return handle_legacy_query(query)
    raise TypeError("Query must be a string or QueryRequest")


class AnswerResponse(BaseModel):
    session: PQASession = Field(alias="answer")
    usage: dict[str, list[int]]
    bibtex: dict[str, str]
    status: str
    timing_info: dict[str, dict[str, float]] | None = None
    duration: float = 0

    async def save_as_template(
        self,
        name: str,
        public: bool = False,
        timeout: AioHTTPTimeout = aiohttp.ClientTimeout(0.5 * 60),  # noqa: B008
    ) -> None:
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{PQA_URL}/api/templates/create/{name}",
                params={"query_id": str(self.session.id), "public": str(public)},
                timeout=timeout,
                headers={"Authorization": f"Bearer {get_pqa_key()}"},
            ) as response,
        ):
            response.raise_for_status()


async def get_query_request(name: str) -> QueryRequest | QueryRequestMinimal:
    with requests.Session() as session:
        response = session.get(
            f"{PQA_URL}/api/templates/view/{name}",
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return coerce_request(response.json())


def upload_file(
    bibliography: str,
    file: BinaryIO,
    metadata: UploadMetadata,
    public: bool = False,
) -> dict[str, Any]:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"

    with requests.Session() as session:
        response = session.post(
            f"{PQA_URL}/api/docs/{bibliography}/upload",
            files=[("file", file)],
            json={"metadata": metadata.model_dump()},
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return response.json()


def upload_paper(doi: str, file: BinaryIO) -> None:
    with requests.Session() as session:
        result = session.post(
            f"{PQA_URL}/db/upload/paper/",
            params={"doi": doi},
            files=[("file", file)],
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        result.raise_for_status()


def check_dois(dois: list[str]) -> dict[str, tuple[str, str]]:
    with requests.Session() as session:
        result = session.post(
            f"{PQA_URL}/db/docs/dois",
            json=dois,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        result.raise_for_status()
        return result.json()


def delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()


async def async_delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()


def get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return DocsStatus(**response.json())


async def async_get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        data = await response.json()
        return DocsStatus(**data)


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(3),
)
def agent_query(
    query: QueryRequest | str | dict,
    bibliography: str = "tmp",
    named_template: str | None = None,
    timeout: float | None = 11 * 60,
) -> AnswerResponse:
    data = coerce_request(query, named_template).model_dump(mode="json")
    response = requests.post(
        f"{PQA_URL}/api/agent/{bibliography or 'tmp'}",
        json=data,
        timeout=timeout,
        headers={"Authorization": f"Bearer {get_pqa_key()}"},
    )
    response.raise_for_status()
    return AnswerResponse(**response.json())


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(3),
)
async def async_agent_query(
    query: QueryRequest | str | dict,
    bibliography: str = "tmp",
    named_template: str | None = None,
    timeout: AioHTTPTimeout = aiohttp.ClientTimeout(11 * 60),  # noqa: B008
) -> AnswerResponse:
    data = coerce_request(query, named_template).model_dump(mode="json")
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"{PQA_URL}/api/agent/{bibliography or 'tmp'}",
            json=data,
            timeout=timeout,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return AnswerResponse(**await response.json())


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(10),
    retry=(
        tenacity.retry_if_exception_type((
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
        ))
    ),
)
def submit_agent_job(
    query: QueryRequest | str | dict,
    bibliography: str = "tmp",
    named_template: str | None = None,
    timeout: float | None = 20 * 60,
) -> dict:
    data = coerce_request(query, named_template).model_dump(mode="json")
    response = requests.post(
        f"{PQA_URL}/api/submit_agent_job/{bibliography or 'tmp'}",
        json=data,
        timeout=timeout,
        headers={"Authorization": f"Bearer {get_pqa_key()}"},
    )
    response.raise_for_status()
    return response.json()


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(10),
    retry=(
        tenacity.retry_if_exception_type((
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
        ))
    ),
)
async def async_submit_agent_job(
    query: QueryRequest | str | dict,
    bibliography: str = "tmp",
    named_template: str | None = None,
    timeout: AioHTTPTimeout = aiohttp.ClientTimeout(20 * 60),  # noqa: B008
) -> dict:
    data = coerce_request(query, named_template).model_dump(mode="json")
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"{PQA_URL}/api/submit_agent_job/{bibliography or 'tmp'}",
            json=data,
            params={
                "timeout": getattr(timeout, "total", 20 * 60),
            },
            timeout=timeout,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()


async def async_send_feedback(
    queries: list[UUID],
    feedback: list[dict],
    group: str | None = None,
    timeout: AioHTTPTimeout = aiohttp.ClientTimeout(0.5 * 60),  # noqa: B008
) -> list[UUID]:
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"{PQA_URL}/api/feedback",
            json={
                # default JSON serializer in python cannot handle UUID
                "queries": [str(q) for q in queries],
                "feedback": feedback,
                "feedback_group": group,
            },
            timeout=timeout,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return [UUID(str_uuid) for str_uuid in await response.json()]


async def async_get_feedback(
    query: UUID | None = None,
    group: str | None = None,
    timeout: AioHTTPTimeout = aiohttp.ClientTimeout(10 * 60),  # noqa: B008
) -> dict[str, Any]:
    # add as query parameters
    body = {"query": str(query), "feedback_group": group}
    if query is group is None:
        raise ValueError("At least one of query or group must be provided")
    if query is None:
        del body["query"]
    if group is None:
        del body["feedback_group"]
    url = f"{PQA_URL}/db/feedback"

    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            json=body,
            timeout=timeout,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()


async def async_add_user(
    user: UserModel,
) -> None:
    url = f"{PQA_URL}/users/admin/add"
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            url,
            json=user.model_dump(),
            timeout=aiohttp.ClientTimeout(10 * 60),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(10),
    retry=(
        tenacity.retry_if_exception_type((
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
        ))
    ),
    reraise=True,
)
async def async_get_query(query_id: str) -> dict:
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"{PQA_URL}/db/query/{query_id}",
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()


async def async_get_scrape_status(
    scrape_request_id: str | None = None,
    task_id: str | None = None,
) -> list[dict]:
    params = None
    if not task_id is scrape_request_id is None:
        params = (
            {"scrape_request_id": scrape_request_id}
            if scrape_request_id
            else {"task_id": task_id}  # type: ignore[dict-item]
        )
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"{PQA_URL}/api/scrape_status",
            params=params,
            timeout=aiohttp.ClientTimeout(15),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()


def get_scrape_status(
    scrape_request_id: str | None = None,
    task_id: str | None = None,
) -> list[dict]:
    params = None
    if not task_id is scrape_request_id is None:
        params = (
            {"scrape_request_id": scrape_request_id}
            if scrape_request_id
            else {"task_id": task_id}  # type: ignore[dict-item]
        )
    response = requests.get(
        f"{PQA_URL}/api/scrape_status",
        params=params,
        timeout=15,
        headers={"Authorization": f"Bearer {get_pqa_key()}"},
    )
    response.raise_for_status()
    return response.json()


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(10),
    retry=(
        tenacity.retry_if_exception_type((
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
        ))
    ),
)
async def async_submit_scrape_job(
    query: list[PaperDetails],
    document_type: str = "paper",
) -> list[dict]:
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"{PQA_URL}/api/submit_scrape_job",
            json=[q.model_dump() for q in query],
            params={"document_type": document_type},
            timeout=aiohttp.ClientTimeout(15),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(10),
    retry=(
        tenacity.retry_if_exception_type((
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
        ))
    ),
)
def submit_scrape_job(
    query: list[PaperDetails],
    document_type: str = "paper",
) -> list[dict]:
    response = requests.post(
        f"{PQA_URL}/api/submit_scrape_job",
        json=[q.model_dump() for q in query],
        params={"document_type": document_type},
        timeout=15,
        headers={"Authorization": f"Bearer {get_pqa_key()}"},
    )
    response.raise_for_status()
    return response.json()


CONTINUE_POLLING_STATUSES: Collection[str] = {
    AgentStatus.SUCCESS.value,
    AgentStatus.UNSURE.value,
    AgentStatus.TRUNCATED.value,
    AgentStatus.FAIL.value,
}


async def get_pqa_result_via_polling(
    request_id: str,
    verbose: bool = True,
    poll_interval: int = 30,  # seconds, how often it pings to check
    max_polls: int = 25,
) -> dict | None:
    status = AgentStatus.INITIALIZED
    tic = time.time()
    counter = 0
    while status not in CONTINUE_POLLING_STATUSES and counter < max_polls:
        try:
            query = await async_get_query(request_id)
        except aiohttp.ClientResponseError as e:
            if e.status == HTTPStatus.NOT_FOUND.value:
                query = {"question": "n/a", "response": {"status": "Waiting in queue"}}
            else:
                raise
        if verbose:
            logger.info(
                f"Elapsed: {time.time() - tic:.1f}s Query: {query['question']} - Status: {query['response']['status']}"
            )
        status = query["response"]["status"]
        if status not in CONTINUE_POLLING_STATUSES:
            await asyncio.sleep(poll_interval)
            counter += 1

    if counter >= max_polls:
        logger.error(f"Max polls reached for request {request_id}")
        return None

    return query


async def gather_pqa_results_via_polling(
    request_ids: list[str],
    verbose: bool = True,
    poll_interval: int = 30,  # seconds
    max_polls: int = 25,
) -> list[dict | None]:
    return await asyncio.gather(*[
        get_pqa_result_via_polling(request_id, verbose, poll_interval, max_polls)
        for request_id in request_ids
    ])
