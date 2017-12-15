def is_match(dict1, dict2, strict=True):
    for key, value in dict1.iteritems():
        if key not in dict2:
            return False
        else:
            if isinstance(value, dict) and isinstance(dict2[key], dict):
                is_match(value, dict2[key])
            elif isinstance(value, list) and isinstance(dict2[key], list):
                if strict:
                    if set(value) != set(dict2[key]):
                        return False
            else:
                if value != dict2[key]:
                    return False
    return True

