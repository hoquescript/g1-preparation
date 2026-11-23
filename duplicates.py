"""Groups of near-duplicate questions, across categories.

Numbers are the global question numbers in question_bank.js: Road Rules 1-203 as in questions.csv,
Fines 1001-1094 (1000 + the number in questions_fines.csv). Each group asks the same fact, or one
question gives away another's answer. quiz.html puts at most one question from each group into a test.
"""

DUPLICATES = [
    [3, 150],             # low beams in fog / poor weather
    [6, 70, 1094],        # report collisions over $2000
    [7, 161, 1073],       # low beams within 60 m when following
    [8, 132],             # no persons in a house or boat trailer
    [12, 130],            # report a collision immediately
    [14, 124, 1079],      # 50 km/h in built-up areas
    [15, 131],            # flashing amber / yellow beacon
    [18, 107],            # overdriving your headlights
    [26, 155],            # yield sign
    [30, 135],            # stop 2 m behind a streetcar's rear door
    [36, 86],             # wheels off the pavement / off the road
    [39, 66, 108, 122],   # 90-day roadside suspension
    [40, 106],            # never lend your licence
    [44, 134],            # right turn on red
    [47, 153],            # flashing red light / beacon
    [49, 141],            # blue lights mean snow removal
    [59, 112],            # exiting a freeway or expressway
    [64, 164, 169],       # blind spots and shoulder checks
    [80, 162],            # broken line: may pass if clear
    [84, 138],            # solid line: unsafe to pass
    [91, 181],            # whiteout / dense fog: pull off with flashers
    [95, 116],            # steer where you want to go in a skid / on black ice
    [96, 127],            # causes of skids
    [97, 182],            # roads most slippery when rain begins
    [100, 148],           # two-second rule
    [110, 196],           # register within 30 days
    # Road Rules and Fines asking the same fact
    [16, 1087],           # accompanying driver: 4 years' experience
    [20, 1084],           # G2 teen, first 6 months: 1 young passenger at night
    [21, 1063, 1081],     # G2 teen after 6 months: 3 young passengers
    [23, 1075],           # low beams within 150 m of oncoming vehicles
    [25, 1085],           # stop 5 m from the rail at a crossing signal
    [27, 1086],           # when headlights are required
    [46, 1068],           # report a name or address change within 6 days
    [69, 1076],           # accompanying driver BAC under 0.05
    [81, 1066],           # 3 m from a fire hydrant
    [105, 1093],          # new driver drinking and driving
    [111, 1077],          # 1 m when passing a cyclist
    [128, 1072],          # G1: no driving midnight to 5 a.m.
    [133, 1001],          # 7 points for leaving the scene of a collision
    [163, 1051],          # 15 points: 30-day suspension
    [198, 1062],          # 125 m clear view to park
    [199, 1061],          # 15 m from a level railway crossing
    [200, 1071],          # 100 m from a bridge
    [203, 1082],          # 9 m from an intersection without lights
    # Fines asking the same fact
    [1003, 1088],         # careless driving: 6 points
    [1005, 1092],         # 50 km/h or more over: 6 points
    [1007, 1074],         # school bus: 6 points
    [1011, 1067],         # distracted driving: 3 points
    [1021, 1022, 1064],   # Move Over law: 3 points
    [1025, 1083],         # HOV lane: 3 points
]
