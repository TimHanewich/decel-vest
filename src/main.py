# Available Mode
decel_vest = 0
strobe_test = 1
record_processed = 2
record_raw = 3
strobe_solid = 4
pitlane_test = 5

# RUN MODE
EXECUTION_MODE = decel_vest

if EXECUTION_MODE == decel_vest:
    import decel_vest
elif EXECUTION_MODE == strobe_test:
    import strobe_test
elif EXECUTION_MODE == record_processed:
    import record_processed
elif EXECUTION_MODE == record_raw:
    import record_raw
elif EXECUTION_MODE == strobe_solid:
    import strobe_solid
elif EXECUTION_MODE == pitlane_test:
    import pitlane_test
else:
    print("Did not understand execution mode '" + str(EXECUTION_MODE) + "'")