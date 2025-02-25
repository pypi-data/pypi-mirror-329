import json
import re
import warnings
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

import paperqa
from aviary.utils import MultipleChoiceQuestion
from paperqa.settings import AgentSettings as PQAAgentSettings
from paperqa.settings import ParsingSettings, Settings
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    ValidationInfo,
    computed_field,
    field_validator,
    validator,
)


def _extract_doi(citation: str) -> str | None:
    doi = re.findall(r"10\.\d{4}/\S+", citation, re.IGNORECASE)
    return doi[-1] if doi else None


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: str | None = None


class Doc(paperqa.Doc):
    doi: str | None = None

    @validator("doi", pre=True)
    def citation_to_doi(cls, v: str | None, values: dict) -> str | None:  # noqa: N805
        if v is None and "citation" in values:
            return _extract_doi(values["citation"])
        return v


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: list[Doc]
    doc_count: int
    writeable: bool = False


# COPIED FROM paperqa-server!
class ParsingOptions(StrEnum):
    S2ORC = "s2orc"
    PAPERQA_DEFAULT = "paperqa_default"
    GROBID = "grobid"


class ChunkingOptions(StrEnum):
    SIMPLE_OVERLAP = "simple_overlap"
    SECTIONS = "sections"


class AgentStatus(StrEnum):
    # INITIALIZED - the agent has started, but no answer is present
    INITIALIZED = "initialized"
    # IN_PROGRESS - the agent has provided an incomplete answer, still processing to the final result
    IN_PROGRESS = "in progress"
    # FAIL - no answer could be generated
    FAIL = "fail"
    # SUCCESS - answer was generated
    SUCCESS = "success"
    # TRUNCATED - agent didn't finish naturally (e.g. timeout, too many actions),
    # so we prematurely answered
    TRUNCATED = "truncated"
    # UNSURE - the agent was unsure, but an answer is present
    UNSURE = "unsure"


class AgentSettings(PQAAgentSettings):
    """Configuration for the agent."""

    model_config = ConfigDict(extra="allow")

    agent_type: str = Field(
        default="ldp.agent.SimpleAgent",
        description="Type of agent to use",
    )

    search_min_year: int | None = None
    search_max_year: int | None = None
    papers_from_evidence_citations_config: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Optional keyword argument configuration for the"
            " PapersFromEvidenceCitations tool. If None, the tool's default parameters"
            " will be used."
        ),
    )
    websockets_to_gcs_config: dict[str, str | bool] | None = Field(
        default=None,
        description=(
            "Optional configuration upload websockets data as JSON ('gcs_prefix' string"
            " is required, 'use_compression' boolean defaults to False), or leave field as"
            " default of None to not upload websockets data."
        ),
    )

    @field_validator("websockets_to_gcs_config", mode="before")
    @classmethod
    def validate_websockets_to_gcs_config(
        cls, v: dict[str, str | bool] | str | None
    ) -> dict[str, str | bool] | None:
        # If None, move on
        if not v:
            return None

        # If given as a string, load the JSON
        # let json decode error be raised naturally
        v_dict = json.loads(v) if isinstance(v, str) else v

        # gcs_prefix is required & value must be string
        if "gcs_prefix" not in v_dict or not isinstance(v_dict["gcs_prefix"], str):
            raise ValueError("gcs_prefix is required and must be a string.")
        # use_compression is not required & value must be boolean
        if "use_compression" in v_dict and not isinstance(
            v_dict["use_compression"], bool
        ):
            raise ValueError(
                f"use_compression must be a boolean, input {v_dict['use_compression']}."
            )
        return v_dict


class ParsingConfiguration(ParsingSettings):
    ordered_parser_preferences: list[ParsingOptions] = [  # noqa: RUF012
        ParsingOptions.S2ORC,
        ParsingOptions.PAPERQA_DEFAULT,
    ]
    chunking_algorithm: ChunkingOptions = ChunkingOptions.SIMPLE_OVERLAP  # type: ignore[assignment]
    gcs_parsing_prefix: str = "parsings"
    gcs_raw_prefix: str = "raw_files"
    use_human_readable_clinical_trials: bool = Field(
        default=True,
        description="Parse clinical trial JSONs into human readable text",
    )


class ServerSettings(BaseModel):
    group: str | None = None


class QuerySettings(Settings):
    parsing: ParsingConfiguration = Field(default_factory=ParsingConfiguration)  # type: ignore[mutable-override]
    agent: AgentSettings = Field(default_factory=AgentSettings)  # type: ignore[mutable-override]
    named_template: str | None = None


class QueryRequestMinimal(BaseModel):
    """A subset of the fields in the QueryRequest model."""

    query: str = Field(description="The query to be answered")
    group: str | None = Field(None, description="A way to group queries together")
    named_template: str | None = Field(
        None,
        description="The template to be applied (if any) to the query for settings things like models, chunksize, etc.",
    )


class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str | MultipleChoiceQuestion = Field(
        description=(
            "The query to be answered. Set to a multiple choice question when grading"
            " (e.g. for training)."
        ),
    )
    id: UUID = Field(
        default_factory=uuid4,
        description="Identifier which will be propagated to the Answer object.",
    )
    settings_template: str | None = None
    settings: QuerySettings = Field(
        default_factory=QuerySettings, validate_default=True
    )
    # provides post-hoc linkage of request to a docs object
    # NOTE: this isn't a unique field, on the user to keep straight
    _docs_name: str | None = PrivateAttr(default=None)

    @field_validator("settings")
    @classmethod
    def apply_settings_template(
        cls, v: QuerySettings, info: ValidationInfo
    ) -> Settings:
        if info.data["settings_template"] and isinstance(v, Settings):
            base_settings = QuerySettings.from_name(info.data["settings_template"])
            return QuerySettings(**(base_settings.model_dump() | v.model_dump()))
        return v

    @computed_field  # type: ignore[prop-decorator]
    @property
    def docs_name(self) -> str | None:
        return self._docs_name

    def set_docs_name(self, docs_name: str) -> None:
        """Set the internal docs name for tracking."""
        self._docs_name = docs_name

    group: str | None = Field(None, description="A way to group queries together")
    server: ServerSettings = Field(default_factory=ServerSettings)
    named_template: str | None = Field(
        default=None,
        description="If set, the prompt will be initialized by fetching "
        "the named query request template from the server.",
    )


class UserModel(BaseModel):
    email: str
    full_name: str
    disabled: bool = False
    verified: bool = False
    roles: str = Field(
        default="user",
        description="roles delimied with ':', valid roles include 'user', 'admin', and 'api'.",
    )


class ScrapeStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKLIST = "blocklist"
    IN_PROGRESS = "none"
    DUPLICATE = "duplicate"
    PARSED = "parsed"
    PENDING = "pending"


class PaperDetails(BaseModel):
    """A subset of the fields in the PaperDetails model."""

    citation: str | None = None
    year: int | None = None
    url: str | None = Field(
        default=None,
        description=(
            "Optional URL to the paper, which can lead to a Semantic Scholar page,"
            " arXiv abstract, etc. As of version 0.67 on 5/10/2024, we don't use this"
            " URL anywhere in the source code."
        ),
    )
    title: str | None = None
    doi: str | None = None
    paperId: str | None = None  # noqa: N815
    other: dict[str, Any] = Field(
        default_factory=dict,
        description="Other metadata besides the above standardized fields.",
    )

    def __getitem__(self, item: str):
        """Allow for dictionary-like access, falling back on other."""
        try:
            return getattr(self, item)
        except AttributeError:
            return self.other[item]


def maybe_upgrade_legacy_query_request(request: dict[Any, Any]) -> QueryRequest:
    if "settings" not in request:
        return convert_legacy_query_request(request)

    # allow  extras
    class Permissible(QueryRequest):
        model_config = ConfigDict(extra="allow")

    return Permissible.model_validate(request)


def convert_legacy_query_request(  # noqa: C901, PLR0915, PLR0912
    legacy_request: dict[str, Any],
) -> QueryRequest:
    # Extract basic fields
    query = legacy_request.get("query", "")
    group = legacy_request.get("group")
    named_template = legacy_request.get("named_template")
    query_id = legacy_request.get("id", uuid4())

    settings = QuerySettings()

    # Map LLM fields
    settings.llm = legacy_request.get("llm", settings.llm)
    settings.summary_llm = legacy_request.get("summary_llm", settings.summary_llm)
    settings.temperature = legacy_request.get("temperature", settings.temperature)
    settings.embedding = legacy_request.get("embedding", settings.embedding)
    settings.texts_index_mmr_lambda = legacy_request.get(
        "texts_index_mmr_lambda", settings.texts_index_mmr_lambda
    )

    # Map agent settings
    if agent_llm := legacy_request.get("agent_llm"):
        settings.agent.agent_llm = agent_llm

    if agent_tools := legacy_request.get("agent_tools"):
        if agent_tool_names := agent_tools.get("agent_tool_names"):
            settings.agent.tool_names = agent_tool_names
        if agent_system_prompt := agent_tools.get("agent_system_prompt"):
            settings.agent.agent_system_prompt = agent_system_prompt
        if agent_prompt := agent_tools.get("agent_prompt"):
            settings.agent.agent_prompt = agent_prompt
        if search_count := agent_tools.get("search_count"):
            settings.agent.search_count = search_count
        if wipe_context_on_answer_failure := agent_tools.get(
            "wipe_context_on_answer_failure"
        ):
            settings.agent.wipe_context_on_answer_failure = (
                wipe_context_on_answer_failure
            )
        if timeout := agent_tools.get("timeout"):
            settings.agent.timeout = timeout
        if should_pre_search := agent_tools.get("should_pre_search"):
            settings.agent.should_pre_search = should_pre_search
        if websockets_to_gcs_config := agent_tools.get("websockets_to_gcs_config"):
            settings.agent.websockets_to_gcs_config = websockets_to_gcs_config
        if search_max_year := agent_tools.get("search_max_year"):
            settings.agent.search_max_year = search_max_year
        if search_min_year := agent_tools.get("search_min_year"):
            settings.agent.search_min_year = search_min_year

    # Map answer settings
    if length := legacy_request.get("length"):
        settings.answer.answer_length = length

    if consider_sources := legacy_request.get("consider_sources"):
        settings.answer.evidence_k = consider_sources

    if summary_length := legacy_request.get("summary_length"):
        settings.answer.evidence_summary_length = summary_length

    if max_sources := legacy_request.get("max_sources"):
        settings.answer.answer_max_sources = max_sources

    if (
        filter_extra_background := legacy_request.get("filter_extra_background")
    ) is not None:
        settings.answer.answer_filter_extra_background = filter_extra_background

    if max_concurrent := legacy_request.get("max_concurrent"):
        settings.answer.max_concurrent_requests = max_concurrent

    # Map parsing settings
    if parsing_config := legacy_request.get("parsing_configuration"):
        if chunk_size := parsing_config.get("chunksize"):
            settings.parsing.chunk_size = chunk_size
        if overlap := parsing_config.get("overlap"):
            settings.parsing.overlap = overlap
        if chunking_algorithm := parsing_config.get("chunking_algorithm"):
            settings.parsing.chunking_algorithm = ChunkingOptions(chunking_algorithm)
        if ordered_parsing_preferences := parsing_config.get(
            "ordered_parsing_preferences"
        ):
            settings.parsing.ordered_parser_preferences = ordered_parsing_preferences
        if gcs_parsing_prefix := parsing_config.get("gcs_parsing_prefix"):
            settings.parsing.gcs_parsing_prefix = gcs_parsing_prefix
        if gcs_raw_prefix := parsing_config.get("gcs_raw_prefix"):
            settings.parsing.gcs_raw_prefix = gcs_raw_prefix

    # Map prompts
    if prompts := legacy_request.get("prompts"):
        if summary := prompts.get("summary"):
            settings.prompts.summary = summary
        if qa := prompts.get("qa"):
            settings.prompts.qa = qa
        if select := prompts.get("select"):
            settings.prompts.select = select
        if pre := prompts.get("pre"):
            settings.prompts.pre = pre
        if post := prompts.get("post"):
            settings.prompts.post = post
        if system := prompts.get("system"):
            settings.prompts.system = system
        if summary_json := prompts.get("summary_json"):
            settings.prompts.summary_json = summary_json
        if summary_json_system := prompts.get("summary_json_system"):
            settings.prompts.summary_json_system = summary_json_system
        if json_summary := prompts.get("json_summary"):
            settings.prompts.use_json = json_summary
        if skip_summary := prompts.get("skip_summary"):
            settings.answer.evidence_skip_summary = skip_summary

    # Map server settings
    server_settings = ServerSettings()
    if group:
        server_settings.group = group

    return QueryRequest(
        query=query,
        group=group,
        named_template=named_template,
        id=query_id,
        settings=settings,
        server=server_settings,
    )


def handle_legacy_query(
    query: dict[str, Any],
) -> QueryRequest:
    with warnings.catch_warnings():
        warnings.filterwarnings("always", category=DeprecationWarning)
        warnings.warn(
            "Using legacy query format is deprecated and support  "
            "will be removed in version 8. Please reference the "
            "updated QueryRequest object to update.",
            DeprecationWarning,
            stacklevel=2,
        )
        return maybe_upgrade_legacy_query_request(query)
