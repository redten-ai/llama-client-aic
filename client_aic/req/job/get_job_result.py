import logging
import ujson as json
import requests
import client_aic.get_cfg as get_cfg
import client_aic.models.core_result_job as core_result_job
import client_aic.models.core_user as core_user
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def get_job_result(
    id: int,
    user: core_user.CoreUser,
    cfg: dict = None,
):
    """
    get_job_result

    get the user's job results from the db
    by the **CoreJob.id**

    helpful for tracking job progress status.

    :param id: CoreJob.id for an existing user job
    :param CoreUser user: authenticated user
        that is making this request
    :param cfg: optional - **CoreConfig** dictionary

    :returns: **CoreResultJob** on success
        **None** on non-success
    :rtype: CoreResultJob or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/job/result/{id}'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    log.debug(f"get job result: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    data = {"user_id": user.id, "job_id": id}
    r = s.get(
        url,
        json=data,
        verify=verify,
        cert=(cert_file, key_file),
        timeout=10,
    )
    if r.status_code != 200:
        if debug:
            log.info(
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
        try:
            cur_json = json.loads(r.text)
            cur_o = core_result_job.CoreResultJob(
                id=cur_json.get("id", None),
                job_id=cur_json.get("job_id", None),
                worker_id=cur_json.get("worker_id", None),
                job_type=cur_json.get("job_type", None),
                user_id=cur_json.get("user_id", None),
                state=cur_json.get("state", None),
                data=cur_json.get("data", None),
                msg=cur_json.get("msg", None),
                created_at=cur_json.get("created_at", None),
                updated_at=cur_json.get("updated_at", None),
            )
            return cur_o
        except Exception as e:
            log.error(
                f'failed to get job_result.id={id} with ex="{e}"'
            )
    return None
