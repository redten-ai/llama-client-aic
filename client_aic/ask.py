import os
import time
import logging
import client_aic.get_cfg as get_cfg
import client_aic.authenticate as auth
import client_aic.req.ai.run_job_ask as run_job_ask
import client_aic.req.ai.get_ai_result as get_ai_result
import client_aic.req.job.get_job_result as get_job_result
import client_aic.models.core_result_job as core_result_job
import client_aic.ppj as ppj


log = logging.getLogger(__name__)


def ask(
    question: str,
    collection_id: str,
    email: str = None,
    password: str = None,
    username: str = None,
    job_params: dict = None,
    cfg_core: dict = None,
    wait_for_result: bool = True,
    wait_interval: float = 2.0,
):
    """
    ask

    use the reinforcement learning with human
    feedback and rag rest api to ask the
    underlying llm a question
    and wait for the results

    :param question: question to ask the llm
    :param collection_id: embedding alias name
        to use for the rag source data
    :param email: optional - user email for the rest api
    :param password: optional - user password for the rest api
    :param username: optional - username for the rest api
    :param job_params: optional - llm question
        properties and attributes
    :param cfg_core: optional - **CoreConfig** dictionary
    :param wait_for_result: optional flag -
        with default set to **True**.
        When **True** this function will wait for the
        **CoreResultAI** before returning.
        When **False** this function
        will start the llm job and then return a **None**
        for the **CoreResultAI** in the
        returned tuple (**CoreResultJob**, None). please
        use the CoreJob.id to periodically check if the
        job is done.
    :param wait_interval: float - optional - how
        many seconds to wait before trying to get the
        **CoreResultAI** record from the rest api

    :returns: on success (**CoreUser**, **CoreResultAI**,
        **CoreResultAI**) versus non-success can return
        (**None**, **None**, **None**)
    :rtype: (CoreUser, CoreResultAI, CoreResultAI)
    """
    res_job = None
    res_ai = None
    user = None
    debug = os.getenv("LLM_DEBUG", "0") == "1"
    cfg = cfg_core
    if not cfg_core:
        cfg = get_cfg.get_cfg()
    cfg_user = cfg.get("user", {})
    if not username:
        username = os.getenv(
            "AI_USERNAME", cfg_user.get("u", None)
        )
    if not password:
        password = os.getenv(
            "AI_PASSWORD", cfg_user.get("p", None)
        )
    if not email:
        email = os.getenv(
            "AI_EMAIL", cfg_user.get("e", None)
        )
    missing_env_vars = []
    if not question or len(question) < 4:
        log.error(
            "please ask a question more than 4 characters"
        )
        return (user, res_job, res_ai)
    if not email:
        missing_env_vars.append("AI_EMAIL")
    if not password:
        missing_env_vars.append("AI_PASSWORD")
    if len(missing_env_vars) > 0:
        missing_str = ", ".join(missing_env_vars)
        log.error(
            "please set these environment variables "
            f"and retry: {missing_str}"
        )
        return (user, res_job, res_ai)
    # name of a pgvector embedding db
    # database connection dict
    user = auth.authenticate(
        username=username,
        email=email,
        password=password,
        cfg=cfg,
    )
    if not user:
        log.error(f"failed to login as user: {username}")
        return (user, res_job, res_ai)
    log.info(
        f"user={username} asking='{question}' "
        f"embedding collection_id={collection_id} "
        "please be patient while the llm responds "
        "there could be a lot of users on the system "
        "at this time"
    )
    create_job_res = run_job_ask.run_job_ask(
        question=question,
        user=user,
        collection_id=collection_id,
        cfg=cfg,
    )
    if not create_job_res:
        log.error("failed to start job ")
        return (user, res_job, res_ai)
    job_id = int(create_job_res.id)
    if wait_for_result:
        log.debug(
            f"waiting for job_id={job_id} "
            f"to finish sleeping {wait_interval}s "
            "per retry"
        )
    else:
        log.debug(f"not waiting for job_id={job_id}")
        res_job = core_result_job.CoreResultJob(
            job_id=job_id,
            user_id=user.id,
            state=create_job_res.state,
        )
        return (user, res_job, res_ai)

    if job_id:
        if job_id < 1:
            log.error(
                "please use a positive integer "
                f"job_id={job_id} value"
            )
            return (user, res_job, res_ai)
        log.debug(
            "getting account.ai_result where "
            f"job.id = {job_id}"
        )
        not_done = True
        while not_done:
            res_job = get_job_result.get_job_result(
                id=job_id, user=user, cfg=cfg
            )
            if not res_job:
                if wait_for_result:
                    log.debug(
                        f"waiting job_id={job_id} "
                        f"{wait_interval}s"
                    )
                    time.sleep(wait_interval)
                    continue
                else:
                    log.error(
                        f"did not find the job_id={job_id}"
                    )
                    return (user, res_job, res_ai)
            # get by the new result's parent job id
            # that should be the same as job_id
            res_ai = get_ai_result.get_ai_result(
                id=res_job.job_id,
                user=user,
                cfg=cfg,
            )
            if not res_ai:
                log.error(
                    "failed getting ai result: "
                    f"job_id={res_job.id}"
                )
                return (user, res_job, res_ai)
            if debug:
                log.debug(
                    f"got ai result id={res_ai.id} "
                    f"answer={res_ai.answer} "
                    f"job_id={res_job.job_id}"
                    f"job_result_id={res_job.id}"
                    f"answer: {res_ai.answer}"
                )
            not_done = False
        # end of while
    else:
        log.error("no job_id detected on command line")

    if not res_ai:
        log.error(
            "failed getting ai result: " f"job_id={job_id}"
        )
        return (user, res_job, res_ai)
    if user and res_job and res_ai:
        if debug:
            log.debug(
                f"user={user.id} job_id={res_job.id} "
                f"has ai results:\n{ppj.ppj(res_ai.get_dict())}"
            )
        else:
            log.debug(
                f"answer for user={user.id} job_id={res_job.id} "
                f"ai_result_id={res_ai.id}"
            )
    else:
        log.error(
            f"user={user.id} ask hit unexpected return case "
            "\n"
            f"res_job={res_job}\n"
            f"res_ai={res_ai}\n"
        )
    return (user, res_job, res_ai)


"""
# useful for testing
if __name__ == '__main__':
    collection_id = "embed-security"
    question = (
        "using std::namespace;\n"
        "int main() {\n"
        "std::cout << \"hello\" << std::endl;\n"
        "return 256;\n}"
        "\n"
        "")
    log.info(
        f"asking llm to answer='{question}' "
        f'using rag collection_id={collection_id}')
    (user, res_job, res_ai) = ask(
        question=question,
        collection_id=collection_id)
    if res_ai:
        log.info(
            f'got ai result: {res_ai}')
        res_ai.show()
"""
