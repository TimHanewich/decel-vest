
# ONGOING VARIABLES
fixed = 0 # number of seconds in UTC time that was collected
latitude = 0.0
longitude = 0.0
altitude = 0.0
satellites = 0

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
        fixed = vFixed
        latitude = vLatitude
        longitude = vLongitude
        
    # set the satellites
    if vSatellites != None:
        satellites = vSatellites
    
    # set the altitude
    if vAltitude != None:
        altitude = vAltitude

        
parse(b'$GPGGA,233517.00,2.38482,N,08227.11282,W,1,06,1.33,25.1,M,,*5A')
print(latitude)
print(longitude)
print(altitude)