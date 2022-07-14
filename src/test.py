import nmea
import speed_controller

f = open(r"C:\Users\tahan\Downloads\decel-vest\raw-data\20220713-3.txt")
content = f.readlines()
sc = speed_controller.speed_controller()

for line in content:
    
    try:
        tele = nmea.parse(line)

        if tele != None:
            print(str(tele.latitude) + ", " + str(tele.longitude))

        #sc.ingest(tele)
        #print(sc.speed_mph)
    except:
        pass

    