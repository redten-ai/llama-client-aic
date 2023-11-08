import logging
import requests
import ujson as json
import client_aic.tls.utils as tls_utils
import client_aic.get_cfg as get_cfg
import client_aic.models.core_search_result_ai as core_search_result_ai
import client_aic.models.core_user as core_user


log = logging.getLogger(__name__)


def search_ai_results(
    user: core_user.CoreUser,
    data: dict,
    cfg: dict = None,
):
    """
    search_ai_results

    Search for ai results within the database

    search for specific ai results using the
    supported parameters

    :param CoreUser user: authenticated user
        that is making this request
    :param data: request values dictionary
    :param cfg: optional **CoreConfig** dictionary

    :returns: **CoreSearchResultAI** on success
        **None** on non-success
    :rtype: CoreSearchResultAI or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/ai/result/search'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    debug = cfg.get("debug", False)
    verify = tls_utils.get_verify(cfg)
    log.debug(f"search ai result: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    r = s.post(
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
            log.info(f"search ai result success - {r.text}")
        try:
            rec_dict = json.loads(r.text)
            cur_o = (
                core_search_result_ai.CoreSearchResultAI()
            )
            cur_o.load_response_dict(rec_dict=rec_dict)
            return cur_o
        except Exception as e:
            log.error(
                f"failed to search ai_result.id={id} "
                f'with ex="{e}"'
            )
    return None
