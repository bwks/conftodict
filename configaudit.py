"""
Functions for performing config audit
- Currently no tests
"""


class AuditResult(object):
    def __init__(self, ok=False, missing=None, extra=None, error=None):
        """
        Helper class to return result object
        :param ok: True/False
        :param missing: Missing entries
        :param extra: Extra entries
        :param error: Error string
        """
        self.ok = ok
        self.missing = missing
        self.extra = extra
        self.error = error


def search_dict_list(dict_list, dict_key, value_list):
    """
    Search a list of dictionaries for dict values
    # level 0 < dict_list
    #  level 1 < dict_key
    #   level 2 < [search for these values,
    #   level 2 < search for these values]
    #  level 1
    #   level 2
    #   level 2

    :param dict_list: A LIST of DICTIONARIES
    :param dict_key: The key to search for in dict_list
    :param value_list: LIST of values to check for
    :return: AuditResult object

    Example Usage:
    >>> from conftodict import ConfToDict
    >>> from configaudit import search_dict_list
    >>> c = ConfToDict('tests/test.txt', from_file=True)
    >>> stuff = c.to_dict()
    >>> things = ['priority percent 20', 'set ip dscp ef']
    >>> blah = search_dict_list(stuff['policy-map QOS_CATEGORIES'], 'class QOS_VOICE_RTP', things)
    >>> blah.ok
    >>> True
    """
    found = []
    not_found = []
    for i in dict_list:
        if dict_key in i:
            # Check for missing values
            for j in value_list:
                if j not in i[dict_key]:
                    not_found.append(j)
            # Check for extra values
            for j in i[dict_key]:
                if j not in value_list:
                    found.append(j)

            if not_found and not found:
                return AuditResult(ok=False, missing=not_found, error='value(s) not found')
            elif found and not not_found:
                return AuditResult(ok=False, extra=found, error='extra value(s) found')
            elif found and not_found:
                return AuditResult(ok=False, extra=found, missing=not_found,
                                   error='extra value(s) and value(s) not found')
            else:
                return AuditResult(ok=True)
        else:
            return AuditResult(ok=False, missing=dict_key, error='key not found')


def search_keys(conf_dict, conf_list):
    """
    Search dict keys for a list of commands
    :param conf_dict: DICTIONARY of config
    :param conf_list: LIST of keys to search for
    :return: AuditResult object
    """
    found = [i for i in conf_dict if i not in conf_list]
    not_found = [i for i in conf_list if i not in conf_dict]

    if not_found and not found:
        return AuditResult(ok=False, missing=not_found, error='key(s) not found')
    elif found and not not_found:
        return AuditResult(ok=False, extra=found, error='extra key(s) found')
    elif found and not_found:
        return AuditResult(ok=False, extra=found, missing=not_found,
                           error='extra key(s) and key(s) not found')
    else:
        return AuditResult(ok=True)


def search_key(conf_dict, key):
    """
    Search dict for a single key
    :param conf_dict: DICTIONARY of config
    :param key: STRING to search for
    :return: AuditResult object
    """
    if key in conf_dict:
        return AuditResult(ok=True)
    else:
        return AuditResult(ok=False, missing=key, error='key not found')


def search_values(dict_key, conf_list):
    """
    Search a dict_key's values for a list of commands
    # Examples:
    # level 0 < dict_key
    #  level 1 < [search for these values,
    #  level 1 < search for these values]

    # level 0
    #  level 1 < dict_key
    #   level 2 < [search for these values,
    #   level 2 < search for these values]

    :param dict_key: LIST from dictionary key
    :param conf_list: LIST of commands to search for
    :return: AuditResult object
    """
    found = [i for i in dict_key if i not in conf_list]
    not_found = [i for i in conf_list if i not in dict_key]

    if not_found and not found:
        return AuditResult(ok=False, missing=not_found, error='value(s) not found')
    elif found and not not_found:
        return AuditResult(ok=False, extra=found, error='extra value(s) found')
    elif found and not_found:
        return AuditResult(ok=False, extra=found, missing=not_found,
                           error='extra value(s) and value(s) not found')
    else:
        return AuditResult(ok=True)


def search_value(dict_key, value):
    """
    Search dict_key's values for a single value
    :param dict_key: List of config
    :param value: STRING to search for
    :return: AuditResult object
    """
    if value in dict_key:
        return AuditResult(ok=True)
    else:
        return AuditResult(ok=False, missing=value, error='value not found')
