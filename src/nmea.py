import math

# ONGOING VARIABLES
fixed = 0 # number of seconds in UTC time that was collected
latitude = 0.0
longitude = 0.0
altitude = 0.0
satellites = 0
speed_mph = 0.0

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

def parse(data:bytes):

    global fixed
    global latitude
    global longitude
    global altitude
    global satellites
    global speed_mph

    s = data.decode("utf-8")
    parts = s.split(",")

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
    
    if "gpgga" in parts[0].lower():
        rFixed = parts[1]
        rLatitude = parts[2]
        rLatitudeDirection = parts[3]
        rLongitude = parts[4]
        rLongitudeDirection = parts[5]
        rSatellites = parts[7]
        rAltitude = parts[9]

    # get collected at
    vFixed = raw_seconds(rFixed)

    # get latitude
    if rLatitude != None and rLatitudeDirection != None:
        lat = raw_coord(rLatitude)
        if lat != None:
            if rLatitudeDirection.lower() == "n":
                vLatitude = lat
            elif rLatitudeDirection.lower() == "s":
                vLatitude = lat * -1

    # get longitude
    if rLongitude != None and rLongitudeDirection != None:
        lon = raw_coord(rLongitude)
        if lon != None:
            if rLongitudeDirection.lower() == "e":
                vLongitude = lon
            elif rLongitudeDirection.lower() == "w":
                vLongitude = lon * -1

    # get satellites
    if rSatellites != None:
        vSatellites = int(rSatellites)

    # get altitude
    if rAltitude != None:
        vAltitude = float(rAltitude)

    # set coordinates - only set all of these if they are all here
    if vFixed != None and vLatitude != None and vLongitude != None:

        # calculate speed?
        if fixed != None:
            if fixed != 0:
                if latitude != None and longitude != None:
                    dist = distance(latitude, longitude, vLatitude, vLongitude)
                    hours = (vFixed - fixed) / 60 / 60 # the difference between vFixed and fixed is in seconds, so need to divide by 60 and then 60 again to get it in hours.
                    mph = dist / hours
                    speed_mph = mph

        # set values
        fixed = vFixed
        latitude = vLatitude
        longitude = vLongitude
        
    # set the satellites
    if vSatellites != None:
        satellites = vSatellites
    
    # set the altitude
    if vAltitude != None:
        altitude = vAltitude

        
#parse(b'$GPGGA,233517.00,2.38482,N,08227.11282,W,1,06,1.33,25.1,M,,*5A')
parse(b'GPGGA,185227.00,2712.37950,N,08227.10759,W,1,10,0.95,9.5,M,-26.9,M,,*6F\r\n')
print(fixed)
print(latitude)
print(longitude)
print(altitude)
print(satellites)