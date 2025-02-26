def parse_annotations(annotations: str):
    """annotations are in format: key1=val1,key2=val2,...
    this function parse it into dictionary as {key1: val1, key2: val2, ...}
    """
    pairs = annotations.split(",")
    parsed = {}
    for pair in pairs:
        key, val = pair.split("=")
        parsed[key] = val
    return parsed
