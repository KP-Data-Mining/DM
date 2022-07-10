import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def Start(data, defects, x_label='X', y_label='Y', defect_limit=75.0, eps=0.25, min_samples=10):
    """
    Запускает визуализацию данных:\n
    data - 2D обычный массив с X и Y. [[x0, y0], [x1, y1],... [xn, yn]]\n
    defects - массив всех дефектов\n
    defect_limit - предельльное значение дефекта.\n
        Если дефект больше defect_limit в заданой точке, то рисуется звездочка\n
    defect_name - например 'Defects.Roll10Sqm.DefMap1' (чероные точки)\n
    eps - радиус поиска соседей для алгоритма. чем больше, тем меньше плотность кластера может быть\n
    min_samples - минимальное кол-во соседей
    """

    fig, ax = plt.subplots(1, figsize=(12,6))

    values = []
    for i in range(len(data)):
        values.append(np.array([data[i][1], data[i][0]]))  # это пример

    values = np.array(values)
    defects = np.array(defects)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(values)
    labels = db.labels_
    unique_labels = set(labels)
    unique_colors = [plt.cm.Spectral(each)
                     for each in np.linspace(0, 1, len(unique_labels))]
    colors = []

    bad_defects = []
    good_defects = []
    for i in range(len(labels)):
        colors.append(np.array(unique_colors[labels[i]]))
        if defects[i] <= defect_limit:
            good_defects.append(defects[i])
        elif defects[i] > defect_limit:
            bad_defects.append(defects[i])

    scatters = []
    np_array_x = np.array(values.T[0])[defects <= defect_limit]
    np_array_y = np.array(values.T[1])[defects <= defect_limit]
    color_array1 = (np.array(colors)[defects <= defect_limit]).tolist()
    color_array2 = (np.array(colors)[defects > defect_limit]).tolist()
    scatters.append(ax.scatter(np_array_x, np_array_y, marker='o', edgecolor='black', linewidth=1, alpha=0.75, s=80, c=
                    color_array1))

    np_array_x = np.array(values.T[0])[defects > defect_limit]
    np_array_y = np.array(values.T[1])[defects > defect_limit]
    scatters.append(ax.scatter(np_array_x, np_array_y, marker='*', edgecolor='black', linewidth=1, alpha=0.75, s=80, c=
                    color_array2))

    #legend1 = ax.legend(*scatters[0].legend_elements(),
                        #                    loc="lower left", title="Good clusters")
    #ax.add_artist(legend1)
    #legend2 = ax.legend(*scatters[1].legend_elements(),
                        #                    loc="upper left", title="Bad clusters")
    #ax.add_artist(legend2)

    # for lable in unique_labels:
    #     col = [0, 0, 0, 1]
    #     if lable.T != -1:
    #         col = colors[lable.T]
    #     np_array = values[(labels == lable) & (defects <= defect_limit)].T  # 75
    #     ax.plot(np_array[0], np_array[1], "o", markerfacecolor=tuple(
    #         col), markeredgecolor="k", markersize=8, )
    #     np_array = np.array(
    #         values[(labels == lable) & (defects > defect_limit)]).T
    #     ax.plot(np_array[0], np_array[1], "*", markerfacecolor=tuple(
    #         col), markeredgecolor="k", markersize=10, )


    annot = ax.annotate("", xy=(0,0), xytext=(5,5), textcoords="offset points")
    annot.set_visible(False)
    def onclick(event):
        for i in range(2):
            if event.inaxes == ax:
                cont, ind = scatters[i].contains(event)
                if cont:
                    annot.xy = (event.xdata, event.ydata)
                    if i == 0:
                        annot.set_text("{}".format(', '.join([str(good_defects[n]) for n in ind["ind"]])))
                    elif i == 1:
                        annot.set_text("{}".format(', '.join([str(bad_defects[n]) for n in ind["ind"]])))
                    annot.set_visible(True)
                    break
                else:
                    annot.set_visible(False)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Estimated number of clusters: %d" % len(unique_colors))
    fig.canvas.mpl_connect("button_press_event", onclick)
    plt.legend()
    plt.show()
    return labels
