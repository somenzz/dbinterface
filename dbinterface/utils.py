import re


def is_unsafe_sql(sql) -> bool:
    if sql.replace(" ", "") == "":
        return False
    result = re.findall(r"--|;|#|delete|drop|update|truncate|/\*|\*/", sql.lower())
    if result:
        return True
    return False


def iter_count(file_name, encoding="utf-8"):
    from itertools import takewhile, repeat

    buffer = 1024 * 1024
    with open(file_name, mode="r", encoding=encoding, errors="ignore") as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count("\n") for buf in buf_gen)
