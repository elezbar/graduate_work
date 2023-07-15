import time


def camelcase_to_snake(val: str) -> str:
    """
    Converts CamelCaseString to stake_case_string
    """

    if not val:
        # nothing to change
        return val

    new_val = [val[0].lower()]
    for v in val[1:]:
        new_val.append(v if not v.isalpha() or v.islower() else f"_{v.lower()}")
    return "".join(new_val)


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print(f"Duration is {(time2-time1)*1000.0} ms")
        return ret

    return wrap
