import math

# returns distance in miles
# taken from https://github.com/TimHanewich/TimHanewich.Toolkit/blob/master/src/Geo/GeoToolkit.cs
def distance(lat1:float,lon1:float,lat2:float,lon2:float) -> float:

    # convert to radians
    lat1r = lat1 / (180 / math.pi)
    lon1r = lon1 / (180 / math.pi)
    lat2r = lat2 / (180 / math.pi)
    lon2r = lon2 / (180 / math.pi)

    con = 3963.0
    a = math.sin(lat1r)
    b = math.sin(lat2r)
    c = math.cos(lat1r)
    d = math.cos(lat2r)
    e = math.cos(lon2r - lon1r)
    a_times_b = a * b
    c_times_d_times_e = c * d * e
    ToArcCos = a_times_b + c_times_d_times_e
    ArcCos = math.acos(ToArcCos)
    DistanceMiles = con * ArcCos

    return DistanceMiles

# Converts a raw time field to number of seconds
def raw_seconds(val:str) -> int:
    p1 = int(val[0:2])
    p2 = int(val[2:4])
    p3 = int(val[4:6])
    tr = (p1 * 60 * 60) + (p2 * 60) + p3
    return tr

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


class gps_telemetry:
    fixed = None #seconds when it was received
    latitude = None
    longitude = None
    altitude = None
    satellites = None


def parse(line:str) -> gps_telemetry:

    # variables we will try to collect in each message below
    rFixed = None
    rLatitude = None
    rLatitudeDirection = None
    rLongitude = None
    rLongitudeDirection = None
    rAltitude = None
    rSatellites = None

    # variables we will plug in to. If each are set, we will update
    vFixed = None
    vLatitude = None
    vLongitude = None
    vAltitude = None
    vSatellites = None

    # find the parts we will use
    line_to_use = None
    try:
        gpgga_loc = line.lower().index("$gpgga")
        line_to_use = line[gpgga_loc:9999]
    except:
        return

    #split
    if line_to_use != None:
        parts = line_to_use.split(",")

    if "gpgga" in parts[0].lower():
        rFixed = parts[1]
        rLatitude = parts[2]
        rLatitudeDirection = parts[3]
        rLongitude = parts[4]
        rLongitudeDirection = parts[5]
        rSatellites = parts[7]
        rAltitude = parts[9]

    # get collected at
    if rFixed != None:
        vFixed = raw_seconds(rFixed)

    # get latitude
    if rLatitude != None and rLatitudeDirection != None:
        if rLatitude != "" and rLatitudeDirection != "":
            lat = raw_coord(rLatitude)
            if lat != None:
                if rLatitudeDirection.lower() == "n":
                    vLatitude = lat
                elif rLatitudeDirection.lower() == "s":
                    vLatitude = lat * -1

    # get longitude
    if rLongitude != None and rLongitudeDirection != None:
        if rLongitude != "" and rLongitudeDirection != "":
            lon = raw_coord(rLongitude)
            if lon != None:
                if rLongitudeDirection.lower() == "e":
                    vLongitude = lon
                elif rLongitudeDirection.lower() == "w":
                    vLongitude = lon * -1

    # get satellites
    if rSatellites != None:
        if rSatellites != "":
            vSatellites = float(rSatellites)

    # get altitude
    if rAltitude != None:
        if rAltitude != "":
            vAltitude = float(rAltitude)


    # Time to preapre the return object
    ToReturn = gps_telemetry()

    # set coordinates - only set all of these if they are all here
    if vFixed != None and vLatitude != None and vLongitude != None: 
        ToReturn.fixed = vFixed
        ToReturn.latitude = vLatitude
        ToReturn.longitude = vLongitude
        
    # set the satellites
    if vSatellites != None:
        ToReturn.satellites = vSatellites
    
    # set the altitude
    if vAltitude != None:
        ToReturn.altitude = vAltitude
