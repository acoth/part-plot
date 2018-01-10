import numpy as np
import matplotlib.pyplot as plt
import mpld3
import json

with open('oap.json')as dataFile:
    oap = json.load(dataFile)

fieldnames = oap.keys()


def labelPlot(xName, yName, labelName='Part #', **kwargs):
    plt.ioff()

    cmap = plt.cm.plasma
    x = np.array(oap[xName])
    y = np.array(oap[yName])
    c = np.array(oap.get(kwargs.get('cName', None), np.zeros(np.shape(x))))
    names = oap.get(labelName, 'Part #')

    xscale = kwargs.get('xscale', 'linear')
    yscale = kwargs.get('yscale', 'linear')
    cscale = kwargs.get('cscale', 'linear')

    xlim = kwargs.get('xlim', (0, np.Inf) if xscale == 'log' else (-np.Inf, np.Inf))
    ylim = kwargs.get('ylim', (0, np.Inf) if yscale == 'log' else (-np.Inf, np.Inf))
    clim = kwargs.get('clim', (0, np.Inf) if cscale == 'log' else (-np.Inf, np.Inf))

    mask = np.array(kwargs.get('mask', np.array([False] * np.shape(x)[0]))) | (x <= xlim[0]) | (x > xlim[1]) | (
            y <= ylim[0]) | (y > ylim[1]) | (c <= clim[0]) | (c > clim[1])
    xm = np.ma.masked_array(x, mask)
    ym = np.ma.masked_array(y, mask)
    cm = np.ma.masked_array(c, mask)
    sm = np.ma.masked_array(kwargs.get('s', 17 * np.ones(np.shape(x))), mask)
    namesm = np.ma.masked_array(names, mask)

    xp = np.log10(xm) if xscale == "log" else xm
    yp = np.log10(ym) if yscale == "log" else ym
    cp = np.log10(cm) if cscale == "log" else cm

    fig, ax = plt.subplots()

    sc = ax.scatter(xp, yp, c=cp, s=sm, cmap=cmap)
    sc.set_clim(np.min(cp), np.max(cp))
    cb = plt.colorbar(sc)
    if xscale == "log":
        majorTicks = np.arange(np.floor(np.min(xp)), np.ceil(np.max(xp)) + 1)
        minorTicks = np.concatenate([np.log10(range(1, 10 if x != majorTicks[-1] else 2)) + x for x in majorTicks])
        ax.set_xticks(minorTicks)
        ax.set_xticklabels([engLabel(x) if x in majorTicks else "" for x in minorTicks])
    if yscale == "log":
        majorTicks = np.arange(np.floor(np.min(yp)), np.ceil(np.max(yp)) + 1)
        minorTicks = np.concatenate([np.log10(range(1, 10 if x != majorTicks[-1] else 2)) + x for x in majorTicks])
        ax.set_yticks(minorTicks)
        ax.set_yticklabels([engLabel(x) if x in majorTicks else "" for x in minorTicks])
    if cscale == "log":
        majorTicks = np.arange(np.floor(np.min(cp)), np.ceil(np.max(cp)) + 1)
        minorTicks = np.concatenate([np.log10(range(1, 10 if x != majorTicks[-1] else 2)) + x for x in majorTicks])
        print minorTicks
        cb.set_ticks(minorTicks)
        cb.set_ticklabels([engLabel(x) if x in majorTicks else "" for x in minorTicks])
    sc.set_clim(np.min(minorTicks), np.max(minorTicks))
    ax.grid(which="both")
    #    ax.set_xlabel(xName)
    #    ax.set_ylabel(yName)
    tooltip = mpld3.plugins.PointLabelTooltip(sc, namesm.compressed())
    mpld3.plugins.connect(fig, tooltip)
    return mpld3.fig_to_html(fig, figid="figure")


def engLabel(number):
    d = 3 * np.floor(number / 3)
    r = number - d
    rstr = "%1.3g" % np.power(10, r)
    unitTable = {0: "",
                 3: "k",
                 6: "M",
                 9: "G",
                 12: "T",
                 15: "P",
                 -3: "m",
                 -6: "u",
                 -9: "n",
                 -12: "p",
                 -15: "f",
                 -18: "a"}
    return rstr + unitTable.get(d, '?')
