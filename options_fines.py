"""Multiple-choice options for each question in questions_fines.csv (Fines, Limits & Points).

OPTIONS[n] = (correct, wrong), as in options.py: `correct` is a short form of the CSV answer (None = use
the CSV answer as written), `wrong` is three plausible but incorrect choices.
"""

POINT_VALUES = [2, 3, 4, 6, 7]  # demerit points Ontario gives for a single offence


def points(n):
    """Options for 'how many demerit points' questions: the three nearest other point values."""
    others = sorted((v for v in POINT_VALUES if v != n), key=lambda v: (abs(v - n), v))[:3]
    return (f"{n} demerit points", [f"{v} demerit points" for v in sorted(others)])


OPTIONS = {
    **{n: points(7) for n in range(1, 3)},
    **{n: points(6) for n in range(3, 8)},
    **{n: points(4) for n in range(8, 11)},
    **{n: points(3) for n in range(11, 30)},
    **{n: points(2) for n in range(30, 46)},
    46: (None, ['1 to 3', '4 to 7', '6 to 8']),
    47: (None, ['2 to 5', '4 to 6', '9 or more']),
    48: (None, ['6 or more', '12 or more', '15 or more']),
    49: (None, ['2 to 5', '9 to 14', '15 or more']),
    50: ('9 to 14', ['6 to 8', '10 to 12', '15 or more']),
    51: (None, ['9 or more', '12 or more', '20 or more']),
    52: (None, ['7 days', '60 days', '90 days']),
    53: (None, ['30 days', '60 days', '1 year']),
    54: ('Licence cancellation and removal from the graduated licensing system', ['A 30-day licence suspension', 'A 90-day licence suspension', 'A $500 fine with no suspension']),
    55: ('7 demerit points', ['0 demerit points', '4 demerit points', '10 demerit points']),
    56: ('4 demerit points', ['0 demerit points', '2 demerit points', '7 demerit points']),
    57: (None, ['Only one passenger', 'Up to three passengers', 'No passengers unless a fully licensed driver is present']),
    58: (None, ['6 months', '8 months', '24 months']),
    59: (None, ['Your G1 licence', 'Your birth certificate', "Your vehicle's ownership permit only"]),
    60: ('5 years', ['2 years', '3 years', '10 years']),
    61: ('15 metres', ['5 metres', '9 metres', '30 metres']),
    62: ('125 metres', ['60 metres', '100 metres', '150 metres']),
    63: ('Up to three passengers aged 19 or under', ['Only one passenger aged 19 or under', 'Up to two passengers aged 19 or under', 'No passengers aged 19 or under']),
    64: ('A fine of $400–$2,000 and 3 demerit points', ['A $110 fine and 2 demerit points', 'A fine of $1,000–$4,000 and a possible jail sentence', 'A warning letter with no fine']),
    65: ('A fine of $1,000–$4,000, possible jail time and a possible licence suspension', ['A fine of $400–$2,000 and 3 demerit points', 'A $110 fine and 2 demerit points', 'A 30-day licence suspension only']),
    66: ('Not closer than 3 metres', ['Not closer than 1 metre', 'Not closer than 5 metres', 'Not closer than 9 metres']),
    67: ('A fine of up to $1,000 and 3 demerit points', ['A fine of up to $500 and 2 demerit points', 'A fine of up to $2,000 and 6 demerit points', 'A warning with no fine or points']),
    68: ('Within 6 days', ['Within 24 hours', 'Within 15 days', 'Within 30 days']),
    69: (None, ['4 months', '6 months', '12 months']),
    70: ('Demerit points are added as if the offence happened in Ontario', ['No demerit points are added to your Ontario record', 'Only a fine applies, with no demerit points', 'Demerit points are added only if you lived in that province']),
    71: (None, ['15 metres', '30 metres', '150 metres']),
    72: ('Midnight and 5 a.m.', ['9 p.m. and 6 a.m.', '10 p.m. and 5 a.m.', '1 a.m. and 6 a.m.']),
    73: ('Within 60 metres', ['Within 30 metres', 'Within 100 metres', 'Within 150 metres']),
    74: ('Cost you 6 demerit points and a fine of up to $2,000', ['Cost you 3 demerit points and a $110 fine', 'Cost you 4 demerit points and a $500 fine', 'Cost you 7 demerit points and a $5,000 fine']),
    75: ('Within 150 metres', ['Within 60 metres', 'Within 100 metres', 'Within 300 metres']),
    76: (None, ['0.00%', '0.08%', '0.10%']),
    77: (None, ['0.5 metres', '2 metres', '3 metres']),
    78: ('No, offences in some U.S. states can also add demerit points', ['Yes, only offences in Canada count', 'Yes, only offences in Ontario count', 'No, offences anywhere in the world count']),
    79: (None, ['40 km/h', '60 km/h', '70 km/h']),
    80: ('When 6 demerit points have been accumulated', ['When 2 demerit points have been accumulated', 'When 9 demerit points have been accumulated', 'When 15 demerit points have been accumulated']),
    81: ('May carry up to three passengers aged 19 or under', ['May carry only one passenger aged 19 or under', 'May carry no passengers aged 19 or under', 'May carry any number of passengers']),
    82: (None, ['3 metres', '6 metres', '15 metres']),
    83: ('A $110 fine and 3 demerit points', ['An $85 fine and 2 demerit points', 'A $250 fine and 4 demerit points', 'A $500 fine and no demerit points']),
    84: ('1 passenger aged 19 or under', ['No passengers aged 19 or under', '2 passengers aged 19 or under', '3 passengers aged 19 or under']),
    85: ('Stop not less than 5 metres from the nearest rail', ['Stop not less than 2 metres from the nearest rail', 'Stop not less than 15 metres from the nearest rail', 'Slow down and cross quickly']),
    86: ("From ½ hour before sunset to ½ hour after sunrise, or when you can't see clearly for 150 m", ['Only between sunset and sunrise', 'From one hour before sunset to one hour after sunrise', 'Only when street lights are off']),
    87: ('Holds a full G licence, has at least 4 years of experience and is the only front-seat passenger', ['Holds a G2 licence and is at least 18 years old', 'Holds a full G licence with at least 1 year of experience', 'Is any adult over 21, seated anywhere in the car']),
    88: ('A licence suspension of up to 2 years, a fine of up to $2,000 and up to 6 months in jail', ['A 30-day licence suspension and a $500 fine', 'A $110 fine with no suspension', 'A lifetime licence suspension']),
    89: (None, ['$50,000', '$100,000', '$1,000,000']),
    90: ('Have your licence suspended, pay a fine of up to $25,000 and/or go to prison', ['Receive only a warning letter', 'Pay a $110 fine and get 2 demerit points', 'Have your vehicle held for 24 hours only']),
    91: ('On a curve, near a railway crossing or hilltop, or near a bridge or tunnel that blocks your view', ['On any street with two or more lanes', 'Only on 400-series highways', 'Only at night']),
    92: ('A $2,000–$10,000 fine, up to 2 years in jail and a licence suspension of up to 5 years', ['A $500 fine and 3 demerit points', 'A $1,000 fine and a 30-day suspension', 'A warning letter and a driver improvement course']),
    93: ('An immediate 3-day roadside licence suspension and a $250 penalty', ['A warning with no suspension', 'A $110 fine and 3 demerit points', 'A 1-year licence suspension only']),
    94: ('Someone is hurt or killed, or damage exceeds $2,000', ['Damage exceeds $500', 'Damage exceeds $1,000, even if no one is hurt', 'Only if someone is killed']),
}
