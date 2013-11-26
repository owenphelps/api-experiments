#from bottle import default_app
from bottle import route, request, response, get, post, put, abort, hook
import json
import datetime
from random import randrange

courses = [ "aintree","ascot","ayr","bangor-on-dee","bath","beverley","brighton","carlisle","cartmel","catterick bridge","cheltenham","chepstow","chester","doncaster","epsom","exeter","fakenham","ffos las","fontwell park","goodwood","hamilton park","haydock park","hexham","huntingdon","kelso","kempton park","leicester","lingfield park","ludlow","market rasen","musselburgh","newbury","newcastle","newmarket","newton abbot","nottingham","perth","plumpton","pontefract","redcar","ripon","salisbury","sandown","sedgefield","southwell","stratford-on-avon","taunton","thirsk","towcester","uttoxeter","warwick","wetherby","wincanton","windsor","wolverhampton","worcester","great yarmouth","york" ]

courses = [x.title() for x in courses]
avail_races = [
    ('Chase',
     "THE JEWSON NOVICES' STEEPLE CHASE (Registered as the Golden Miller Novices' Steeple Chase)"),
    ('Chase', 'THE BYRNE GROUP PLATE (A HANDICAP STEEPLE CHASE)'),
    ('Hurdle',
     "THE ALBERT BARTLETT NOVICES' HURDLE RACE (Registered as The Spa Novices' Hurdle Race)"),
    ('Hurdle', 'THE JCB TRIUMPH HURDLE RACE '),
    ('Chase', 'THE BETFRED CHELTENHAM GOLD CUP STEEPLE CHASE'),
    ('Chase',
     'THE JOHNNY HENDERSON GRAND ANNUAL STEEPLE CHASE CHALLENGE CUP (HANDICAP)'),
    ('Hurdle', "THE VINCENT O'BRIEN COUNTY HANDICAP HURDLE RACE "),
    ('AWT', 'THE BLUE SQUARE WINTER DERBY'),
    ('Flat', 'THE WILLIAM HILL LINCOLN (HERITAGE HANDICAP)'),
    ('Hurdle', 'THE MATALAN ANNIVERSARY 4-Y-O JUVENILE HURDLE RACE'),
    ('Hurdle', 'THE LIVERPOOL HURDLE RACE'),
    ('Chase', 'THE Betfred BOWL STEEPLE CHASE'),
    ('Chase', "THE Betfred MANIFESTO NOVICES' STEEPLE CHASE"),
    ('Chase', 'THE matalan.co.uk RED RUM HANDICAP STEEPLE CHASE'),
    ('Hurdle', "THE JOHN SMITH'S SEFTON NOVICES' HURDLE RACE"),
    ('Chase', "THE JOHN SMITH'S MELLING STEEPLE CHASE"),
    ('Chase', "THE JOHN SMITH'S MILDMAY NOVICES' STEEPLE CHASE"),
    ('Hurdle', "THE JOHN SMITH'S TOP NOVICES' HURDLE RACE"),
    ('Hurdle', 'THE SILVER CROSS HANDICAP HURDLE RACE'),
    ('Chase', "THE JOHN SMITH'S TOPHAM STEEPLE CHASE (HANDICAP)"),
    ('Chase', "THE JOHN SMITH'S MAGHULL NOVICES' STEEPLE CHASE"),
    ('Hurdle', "THE JOHN SMITH'S AINTREE HURDLE"),
    ('Flat', "THE JOHN SMITH'S CHAMPION STANDARD OPEN NATIONAL HUNT FLAT RACE"),
    ('Hurdle', "THE JOHN SMITH'S MERSEY NOVICES' HURDLE RACE"),
    ('Chase', "THE JOHN SMITH'S GRAND NATIONAL STEEPLE CHASE"),
    ('Chase', 'THE CERES ESTATES SILVER TROPHY STEEPLE CHASE (A HANDICAP)'),
    ('Flat', 'THE LANWADES STUD NELL GWYN STAKES'),
    ('Flat', 'THE NOVAE BLOODSTOCK INSURANCE CRAVEN STAKES'),
    ('Flat', 'THE WEATHERBYS EARL OF SEFTON STAKES'),
    ('Chase',
     'THE ARCADIA CONSULTING WILLIAM DICKIE & MARY ROBERTSON FUTURE CHAMPION NOVICES STEEPLE CHASE'),
    ('Hurdle',
     'THE ISLE OF SKYE BLENDED WHISKY SCOTTISH CHAMPION HURDLE RACE (A LIMITED HANDICAP)'),
    ('Chase', 'THE CORAL SCOTTISH GRAND NATIONAL HANDICAP STEEPLE CHASE'),
    ('Flat', 'THE AON GREENHAM STAKES'),
    ('Flat',
     'THE DUBAI DUTY FREE STAKES (Registered as The Fred Darling Stakes)'),
    ('Flat',
     'THE DUBAI DUTY FREE FINEST SURPRISE STAKES (Registered as The John Porter Stakes)'),
    ('Flat', 'THE bet365 MILE '),
    ('Flat', 'THE bet365 CLASSIC TRIAL')
    ]

race_types = ["Flat", "AWT", "Chase", "Hurdle", "Mixed"]
times = ["Afternoon", "Twilight", "Evening"]
goings = ["Good", "Good to firm", "Soft"]

one_day = datetime.timedelta(1)
start_date = datetime.date.today() - 10 * one_day
today_s = start_date.isoformat()
dates = [(start_date + n * one_day).isoformat() for n in range(0, 50)]

fixtures = []
fixture_count = 0
for date in dates:
    nc = randrange(1, 5)
    for i in range(1, nc+1):
        fixture_count += 1
        course = courses[randrange(0, len(courses))]
        race_type = race_types[randrange(0, len(race_types))]
        time = times[randrange(0, len(times))]
        going = goings[randrange(0, len(goings))]
        fixtures.append(
            dict(id=fixture_count, date=date, course=course, type=race_type, time=time, advancedGoing=going)
            )

fixture_races = []
race_count = 0
for fixture in fixtures:
    nr = randrange(3, 12)
    for i in range(1, nr+1):
        race_count += 1
        race = avail_races[randrange(0, len(avail_races))]
        fixture_races.append(
            dict(id=race_count, fixtureId=fixture['id'], type=race[0], title=race[1])
            )

@hook('after_request')
def enable_cors():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    response.set_header('Access-Control-Allow-Headers', 'X-Requested-With')


def get_prefix(request, path='/racing/api'):
    urlparts = request.urlparts
    protocol = urlparts[0]
    domain = urlparts[1]
    if domain.endswith(':80'):
        domain = domain[:-3]

    return "%s://%s%s" % (protocol, domain, path)


@route('/racing/api/handicappers', method=['OPTIONS'])
@route('/racing/api/fixtures', method=['OPTIONS'])
@route('/racing/api/fixtures/:id/races', )
def get_options():
    return json.dumps({})


@get('/racing/api/')
@get('/racing/api')
def racing_api_root():
    prefix = get_prefix(request)
    return dict(
        documentation=prefix + "/docs",
        services=dict(
            races=prefix + "/races",
            handicappers=prefix + "/handicappers"
            )
        )


@get('/racing/api/handicappers')
def get_handicappers():
    response.set_header('Content-Type', 'application/json')

    prefix = get_prefix(request)

    result = [{'id': 1, 'name': 'Frank'}, {'id': 2, 'name': 'Martin'}, {'id': '3', 'name': 'Jason'}]
    return json.dumps(result) #'[' + ',\n'.join(result) + ']'


@get('/racing/api/fixtures')
def get_fixtures():
    response.set_header('Content-Type', 'application/json')

    prefix = get_prefix(request)

    result = fixtures

    return json.dumps(result)

@get('/racing/api/fixtures/:id/races')
def get_fixtures():
    response.set_header('Content-Type', 'application/json')

    prefix = get_prefix(request)

    result = fixtures
