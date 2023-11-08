### How do I ask the LLM questions?

#### Getting Started

##### Install

Please install the python 3 pip:

```bash
pip install llama-client-aic
```

##### Environment Variables

The following environment variables are used to automatically create a new user (or service account) using the RLHF REST API:

```bash
export AI_USER=username
export AI_EMAIL=email@email.com
export AI_PASSWORD=abcdef123
export AI_COLLECTION_ID=embed-security
```

#### Ask a Question from the Command Line

```bash
ask-llm.py \
    -c "${AI_COLLECTION_ID}" \
    -q "question"
```

#### Ask a Question from a File using the Command Line

```bash
ask-llm.py \
    -c "${AI_COLLECTION_ID}" \
    -q PATH_TO_FILE_WITH_QUESTION
```

#### Ask a Question using the Python REST Client

```python
import client_aic.ask as ask
# if your user does not exist it will be created
username = "username"
email = "email@email.com"
password = "your_password"
collection_id = "embed-security"
wait_for_result = True
# ask the llm the question and let the
# llm use the collection_id embeddings to perform rag
# before responding
(
    user,
    res_job,
    res_ai) = ask.ask(
        question=question,
        collection_id=collection_id,
        username=username,
        email=email,
        password=password,
        wait_for_result=wait_for_result)
if not user:
    print(
        f'failed to find user with email={email}')
    return
if not res_job:
    print('failed to find job result')
    return
if wait_for_result:
    if res_ai:
        print(
            f'{email} - job_id={res_job.id} result:\n'
            f'question: {question}\n'
            f'answer: {res_ai.answer}\n'
            f'score: {res_ai.score}')
    else:
        print(
            'failed to get ai result for '
            f'job_id={res_job.id}')
else:
    print(
        f'did not wait for job={res_job.id} result')
```
