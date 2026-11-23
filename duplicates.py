"""Groups of near-duplicate questions in questions.csv.

Each group asks the same fact, or one question gives away another's answer. quiz.html puts at most
one question from each group into a test.
"""

DUPLICATES = [
    [3, 150],             # low beams in fog / poor weather
    [6, 70],              # report collisions over $2000
    [7, 161],             # low beams within 60 m when following
    [8, 132],             # no persons in a house or boat trailer
    [12, 130],            # report a collision immediately
    [14, 124],            # 50 km/h in built-up areas
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
]
