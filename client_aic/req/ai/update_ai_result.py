import logging
import requests
import ujson as json
import client_aic.tls.utils as tls_utils
import client_aic.get_cfg as get_cfg
import client_aic.models.core_result_ai as core_result_ai
import client_aic.models.core_user as core_user


log = logging.getLogger(__name__)


def update_ai_result(
    user: core_user.CoreUser,
    ai_result: core_result_ai.CoreResultAI,
    cfg=None,
):
    """
    update_ai_result

    update an existing ai result

    supports reinforcement learning
    using human feedback with
    the **reviewed_answer** and **reviewed_score** fields

    :param CoreUser user: authenticated user
        that is making this request
    :param ai_result: in-memory object with
        values to send to the database
    :param cfg: optional **CoreConfig** dictionary

    :returns: **CoreResultAI** on success
        **None** on non-success
    :rtype: CoreResultAI or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/ai/result'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    log.debug(f"update ai result: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    data = ai_result.get_dict()
    r = s.put(
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
            log.info(f"update ai result success - {r.text}")
        try:
            cur_json = json.loads(r.text)
            cur_o = core_result_ai.CoreResultAI()
            cur_o.load_response_dict(rec_dict=cur_json)
            return cur_o
        except Exception as e:
            log.error(
                f'failed to update ai_result with ex="{e}"'
            )
    return None
