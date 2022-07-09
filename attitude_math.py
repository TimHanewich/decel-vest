import math

# returns pitch,roll
def attitude(gx:float,gy:float,gz:float):

    # inputs are provided in G's. Conver to m/s2
    ms2_x = gx * 9.80665
    ms2_y = gy * 9.80665
    ms2_z = gz * 9.80665

    # calculate in radions
    # I'm taking this calculation from here (page 3): https://aatishb.com/materials/srr/workshop3.pdf

    # calculate pitch
    tdb = math.sqrt((ms2_y * ms2_y) + (ms2_z * ms2_z))
    if tdb == 0:
        return 0,0
    pitch_rads = math.atan(ms2_x / tdb)

    # calculate roll
    tdb = math.sqrt((ms2_x * ms2_x) + (ms2_z * ms2_z))
    if tdb == 0:
        return 0,0
    roll_rads = math.atan(ms2_y / tdb)
    
    # convert from rads to degrees
    pitch_degs = pitch_rads * (180 / math.pi)
    roll_degs = roll_rads * (180 / math.pi)

    return pitch_degs, roll_degs


print(attitude(0, 0, 0))