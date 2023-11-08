"""
helper for pretty printing a dictionary
"""
import ujson as json


def ppj(json_data: dict):
    """
    ppj

    :param json_data: dictionary to print

    :returns: string for the dictionary
    :rtype: str
    """
    return str(
        json.dumps(
            json_data,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )
    )
