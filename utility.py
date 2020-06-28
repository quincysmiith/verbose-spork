from dateutil.parser import parse
from datetime import datetime
import datetime as dt
import random

### For plotting

import plotly
import plotly.graph_objs as go

import pandas as pd
import json

def make_float(some_object):
    if type(some_object) is float:
        return some_object
    else:
        to_return = float(some_object)
        assert (type(to_return) is float),"unable to convert to float"
        return to_return


def parse_dates(a_string):
    try:
        date = parse(a_string)
        date = date.date()
    except:
        date = datetime.now().date()
    return date


def create_plot():

    numdays = 5
    base = datetime.today().date()
    x = [base - dt.timedelta(days=x) for x in range(numdays)]

    y = random.sample(range(1, 101), numdays)

    df = pd.DataFrame({'x': x, 'y': y})

    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)