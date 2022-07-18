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


def IsPointInPolygon(p:Point, polygon):
    
    minX = polygon[0].X
    maxX = polygon[0].X
    minY = polygon[0].Y
    maxY = polygon[0].Y
    for poly in polygon:
        if poly != polygon[0]:
            minX = min(poly.X, minX)
            maxX = max(poly.X, maxX)
            minY = min(poly.Y, minY)
            maxY = max(poly.Y, maxY)

    if p.X < minX or p.X > maxX or p.Y < minY or p.Y > maxY:
        return False

    inside = False
    j = len(polygon) - 1
    for i in range(0, len(polygon)):
        if ((polygon[i].Y > p.Y) != (polygon[j].Y > p.Y)) and p.X < (polygon[j].X - polygon[i].X) * (p.Y - polygon[i].Y) / (polygon[j].Y - polygon[i].Y) + polygon[i].X:
            inside = not inside

        # increment
        j = i

    return inside



    
