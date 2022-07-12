
# ONGOING VARIABLES
latitude = 0.0
longitude = 0.0
altitude = 0.0
satellites = 0

def raw_coord(val:str) -> float:
    ind = val.index(".")
    if ind == 4:
        lat_str = val[0:2]
        degrees = val[2:999]
        tr = float(lat_str) + (float(degrees) / 60)
        return tr
    elif ind == 5:
        lon_str = val[0:3]
        degrees = val[3:999]
        tr = float(lon_str) + (float(degrees) / 60)
        return tr

def parse(data:bytes):

    global latitude, longitude, altitude, satellites

    s = data.decode("utf-8")
    parts = s.split(",")
    
    if "gpgga" in parts[0].lower():

        # get latitude
        rlat = raw_coord(parts[2])
        if parts[3].lower() == "n":
            latitude = rlat
        elif parts[3].lower() == "s":
            latitude = rlat * -1

        # get longitude
        rlon = raw_coord(parts[4])
        if parts[5].lower() == "w":
            longitude = rlon * -1
        elif parts[3].lower() == "e":
            longitude = rlon

        # altitude (meters)
        altitude = float(parts[9])

        # get satelittes
        satellites = int(parts[7])

    elif "gprmc" in parts[0].lower():
        # get latitude
        rlat = raw_coord(parts[3])
        if parts[4].lower() == "n":
            latitude = rlat
        else:
            latitude = rlat * -1

        # get longitude
        rlon = raw_coord(parts[5])
        if parts[6].lower() == "w":
            longitude = rlon * -1
        else:
            longitude = rlon