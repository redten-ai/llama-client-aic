#!/usr/bin/env python3

"""

submit a reviewed, expert answer
and confidence score per llm
ai result

## Examples

```bash
./examples/review-answer.py -i ID -s SCORE -a ANSWER
```

```bash
echo "reviewing ai result for job: 201"
./examples/review-answer.py \
    -i 201 \
    -s 99.9 \
    -a "subject matter expert review here"
echo "getting updated ai result for job: 201"
/examples/get-ai-result.py -i 201
```

## Debugging

increase logging by
exporting this env variable before starting

```bash
export LOG=debug
```

"""

import os
import logging
import argparse
import client_aic.authenticate as auth
import client_aic.req.ai.get_ai_result as get_ai_result
import client_aic.req.ai.update_ai_result as update_ai_result


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


def submit_expert_answer():
    """
    submit_expert_answer

    submit a reviewed, expert answer
    and a confidence score per llm
    ai result

    ## Examples

    ```bash
    ./examples/review-answer.py -i ID -a ANSWER -s SCORE
    ```

    """
    score = None
    answer = None
    job_id = None

    email = None
    password = None

    parser = argparse.ArgumentParser(
        description=("get ai result from db by the job id")
    )
    parser.add_argument(
        "-e",
        "--email",
        help=(
            "user email "
            "and defaults to the AI_EMAIL env variable"
        ),
        dest="email",
    )
    parser.add_argument(
        "-i",
        "--id",
        help=(
            "matching " "account.ai_result.job_id " "value"
        ),
        required=True,
        dest="job_id",
    )
    parser.add_argument(
        "-p",
        "--password",
        help=(
            "user password "
            "and defaults to the AI_PASSWORD env variable"
        ),
        dest="password",
    )
    parser.add_argument(
        "-a",
        "--answer",
        help=(
            "expert's answer - "
            "just a heads up "
            "please escape double quotes "
            "and all special characters or "
            "the update will fail due to the command "
            "line limitations on parsing single/double "
            "quote(s)"
            ""
        ),
        required=True,
        dest="answer",
    )
    parser.add_argument(
        "-s",
        "--score",
        help=(
            "expert's confidence in how strong the "
            "answer is with supported values between "
            "0-100.00 "
            "where "
            "score < 65 is not confident, and "
            "65 <= score < 80 is confident and "
            "80 <= score < 95 is very confident and "
            "score >= 95 is for known facts "
            ""
        ),
        required=True,
        dest="score",
    )
    args = parser.parse_args()

    if args.email:
        email = args.email
    if args.answer:
        answer = args.answer
    if args.password:
        password = args.password
    if args.job_id:
        job_id = int(args.job_id)
    if args.score:
        try:
            org_score = float(f"{args.score}")
            # limiting resolution per answer
            score = float(f"{org_score:.8f}")
        except Exception:
            log.error(
                f"please set the score={args.score} "
                "between 0.00 and 100.00"
            )
            return
    if score < 0.00:
        log.error("please set a score above 0.00")
        return
    if score > 100.00:
        log.error("please set a score below 100.00")
        return

    log.debug(
        f"submitting expert review for result={job_id} "
        f"score={score} "
        f"answer={answer}"
    )

    user = auth.authenticate(
        email=email,
        password=password,
    )
    if not user:
        log.error(f"failed to login as user: {email}")
        return
    # end of auth/login

    ai_result = None

    if job_id:
        if job_id < 1:
            log.error(
                "please use a positive integer "
                f"job_id={job_id} value"
            )
            return
        log.debug(
            f"getting account.ai_result where job.id = {job_id}"
        )
        not_done = True
        while not_done:
            not_done = False
            # should be the same as the job_id too
            ai_result = get_ai_result.get_ai_result(
                id=job_id, user=user
            )
            if not ai_result:
                log.error(
                    "failed getting ai result: "
                    f"job_id={job_id}"
                )
                return
            log.debug(
                "submitting expert reviews for "
                f"ai result id={ai_result.id} "
                f"answer={ai_result.answer} "
                f"job_id={job_id}"
            )
            ai_result.reviewed_answer = answer
            ai_result.reviewed_score = score
            updated_res = update_ai_result.update_ai_result(
                user=user,
                ai_result=ai_result,
            )
            if not ai_result:
                log.error(
                    "failed getting ai result: "
                    f"job_id={job_id}"
                )
                return
            log.info(
                "updated ai result for "
                f"job_id={job_id}\n"
                "llm     answer: "
                f"{updated_res.answer}\n"
                "review  answer: "
                f"{updated_res.reviewed_answer}\n"
            )
            if os.getenv("LOG", "info") == "debug":
                updated_res.show()


if __name__ == "__main__":
    submit_expert_answer()
