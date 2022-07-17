# Available Mode
decel_vest = 0
strobe_test = 1
record_processed = 2

# RUN MODE
EXECUTION_MODE = strobe_test

if EXECUTION_MODE == decel_vest:
    import decel_vest
elif EXECUTION_MODE == strobe_test:
    import strobe_test
elif EXECUTION_MODE == record_processed:
    import record_processed
else:
    print("Did not understand execution mode '" + str(EXECUTION_MODE) + "'")