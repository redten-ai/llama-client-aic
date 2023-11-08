import logging
import requests
import ujson as json
import client_aic.get_cfg as get_cfg
import client_aic.models.core_user as core_user
import client_aic.models.core_result_ai as core_result_ai
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def create_ai_result(
    user: core_user.CoreUser,
    data: dict,
    cfg: dict = None,
):
    """
    create_ai_result

    provides an api for remote llm(s)
    to stream results over https
    without being co-located with the
    llm(s)

    e.g. run synthetic dataset generative
    jobs on the cloud (aws, gcp, azure, runpod.io
    and stream the results to your self-hosted rest api)

    :param CoreUser user: authenticated user
        that is making this request
    :param data: dictionary from
        ``data=CoreResultAI.get_dict()``
    :param cfg: optional **CoreConfig**
        dictionary

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
    log.debug(f"create ai result: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    data.pop("id", None)
    r = s.post(
        url,
        json=data,
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
        if debug:
            log.debug(
                f"create ai result success - {r.text}"
            )
        try:
            rec_dict = json.loads(r.text)
            cur_o = core_result_ai.CoreResultAI()
            cur_o.load_response_dict(rec_dict=rec_dict)
            return cur_o
        except Exception as e:
            log.error(
                f'failed to create ai result with ex="{e}"'
            )
    return None
