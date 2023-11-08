#!/usr/bin/env python3

"""
get an ai result from the account.ai_result table
by the **ai_result.job_id** (note: user must be the
job's creator/owner)

## Example

```bash
./examples/get-ai-result.py -i JOB_ID
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
import time
import argparse
import client_aic.authenticate as auth
import client_aic.req.ai.get_ai_result as get_ai_result
import client_aic.req.job.get_job_result as get_job_result
import client_aic.req.ai.search_ai_results as search_ai_results


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


def run_get_ai_result():
    """
    run_get_ai_result
    """
    wait_for_job = False
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
        "-n",
        "--no-wait-for-job",
        help=(
            "flat - do not wait for the job to finish "
            "- wait is enabled by default"
        ),
        action="store_true",
        dest="no_wait_for_job",
    )
    args = parser.parse_args()

    if args.email:
        email = args.email
    if args.password:
        password = args.password
    if args.job_id:
        job_id = int(args.job_id)
    if args.no_wait_for_job:
        wait_for_job = False

    user = auth.authenticate(
        email=email,
        password=password,
    )
    if not user:
        log.debug(f"failed to login as user: {email}")
        return
    # end of auth/login

    sleep_interval_sec = 2.0
    job_result = None
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
        num_jobs_found = 0
        not_done = True
        while not_done:
            job_result = get_job_result.get_job_result(
                id=job_id, user=user
            )
            if not job_result:
                if wait_for_job:
                    log.debug(
                        f"waiting job_id={job_id} "
                        f"{sleep_interval_sec}s"
                    )
                    time.sleep(sleep_interval_sec)
                    continue
                else:
                    log.info(
                        f"did not find the job_id={job_id}"
                    )
                    return
            # should be the same as the job_id too
            ai_result = get_ai_result.get_ai_result(
                id=job_result.job_id,
                user=user,
            )
            if not ai_result:
                log.error(
                    "failed getting ai result: "
                    f"job_id={job_result.id}"
                )
                return
            log.debug(
                f"got ai result id={ai_result.id} "
                f"answer={ai_result.answer} "
                f"job_id={job_result.id}"
            )

            search_req = {
                "query": "by_job_id",
                "user_id": user.id,
                # should be the same as the job_id too
                "job_id": ai_result.job_id,
            }
            search_res = (
                search_ai_results.search_ai_results(
                    user=user, data=search_req
                )
            )
            if not search_res:
                log.error(
                    "failed search ai result: "
                    f"job_id={job_result.id}"
                )
                return
            log.debug(
                f"search ai result id={ai_result.id} "
                f"job_id={job_result.id}"
            )
            num_recs = len(search_res.recs)
            for idx, rec in enumerate(search_res.recs):
                found_q = None
                found_a = None
                if rec.question:
                    found_q = rec.question[0:200]
                if rec.answer:
                    found_a = rec.answer[0:200]
                num_jobs_found += 1
                log.info(
                    f"search result - "
                    f"\n-- {idx+1}/{num_recs} "
                    f"job.id={rec.job_id} "
                    f"ai_result.id={rec.id} "
                    f"user_id={rec.user_id} "
                    f"\n - question={found_q} "
                    f"\n - answer={found_a} "
                    f"\n - score={rec.score} "
                    f"\n - model={rec.model_name} "
                    f"\n - match_source={rec.match_source} "
                    f"\n - match_page={rec.match_page} "
                    f"\n - collection={rec.collection} "
                    f"\n - session_id={rec.session_id} "
                    f"\n - tags={rec.tags} "
                    f"\n - reviewed_answer={rec.reviewed_answer} "
                )
            not_done = False
        # end of while
        if num_jobs_found == 0:
            log.info(
                f"did not find job_id={job_id} "
                f"created by user_id={user.id}"
            )
        log.debug("done")
    else:
        log.info("please set the -i job_id")
    return


if __name__ == "__main__":
    run_get_ai_result()
