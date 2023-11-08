import logging
import requests
import ujson as json
import client_aic.get_cfg as get_cfg
import client_aic.models.core_user as core_user
import client_aic.models.core_result_ai as core_result_ai
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def get_ai_result(
    id: int,
    user: core_user.CoreUser,
    cfg: dict = None,
):
    """
    get_ai_result

    after the llm finishes processing the question,
    you can get the ai results table using this
    method

    get the ai result by the **CoreJob.id** value
    using the rest api

    :param id: look up this **CoreJob.id**'s
        ai results
    :param CoreUser user: authenticated user
        that is making this request
    :param cfg: optional **CoreConfig** dictionary

    :returns: **CoreResultAI** on success
        **None** on non-success
    :rtype: CoreResultAI or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/ai/result/{id}'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    log.debug(f"get ai result: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    data = {"user_id": user.id, "job_id": id}
    r = s.get(
        url,
        json=data,
        verify=verify,
        cert=(cert_file, key_file),
        timeout=5,
    )
    if r.status_code != 200:
        log.error(
            "\n\n"
            "non-200 response:\n"
            f"  url: {url}\n"
            f"  job_result.id: {id}\n"
            f"  ca={verify}\n"
            f"  response:\n"
            f"  code: {r.status_code}\n"
            f"  text:\n"
            f"  {r.text}\n"
        )
        return None
    else:
        if debug:
            log.info(f"get ai result success - {r.text}")
        try:
            cur_json = json.loads(r.text)
            cur_o = core_result_ai.CoreResultAI(
                id=cur_json.get("id", None),
                user_id=cur_json.get("user_id", None),
                job_id=cur_json.get("job_id", None),
                worker_id=cur_json.get("worker_id", None),
                state=cur_json.get("state", None),
                question=cur_json.get("question", None),
                answer=cur_json.get("answer", None),
                model_name=cur_json.get("model_name", None),
                score=cur_json.get("score", None),
                question_score=cur_json.get(
                    "question_score", None
                ),
                answer_score=cur_json.get(
                    "answer_score", None
                ),
                match_source=cur_json.get(
                    "match_source", None
                ),
                match_page=cur_json.get("match_page", None),
                match_content=cur_json.get(
                    "match_content", None
                ),
                summarized_question=cur_json.get(
                    "summarized_question", None
                ),
                summarized_answer=cur_json.get(
                    "summarized_answer", None
                ),
                summarized_score=cur_json.get(
                    "summarized_score", None
                ),
                reviewed_answer=cur_json.get(
                    "reviewed_answer", None
                ),
                reviewed_score=cur_json.get(
                    "reviewed_score", None
                ),
                reviewed_computed_score=cur_json.get(
                    "reviewed_computed_score",
                    None,
                ),
                reviewed_notes=cur_json.get(
                    "reviewed_notes", None
                ),
                collection=cur_json.get("collection", None),
                collection_notes=cur_json.get(
                    "collection_notes", None
                ),
                category=cur_json.get("category", None),
                tags=cur_json.get("tags", None),
                latency=cur_json.get("latency", None),
                data=cur_json.get("data", None),
                created_at=cur_json.get("created_at", None),
                updated_at=cur_json.get("updated_at", None),
            )
            return cur_o
        except Exception as e:
            log.error(
                f'failed to get ai_result.id={id} with ex="{e}"'
            )
    return None
