#!/usr/bin/env python3

"""
## Ask a Question

ask an llm a question or a question from a file
and the rest api will reply with a job_id for
tracking the progress. once the llm's finishes
processing the question then the results
are shown to stdout.

## Getting Started

The following environment variables support
setting user or service account credentials
for the llm rest api

```bash
export AI_USER=username
export AI_EMAIL=email@email.com
export AI_PASSWORD=abcdef123
export AI_COLLECTION_ID=embed-security
```

## Examples

### Ask a Question from the Command Line

```bash
./examples/ask-llm.py \
    -c "${AI_COLLECTION_ID}" \
    -q "question"
```

### Ask a Question from a File using the Command Line

```bash
./examples/ask-llm.py \
    -c "${AI_COLLECTION_ID}" \
    -q PATH_TO_FILE_WITH_QUESTION
```

### Ask a Question using the Rest Client

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

## Debugging

Increase logging by exporting this environment
variable before starting this process

```bash
export LOG=debug
```

"""

import os
import logging
import argparse
import client_aic.ask as ask


level = logging.INFO
log_level = os.getenv("LOG", "info")
if log_level == "debug":
    level = logging.DEBUG

logging.basicConfig(
    level=level,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s "
        "%(funcName)s - %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)


def ask_a_question():
    """
    ask_a_question

    ask a question using the rest api

    """

    collection_id = os.getenv(
        "AI_COLLECTION_ID", "embed-security"
    )

    email = None
    password = None
    wait_for_result = True
    question = None

    parser = argparse.ArgumentParser(
        description=(
            "ask a question and " "wait for the response"
        )
    )
    parser.add_argument(
        "-c",
        "--collection-id",
        help=(
            "string - embedding collection id alias "
            f"and defaults to the {collection_id}"
        ),
        dest="collection_id",
    )
    parser.add_argument(
        "-e",
        "--email",
        help=(
            "string - user email "
            "and defaults to the AI_EMAIL env variable"
        ),
        dest="email",
    )
    parser.add_argument(
        "-n",
        "--no-wait-for-job",
        help=(
            "flag - do not wait for the job to finish "
            "- wait is enabled by default"
        ),
        action="store_true",
        dest="no_wait_for_job",
    )
    parser.add_argument(
        "-p",
        "--password",
        help=(
            "string - user password "
            "and defaults to the AI_PASSWORD env variable"
        ),
        dest="password",
    )
    parser.add_argument(
        "-q",
        "--question",
        help=(
            "string - question or a path to a file containing the "
            "question(s) to ask the llm"
        ),
        required=True,
        dest="question",
    )
    args = parser.parse_args()

    if args.email:
        email = args.email
    if args.password:
        password = args.password
    if args.collection_id:
        collection_id = args.collection_id
    if args.question:
        question = str(args.question)
    if args.no_wait_for_job:
        wait_for_result = False
    if not question or len(question) == 0:
        log.error(
            "missing question - "
            "please use "
            "-q QUESTION "
            "or "
            "-q PATH_TO_Q_FILE"
        )
        return
    q_split = question.split(" ")
    if len(q_split) == 1:
        q_file = q_split[0]
        if os.path.exists(q_file):
            log.debug("reading q_file={q_file}")
            with open(q_file, "r") as fp:
                question = fp.read().lstrip().strip()
        if not question or len(question) == 0:
            log.error(
                f"empty question file: {q_file} - stopping"
            )
            return
    if email:
        log.debug(
            f"{email} asking question={question} "
            f"rag data source collection_id={collection_id} "
            f"wait={wait_for_result}"
        )
    else:
        log.debug(
            f"asking question={question} "
            f"rag data source collection_id={collection_id} "
            f"wait={wait_for_result}"
        )
    # ask the llm the question and let the
    # llm use the collection_id embeddings to perform rag
    # before responding
    (user, res_job, res_ai) = ask.ask(
        question=question,
        collection_id=collection_id,
        email=email,
        password=password,
        wait_for_result=wait_for_result,
    )
    if not user:
        log.error(f"failed to find user with email={email}")
        return
    if not res_job:
        log.error("failed to find job result")
        return
    if wait_for_result:
        if res_ai:
            log.info(
                f"{user.email}.id={user.id} "
                f"result:\n"
                f"question: {question}\n"
                f"answer: {res_ai.answer}\n"
                f"score: {res_ai.score}\n"
                f"job_id: {res_job.job_id}\n"
            )
        else:
            log.error(
                "failed to get ai result for "
                f"job_id={res_job.job_id}"
            )
    else:
        log.info(
            f"please wait for job_id {res_job.job_id} "
            "to finish processing"
        )


if __name__ == "__main__":
    ask_a_question()
