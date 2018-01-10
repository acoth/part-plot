#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:42:38 2017

@author: acoth
"""

from flask import Flask, request, render_template
from numpy import Inf
import partplot
import re

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def page():
    #    retPage = '<html><head><title>Pathfinder Odds Calculator</title></head>\n<body><img src="%s"></body></html>'%'odds.svg'
    if request.method == 'GET':
        params = {'xName': 'GBP (typ)',
                  'yName': 'Iq/Amp (typ)',
                  'cName': 'VNoise Density (typ)',
                  'labelName': 'Part #',
                  'xlim': (1e4, 2e10),
                  'ylim': (1e-9, 0.1),
                  'clim': (1e-10, 1e-7),
                  'xscale': 'log',
                  'yscale': 'log',
                  'cscale': 'log'}
    if request.method == 'POST':
        params = {'xName': request.form['xvar'].encode('utf8'),
                  'yName': request.form['yvar'].encode('utf8'),
                  'cName': request.form['cvar'].encode('utf8'),
                  'labelName': request.form['name'].encode('utf8'),
                  'xlim': (float(request.form['xmin']), float(request.form['xmax'])),
                  'ylim': (float(request.form['ymin']), float(request.form['ymax'])),
                  'clim': (float(request.form['cmin']), float(request.form['cmax'])),
                  'xscale': request.form['xscale'].encode('utf8'),
                  'yscale': request.form['yscale'].encode('utf8'),
                  'cscale': request.form['cscale'].encode('utf8'),
                  }
    #    print params
    return (render_template('page.html',
                            plot=partplot.labelPlot(**params),
                            curr_x=params['xName'], curr_y=params['yName'], curr_c=params['cName'],
                            curr_name=params['labelName'],
                            curr_xsc=params['xscale'], curr_ysc=params['yscale'], curr_csc=params['cscale'],
                            curr_xmin='%1.2g' % params['xlim'][0], curr_xmax='%1.2g' % params['xlim'][1],
                            curr_ymin='%1.2g' % params['ylim'][0], curr_ymax='%1.2g' % params['ylim'][1],
                            curr_cmin='%1.2g' % params['clim'][0], curr_cmax='%1.2g' % params['clim'][1],
                            varnames=partplot.fieldnames, scaleTypes=('linear', 'log')))


app.run(host='0.0.0.0', port=80)
