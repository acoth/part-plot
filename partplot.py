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
    plt.colorbar(sc)
    ax.grid(which="both")
    #    ax.set_xlabel(xName)
    #    ax.set_ylabel(yName)
    tooltip = mpld3.plugins.PointLabelTooltip(sc, namesm.compressed())
    mpld3.plugins.connect(fig, tooltip)
    return mpld3.fig_to_html(fig, figid="figure")
