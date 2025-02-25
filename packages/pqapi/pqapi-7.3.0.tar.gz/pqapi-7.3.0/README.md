# paperqa-api

Python client for interacting with the PaperQA server

## Installation

Python 3.11+ is required for this package

```sh
pip install pqapi
```

## Authentication

Make sure to set the environment variable `PQA_API_KEY` to your API token:

```sh
export PQA_API_KEY=pqa-...
```

API keys generally have a rate limit associated with them that is based on queries per day. These are based on a rolling window, rather than resetting at a specific time. You will receive 429s if you have exceeded your rate limit on submission.

## Basic Usage

### Simple Synchronous Queries

The simplest way to use the API is with synchronous queries:

```python
import pqapi

response = pqapi.agent_query("Are COVID-19 vaccines effective?")

print(response.answer)
```

### Async Queries

You can also make asynchronous queries:

```python
import pqapi

response = await pqapi.async_agent_query(query)
```

These still require an open connection though, so do not accumulate too many of them. Each query takes between 1 and 5 minutes generally.

## Advanced Features

### Batch Job Processing

For running multiple long-running queries efficiently, use the job submission API:

```python
import asyncio
import pqapi

# Define multiple queries
queries = [
    'What is the elastic modulus of gold?',
    'What is the elastic modulus of silver?',
    'What is the elastic modulus of copper?'
]

# Submit jobs
jobs = [pqapi.submit_agent_job(query=q) for q in queries]

# Poll for results
results = asyncio.run(pqapi.gather_pqa_results_via_polling(
    [job['metadata']['query_id'] for job in jobs]
))
```

The results will include:

- `question`: Your original query text
- `request`: Serialized settings used in your query
- `response`: Serialized `pqapi.AnswerResponse` object

### Using Templates

You can use predefined templates that you develop and save on paperqa.app:

```python
# Single query with template
response = pqapi.agent_query(
    'The melting point of gold is 1000F.',
    named_template='check for contradiction'
)

# Batch jobs with templates
contradictions = [
    {
        'query': 'Gold can be transmuted into platinum.',
        'named_template': 'check for contradiction'
    },
]
contradiction_jobs = [pqapi.submit_agent_job(**c) for c in contradictions]
results = asyncio.run(pqapi.gather_pqa_results_via_polling(
    [job['metadata']['query_id'] for job in contradiction_jobs]
))
```

## AnswerResponse Object

The response object contains detailed information about your query:

- Sources used
- Cost information
- Other metadata

Access the main specific answer text with:

```python
print(response.answer)
```
