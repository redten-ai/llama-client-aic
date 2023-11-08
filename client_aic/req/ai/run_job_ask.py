import logging
import uuid
import ujson as json
import requests
import client_aic.ppj as ppj
import client_aic.get_cfg as get_cfg
import client_aic.tls.utils as tls_utils
import client_aic.models.core_job as core_job
import client_aic.models.core_user as core_user


log = logging.getLogger(__name__)


def run_job_ask(
    question: str,
    user: core_user.CoreUser,
    cfg: dict = None,
    session_id: str = None,
    derived_session_id: str = None,
    model_name: str = None,
    collection_id: str = None,
    collection_name: str = None,
    embed_model_name: str = None,
    tags: str = None,
    max_tokens: int = 512,
    n_ctx: int = 2048,
    n_batch: int = 10,
    match_docs: int = 3,
    max_doc_scores: int = 3,
    min_q_score: float = 0.3,
    min_a_score: float = 0.3,
):
    """
    run_job_ask

    ask the llm a question and get a **CoreJob**
    for tracking the progress

    Run a generative ai job

    Supports

    - question-answering (qa)
    - synthetic dataset generation
    - prompt template
    - user session tracking and historical context
    - reinforcement learning with human feedback
    - custom embedding models to use (hugging face supported)
    - custom rag embedding collection name or id to search
    - llm model parameter customization

    :param question: question to ask the llm
    :param user: authenticated user
        that is making this request
    :param cfg: optional **CoreConfig** dictionary
    :param session_id: user session id from
        tracking historical context
    :param derived_session_id: optional - sub
        tracking id for more granular historical context
    :param model_name: llm model name
    :param collection_id: search this
        rag collection id before asking the llm
    :param collection_name: search this
        rag collection name before asking the llm
    :param embed_model_name: name of the embedding
        model for this job
    :param tags: comma-delimited tags for this
        question
    :param max_tokens: supported max tokens
        on this request
    :param n_ctx: supported max context
        on this request (usually the llm is hardcoded
        to a specific context and you do not usually
        change this)
    :param n_batch: number of batches for
        this question
    :param match_docs: how many matching documents
        from the rag data source collection id/names
        are allowed before proceeding to the llm
    :param max_doc_scores: how many document score
        are required for this request
    :param min_q_score: minimum rag data source
        confidence score as a valid source for the llm
        to use with this question
    :param min_a_score: minimum rag data source
        confidence score as a valid source for the llm
        to use with this answer

    :returns: **CoreJob** on success
        **None** on non-success
    :rtype: CoreJob or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/job'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    log.debug(f'run job ask: {url} question="{question}"')
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})

    use_model_name = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    use_embed_name = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    use_tags = None
    use_session_id = None
    use_derived_session_id = None
    if model_name:
        use_model_name = model_name
    if embed_model_name:
        use_embed_name = embed_model_name
    if tags:
        use_tags = tags
    if session_id:
        use_session_id = session_id
    else:
        session_id = str(uuid.uuid4()).replace("-", "")
    if derived_session_id:
        use_derived_session_id = derived_session_id

    # src/requests/job/create_job.rs
    use_req = {
        "user_id": user.id,
        # ask worker id = 1
        # gen worker id = 2
        "worker_id": 1,
        # ready for work when state == 1
        "state": 1,
        # ask questions = 1
        # gen answers = 2
        "job_type": 1,
        "ask": {
            "msg": question,
            "model_name": use_model_name,
            "embed_model_name": use_embed_name,
            "collection_id": collection_id,
            "collection_name": collection_name,
            "max_tokens": max_tokens,
            "n_ctx": n_ctx,
            "n_batch": n_batch,
            "rag": {
                "dirs": [],
                "s3": [],
                "caches": [],
                "rss": [],
                "match_docs": match_docs,
                "max_doc_scores": max_doc_scores,
                "min_q_score": min_q_score,
                "min_a_score": min_a_score,
            },
            "data": {},
            "tags": use_tags,
            "session_id": use_session_id,
            "derived_session_id": use_derived_session_id,
        },
    }
    log.debug(
        "starting ai job with config:"
        f"\n{ppj.ppj(use_req)}\n"
    )
    use_json = json.dumps(use_req)
    r = s.post(
        url,
        use_json,
        verify=verify,
        cert=(cert_file, key_file),
        timeout=5,
    )
    if r.status_code != 201:
        log.error(
            "\n\n"
            "non-201 response:\n"
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
        try:
            cur_json = json.loads(r.text)
            cur_o = core_job.CoreJob(
                id=cur_json.get("id", None),
                user_id=cur_json.get("user_id", None),
                worker_id=cur_json.get("worker_id", None),
                job_type=cur_json.get("job_type", None),
                state=cur_json.get("state", None),
                status=cur_json.get("status", None),
                data=cur_json.get("data", None),
                msg=cur_json.get("msg", None),
                created_at=cur_json.get("created_at", None),
                updated_at=cur_json.get("updated_at", None),
            )
            return cur_o
        except Exception as e:
            log.error(
                f'failed to run ask job with ex="{e}"'
            )
    return None
