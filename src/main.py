# Available Mode
decel_vest = 0
strobe_test = 1

# RUN MODE
EXECUTION_MODE = strobe_test

if EXECUTION_MODE == decel_vest:
    import decel_vest
elif EXECUTION_MODE == strobe_test:
    import strobe_test
else:
    print("Did not understand execution mode '" + str(EXECUTION_MODE) + "'")