"""
Functions for performing config audit
- Currently no tests
"""


class AuditResult(object):
    def __init__(self, ok=False, missing=None, error=None):
        """
        Helper class to return result
        :param ok: True/False
        :param missing: Missing entries
        :param error: Error value
        """
        self.ok = ok
        self.missing = missing
        self.error = error


def search_dict(dict_list, dict_key, value_list):
    """
    A list of dictionaries to search for values
    :param dict_list: A list of dictionaries
    :param dict_key: The key to search for in dict_list
    :param value_list: List of values to check for
    :return: something

    Example Usage:
    >>> from conftodict import ConfToDict
    >>> from configaudit import search_dict
    >>> c = ConfToDict('tests/test.txt', from_file=True)
    >>> stuff = c.to_dict()
    >>> things = ['priority percent 20', 'set ip dscp ef']
    >>> blah = search_dict(stuff['policy-map QOS_CATEGORIES'], 'class QOS_VOICE_RTP', things)
    >>> blah.ok
    >>> True
    """
    found = []
    not_found = []
    for i in dict_list:
        if dict_key in i:
            for j in value_list:
                if j in i[dict_key]:
                    found.append(j)
                else:
                    not_found.append(j)
            if not_found:
                return AuditResult(ok=False, missing=not_found, error='value(s) not found')
            else:
                return AuditResult(ok=True)
        else:
            return AuditResult(ok=False, missing=dict_key, error='key not found')
