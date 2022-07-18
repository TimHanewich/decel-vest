import json

class Point:
    X = 0.0
    Y = 0.0


def parse_json(json_string:str):
    doc = json.loads(json_string)
    areas = []
    for arr in doc:
        this_area = []
        for p in arr:
            pt = Point()
            pt.X = float(p["X"])
            pt.Y = float(p["Y"])
            this_area.append(pt)
        areas.append(this_area)
    return areas

def parse_file(path:str):
    f = open(path)
    content = f.readlines()
    content1 = ""
    for line in content:
        content1 = content1 + line
    
    areas = parse_json(content1)
    return areas

    
