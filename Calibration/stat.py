#!/usr/bin/env python3
# ----------------------------------------- #
# stat.py
# ----------------------------------------- #
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
#
# read data and drop unwanted rows and columns
try:
    df = pd.read_csv('fort.9',delim_whitespace = True,
        names=["time","CFL","fx1","fy1","m1","p1","fx2","fy2","m2","p2"])
except FileNotFoundError:
    exit('stat: fort.9 not found')
df.drop(df.index[:3], inplace=True)

try:
    mg = pd.read_csv('fort.8',delim_whitespace = True,
        names=["itr","res0","res","inf"])[2:]
except FileNotFoundError:
    exit('stat: fort.8 not found')
#
# -- plot PDF pages
def str_rnd(num,d=4): return str(round(num,d))

def plot_hist(pdf,name,label):
    ax = df.plot(x='time',y=name,figsize=(8,4))
    plt.xlabel(r'$t/T$', fontsize=12)
    plt.ylabel(label, fontsize=12)
    mean,mad = df[name].mean(), 1.5748*df[name].mad()
    x1,x2,y1,y2 = plt.axis()
    mx,mn = min(y2,mean+3*mad),max(y1,mean-3*mad)
    plt.ylim([mn,mx])
    txt = 'mean='+str_rnd(mean)+', mad='+str_rnd(mad)
    plt.text(0.5,0.01,txt,transform=ax.transAxes)
    pdf.savefig()
    plt.close()

with PdfPages('history.pdf') as pdf:
    plot_hist(pdf,name='fx1',label=r'$C_{X,1}$')
    plot_hist(pdf,name='fy1',label=r'$C_{Y,1}$')
    plot_hist(pdf,name='m1' ,label=r'$C_{M,1}$')
    plot_hist(pdf,name='p1' ,label=r'$C_{P,1}$')
    plot_hist(pdf,name='fx2',label=r'$C_{X,2}$')
    plot_hist(pdf,name='fy2',label=r'$C_{Y,2}$')
    plot_hist(pdf,name='m2' ,label=r'$C_{M,2}$')
    plot_hist(pdf,name='p2' ,label=r'$C_{P,2}$')
    plot_hist(pdf,name='CFL',label=r'$\frac{\Delta t U}{\Delta x}$')

    mg.plot(y=['res0','res','inf'],figsize=(8,4))
    plt.yscale('log')
    pdf.savefig()

    mg.plot(y='itr',figsize=(8,4))
    pdf.savefig()
