import os
import pandas
import numpy as np
import matplotlib.pyplot as plt

from bokeh.io import curdoc
from subprocess import Popen
from win32api import GetSystemMetrics
from bokeh.plotting import figure, save
from MODELS.DBSCAN.Clustering.PlotWindow import PlotWindow
from bokeh.models import ColumnDataSource, Legend, LegendItem, TapTool, OpenURL


def show():
    p = Popen(['bokeh', 'serve', "MODELS\\DBSCAN\\Crossfilter"], shell=True)
    window = PlotWindow(link="file:///TSAC.html", server=p)
    return window


def create(df_points, df_defects, df_labels, df_info, defect_limit=75, title="Plot", x_axis_label="X",
           y_axis_label="Y"):
    df_info = df_info.T
    df_info_html = [pandas.DataFrame(df_info[i]).to_html(header=False) for i in range(len(df_points))]
    markers = ["star" if defect > defect_limit else "circle" for defect in df_defects]
    unique_labels = set(df_labels)
    unique_colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    unique_color_rgb = [
        '#%02x%02x%02x' % (int(list(each)[0] * 0xFF), int(list(each)[1] * 0xFF), int(list(each)[2] * 0xFF))
        for each in unique_colors]
    fill_colors = [unique_color_rgb[each] for each in df_labels]
    x = df_points[:, 1]
    y = df_points[:, 0]
    sizes = [20 if defect > defect_limit else 12 for defect in df_defects]

    source = ColumnDataSource(dict(x=x, y=y, sizes=sizes, marker=markers, fill_color=fill_colors,
                                   defects=df_defects, info=df_info_html, labels=df_labels))
    TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,"\
            "lasso_select, "
    TOOLTIPS = open(os.getcwd() + "\\MODELS\\DBSCAN\\Clustering\\tooltips.html", "r", encoding='utf-8').read()

    width = GetSystemMetrics(0) - round(GetSystemMetrics(0) * 0.03)
    height = GetSystemMetrics(1) - round(GetSystemMetrics(1) * 0.10)

    plot = figure(title=title, width=width, height=height, min_border=0, toolbar_location="right", tools=TOOLS,
                  tooltips=TOOLTIPS, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    r = plot.scatter(x="x", y="y", size="sizes", line_color='black', fill_color="fill_color", fill_alpha=1,
                     line_width=0.9, marker='marker', source=source)
    arr = []
    for i in range(len(df_defects)):
        arr.append([df_labels[i], df_defects[i]])
    data_f = pandas.DataFrame(arr, columns=['clusters', 'defects'])
    data_max = data_f[data_f.groupby(['clusters'])['defects'].transform(max) == data_f['defects']].drop_duplicates(
        subset=['defects', 'clusters']).sort_values(by=['clusters'])
    items = [LegendItem(label=str(data_max['clusters'][i]), renderers=[r], index=i) for i in data_max.index]
    legend = Legend(items=items, border_line_color='#151515')
    plot.add_layout(legend)
    plot.legend.glyph_height = 40
    plot.legend.glyph_width = 80
    plot.legend.label_text_font_size = "1.6em"

    url = "http://localhost:5006/Crossfilter/?cluster=@labels"
    tap_tool = plot.select(type=TapTool)
    tap_tool.callback = OpenURL(url=url, same_tab=True)
    curdoc().add_root(plot)
    save(plot)
