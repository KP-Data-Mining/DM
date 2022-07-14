import os
import pandas as pd
import numpy as np
import pylab

from bokeh.layouts import column, row
from bokeh.models import Select, DatetimeTickFormatter
from bokeh.plotting import curdoc, figure, show
from win32api import GetSystemMetrics

param = curdoc().session_context.request.arguments
cluster_num = int(param['cluster'][0])
print(cluster_num)

df = pd.read_csv('2.csv')
df2 = pd.read_csv('3.csv')

cm = pylab.get_cmap('RdYlBu')
cgen = [cm(1.*i/len(df)) for i in range(len(df))]
cgen.reverse()
df = df.join(df2.set_index('index'), on='index')
df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%d %H:%M:%S")
df = df.drop(columns=["index"])
df = df.query('Кластер == ' + str(cluster_num))
df.reset_index(drop=True)

markers = ["star" if defect > 75 else "circle" for defect in df['defects']]

SIZES = [20 if defect > 75 else 12 for defect in df['defects']]
COLORS = ['#%02x%02x%02x' % (int(list(each)[0] * 0xFF), int(list(each)[1] * 0xFF), int(list(each)[2] * 0xFF))
          for each in cgen]
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]


def create_figure():
    xs = df[x.value].values
    x_axis_type = 'linear'
    y_axis_type = 'linear'
    if pd.api.types.is_datetime64_ns_dtype(xs.dtype):
        x_axis_type = 'datetime'
    ys = df[y.value].values
    if pd.api.types.is_datetime64_ns_dtype(ys.dtype):
        y_axis_type = 'datetime'
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "\'%s\' и \'%s\'" % (x_title, y_title)
    width = GetSystemMetrics(0) - round(GetSystemMetrics(0) * 0.20)
    height = GetSystemMetrics(1) - round(GetSystemMetrics(1) * 0.10)
    p = figure(width=width, height=height, x_axis_type=x_axis_type, y_axis_type=y_axis_type,
               tools='pan,box_zoom,hover,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 2

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if df[color.value].dtype == np.float64:
            factor = (N_COLORS - 1) / df[color.value].max() - df[color.value].min()
            c = [COLORS[int(xx * factor)] for xx in df[color.value]]
        else:
            if len(set(df[color.value])) > N_COLORS:
                groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
            else:
                groups = pd.Categorical(df[color.value])
            c = [COLORS[xx] for xx in groups.codes]

    p.scatter(x=xs, y=ys, color=c, size=SIZES, marker=markers, line_color="black", alpha=0.7, hover_color='white',
              hover_alpha=0.5)
    date_format = DatetimeTickFormatter(milliseconds='%d.%m.%Y %H:%M:%S', seconds='%d.%m.%Y %H:%M:%S',
                                        minsec='%d.%m.%Y %H:%M:%S', minutes='%d.%m.%Y %H:%M:%S',
                                        hourmin='%d.%m.%Y %H:%M', hours='%d.%m.%Y %H:%M', days='%d.%m.%Y %H:%M',
                                        months='%d.%m.%Y', years='%d.%m.%Y')
    if x_axis_type == 'datetime':
        p.xaxis[0].formatter = date_format
    if y_axis_type == 'datetime':
        p.yaxis[0].formatter = date_format
    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='Ось абсцисс (x)', value='time', options=columns)
x.on_change('value', update)

y = Select(title='Ось ординат (y)', value='time', options=columns)
y.on_change('value', update)

size = Select(title='Размер', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Цвет', value='None', options=['None'] + continuous)
color.on_change('value', update)

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"
