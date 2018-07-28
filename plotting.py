#functions for custom plotting

import decimal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import log10, floor, ceil

def ordMag(x):
    """Returns the order of magnitude of a number x,
i.e. 1 for x = 3, 10 for x = 30."""
    return 10**(floor(log10(x)))

def closestMult(x, y):
    """Returns the closest multiple of x by y."""
    return y*((x+y//2)//y)

def drange(start=-10, stop=10, by=.1):
    """Return an object that produces a sequence of float numbers from start
(inclusive) to stop (exclusive) by step. Example: x = list(drange)"""
    while start < stop:
        yield float(start)
        start += decimal.Decimal(by)

def plotGraph(p, start=None, stop=None, xname='x axis', yname='y axis'):
    """Return  the graph of a mathematical function and shows the plot. xrange
should specificy the interval [start,stop] of x values to calculate the y values
of the polynomial function whose constants are in the list "p"."""
    #generate the range of x values
    if start == None or stop == None:
              x = np.linspace(-10,10,200)
    else:
              x = np.linspace(start,stop,num=200)

    #plot data
    y = np.polyval(p, x)

    graph = plt.plot(x,y, zorder =4)
    plt.axhline(y=0, color='lightgrey', lw =.5)
    plt.axvline(x=0, color='lightgrey', lw =.5)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.show()
    return graph

def plotScatter(data, x, y, colorby=None, xlab=None, ylab=None):
    """Plots individual data points as a scatter plot.
data : data frame
x : name of column in data frame plotted on x axis
y : name of column in data frame plotted on y axis
colorby : name of column in data frame, different groups will have
    a different color
xlab : name of x axis
ylab : name of y axis
"""
    col = plt.cm.get_cmap('tab20').colors
    fig, ax = plt.subplots()
    
    if colorby != None:
        i = 0
        while i <  len(set(data[colorby])):
            ax.scatter(x=data[x][data[colorby]==list(set(data[colorby]))[i]],
                   y=data[y][data[colorby]==list(set(data[colorby]))[i]],
                   c=col[i], zorder=4)
            i += 1
        ax.legend(set(data[colorby]))
    else:
        ax.scatter(x=data[x], y=data[y], zorder=4)

    # axes labels
    if xlab == None:
        ax.set_xlabel(x)
    else:
        ax.set_xlabel(xlab)
    if ylab == None:
        ax.set_ylabel(y)
    else:
        ax.set_ylabel(ylab)

    #draw grid
    ax.grid(color=(.9,.9,.9), zorder=0)
    
    plt.show()

def plotFacet(data, x, y, facet=None, xlab=None, ylab=None,
                   style="scatter"):
    """Plots data by separating them according to values specified by facet.
data : data frame
x : name of column of data frame plotted on x axis
y : name of column of data frame plotted on y axis
facet : name of column of data frame containing values serving to group data
into different subplots
type : type of plot (default is scatter)
xlab : name of x axis
ylab : name of y axis
"""
    #extract names corresponding to selected facet
    facet_names = []
    if facet != None:
        for i in data[facet]:
            if i not in facet_names:
                facet_names.append(i)
    else:
        print("Please select a facet name.")
        return #exit function

    #determine the required number of rows for facets
    if len(facet_names) <= 8:
        rows = 2
    elif len(facet_names) <= 12:
        rows = 3
    else:
        print("Too many facets")

    #draw subplots
    cols = 4
    fig, ax = plt.subplots(nrows=rows, ncols=cols, sharex=False, sharey=True)

    #set axes parameters
    #set axes limits and steps
    #for y
    ymini = floor(min(data[y]))
    ymaxi = ceil(max(data[y]))
    if 0 < ymaxi -ymini <= 10:
        ystep = 2
    elif 10 < ymaxi -ymini <= 100:
        ystep = 10
    elif 100 < ymaxi -ymini <= 1000:
        ystep = 100
    ylim_lo = closestMult(ymini, ordMag(ymaxi -ymini)) -ordMag(ymaxi -ymini)
    ylim_hi = closestMult(ymaxi, ordMag(ymaxi -ymini)) +ordMag(ymaxi -ymini)
    plt.ylim(ymin=ylim_lo, ymax=ylim_hi)
    
    #for x
    xmini = floor(min(data[x]))
    xmaxi = ceil(max(data[x]))
    xlim_lo = closestMult(xmini, ordMag(xmaxi -xmini)) -ordMag(xmaxi -xmini)
    xlim_hi = closestMult(xmaxi, ordMag(xmaxi -xmini)) +ordMag(xmaxi -xmini)
    if 0 < xmaxi -xmini <= 10:
        xstep = 2
    elif 10 < xmaxi -xmini <= 100:
        xstep = 10
    elif 100 < xmaxi -xmini <= 1000:
        xstep = 100
    lab_rota = 45 if len(str(data[x][0])) >= 4 else 0
    lab_size = "x-small" if len(str(data[x][0])) >= 4 else "medium"
    x_title_pos = 0.01 if len(str(data[x][0])) >= 4 else 0.04
   
    #draw y ticks on first column and x ticks
    #on all but bottom row
    for irow in range(rows-1):
        ax[irow, 0].set_yticks(list(range(ylim_lo, ylim_hi, ystep)))
        for icol in range(cols):
            ax[irow, icol].set_xlim(xmin=xlim_lo, xmax=xlim_hi)
            ax[irow, icol].set_xticks(list(range(xlim_lo, xlim_hi, xstep)))
            ax[irow, icol].set_xticklabels(list("" for _ in range(xlim_lo, xlim_hi, xstep)))
            
    #draw y ticks (first column only) and x ticks on bottom row
    ax[rows-1, 0].set_yticks(list(range(ylim_lo, ylim_hi, ystep)))
    for icol in range(4):
        ax[rows-1, icol].set_xlim(xmin=xlim_lo, xmax=xlim_hi)
        ax[rows-1, icol].set_xticks(list(range(xlim_lo, xlim_hi, xstep)))
        ax[rows-1, icol].set_xticklabels(list(map(str, range(xlim_lo, xlim_hi, xstep))),
                                         rotation=lab_rota,
                                         size=lab_size)
        
    #draw x ticks labels on overhanging subplot
    for i in range(rows*4 -len(facet_names)):
        ax[rows-2, 4 -1 -i].set_xlim(xmin=xlim_lo, xmax=xlim_hi)
        ax[rows-2, 4 -1 -i].set_xticks(list(range(xlim_lo, xlim_hi, xstep)))
        ax[rows-2, 4 -1 -i].set_xticklabels(list(map(str, range(xlim_lo, xlim_hi, xstep))),
                                        rotation=lab_rota,
                                        size=lab_size)
    
    #draw axes names
    if xlab == None:
        xlab = x
    if ylab == None:
        ylab = y
    fig.text(0.5, x_title_pos, xlab, ha='center')
    fig.text(0.04, 0.5, ylab, va='center', rotation='vertical')

    #draw data and grid
    for i in range(len(facet_names)):
        icol = i%4
        irow = i//4
        ax[irow, icol].grid(color=(.9,.9,.9), zorder=0)
        #plot scatter
        if style == "scatter":
            ax[irow, icol].scatter(x=data[x][data[facet]==facet_names[i]],
                                   y=data[y][data[facet]==facet_names[i]],
                                   s=2,
                                   zorder=3)
        #plot line, does not work with niab weather data for some reason
        if style == "line":
            ax[irow, icol].plot(data[x][data[facet]==facet_names[i]],
                                data[y][data[facet]==facet_names[i]],
                                linewidth=1)
            
        #give a title to each subplot    
        ax[irow, icol].set_title(facet_names[i])
        
    #delete unused subplots
    for i in range(rows*4 -len(facet_names)):
        fig.delaxes(ax[-1,-(i+1)])

    #adjust distance between rows of subplots
    plt.subplots_adjust(hspace=0.3)
   
    plt.show()
