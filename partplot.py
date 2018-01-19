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
    try:
        d = c + 1
    except:
        d = list(set(c))
        d.sort()
        c = np.array(map(lambda x: d.index(x), c))

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

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=128)

    sc = ax.scatter(xp, yp, c=cp, s=sm, cmap=cmap, alpha=0.7)
    sc.set_clim(np.min(cp), np.max(cp))
    cb = plt.colorbar(sc)
    if xscale == "log":
        xMinorTicks, xMinorTickLabels = logTicks(np.min(xp), np.max(xp))
        ax.set_xticks(xMinorTicks)
        ax.set_xticklabels(xMinorTickLabels)
    if yscale == "log":
        yMinorTicks, yMinorTickLabels = logTicks(np.min(yp), np.max(yp))
        ax.set_yticks(yMinorTicks)
        ax.set_yticklabels(yMinorTickLabels)
    if cscale == "log":
        cMinorTicks, cMinorTickLabels = logTicks(np.min(cp), np.max(cp))
        cb.set_ticks(cMinorTicks)
        cb.set_ticklabels(cMinorTickLabels)
        sc.set_clim(np.min(cMinorTicks), np.max(cMinorTicks))
    ax.grid(which="both")
    #    ax.set_xlabel(xName)
    #    ax.set_ylabel(yName)
    tooltip = mpld3.plugins.PointLabelTooltip(sc, namesm.compressed())
    mpld3.plugins.connect(fig, tooltip)
    return mpld3.fig_to_html(fig, figid="figure")


def logTicks(lower, upper):
    lli = np.floor(lower)
    llf = np.floor(np.power(10, lower - lli))
    uli = np.floor(upper)
    ulf = np.ceil(np.power(10, upper - uli))
    if lli == uli:
        ticks = lli + np.log10(np.arange(llf, ulf + 1))
    else:
        firstPart = lli + np.log10(np.arange(llf, 10))
        middle = np.concatenate([np.log10(np.arange(1, 10)) + x for x in np.arange(lli + 1, uli)])
        lastPart = uli + np.log10(np.arange(1, ulf + 1))
        ticks = np.concatenate((firstPart, middle, lastPart))
    labels = [engLabel(x) if x.is_integer() else "" for x in ticks]
    labels[0] = engLabel(ticks[0])
    labels[-1] = engLabel(ticks[-1])
    return (ticks, labels)

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
