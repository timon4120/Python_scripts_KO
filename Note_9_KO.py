import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import Slider, Div, ColumnDataSource
from bokeh.layouts import row, column

N = 10000
S_0 = 9999
I_0 = N - S_0
R_0 = 0
y_0 = S_0,I_0,R_0
b = 0.78
y = 0.12
t = np.linspace(0,60,100)

def SIR(y,t,N,beta,gamma):
    S,I,R = y
    SS = -beta*S*I/N
    II = beta*I*S/N-gamma*I
    RR = gamma*I
    return SS,II,RR

results = odeint(SIR, y_0, t, (N,b,y))
XX = pd.DataFrame({"t" : t, "S" : list(results[:,0]), "I" : list(results[:,1]), "R" : list(results[:,2])})
source = ColumnDataSource(XX)

fig = figure(x_axis_label = "t", y_axis_label = "(S|I|R)(t)", width = 1200, aspect_ratio = 2)
fig.line("t","S", color = "green", line_width = 3, source=source)
fig.line("t","I", color = "gold", line_width = 3, source=source)
fig.line("t","R", color = "red", line_width = 3, source=source)

def Update_alpha(attr,old,new):
    global y
    y = new
    results = odeint(SIR, y_0, t, (N,b,y))
    XXX = pd.DataFrame({"t" : t, "S" : list(results[:,0]), "I" : list(results[:,1]), "R" : list(results[:,2])})
    source.data = ColumnDataSource.from_df(XXX)

def Update_beta(attr,old,new):
    global b
    b = new
    results = odeint(SIR, y_0, t, (N,b,y))
    XXX = pd.DataFrame({"t" : t, "S" : list(results[:,0]), "I" : list(results[:,1]), "R" : list(results[:,2])})
    source.data = ColumnDataSource.from_df(XXX)

fig.toolbar.autohide = True
slid_a = Slider(start = 0, end = 1, step = 0.02, value = 0.12, title = "Alpha")
slid_b = Slider(start = 0, end = 1, step = 0.02, value = 0.78, title = "Beta")
slid_a.on_change("value",Update_alpha)
slid_b.on_change("value",Update_beta)

curdoc().theme = 'night_sky'
curdoc().add_root(row(column(Div(text = "<b>Model SIR</b>", align = "center"),slid_a,slid_b),fig))