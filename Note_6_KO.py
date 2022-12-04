import argparse
import numpy as np
import random as rd
import rich
import time
import rich.progress
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as c
from matplotlib.animation import FuncAnimation
import numba as nb
from numba import njit
import matplotlib
matplotlib.use('Agg')

"""
Kamil Orzechowski
Exec: python Note_2_KO.py 
Flags:
-n : shape of grid (n)x(n)
-j : exchange integral
-b : beta = 1/kT (k - Boltzmann constant | T - temperature)
-B : magnetic induction value
-s : number of steps
-d : spin's density (def = 50%) 
--stepimage : returns grid figure for every step as PNG file. If you dont't use the flag, the file won't be created as well as in two next cases.
--gridanimation : returns a GIF file with animation
--magnetization : return a TXT file with 2 columns - timestep and magnetization
"""
@njit
def Get_Magnetization(steps,M):
    return np.arange(0,steps), M

def Print_Grid(i,mm,title,matrix,n):
    plt.rcParams['font.size'] = 16
    cMap = c.ListedColormap(['black','white'])
    plt.figure(figsize = (15,15))
    plt.pcolormesh(np.flip(matrix,0),cmap=cMap)
    plt.xticks(np.arange(n))
    plt.yticks(np.arange(n))
    plt.plot([],[], color = 'white', label = r'$s_{i} = \uparrow$')
    plt.plot([],[], color = 'black', label = r'$s_{i} = \downarrow$')
    plt.axis("off")
    plt.legend(bbox_to_anchor=(1, 1.1))
    plt.title(f'Ising Model \n Lattice: {n}x{n}  | Timestep: {i} | Magnetization: {round(mm,3)} \n Kamil Orzechowski')
    plt.grid(which='major', alpha=0.5)
    plt.savefig(f'{title}_{i}.png')
    plt.close()

def animate2(i,gr,n,J,T,B,dens,M):
    cMap = c.ListedColormap(['black','white'])
    plt.title(f'Ising Model \n N: {n} | J: {J} | T: {T} | B: {B} | Dens: {dens} | t: {i} | M: {round(M[i],2)} \n Kamil Orzechowski')
    plt.pcolormesh(gr[i],cmap=cMap)
    
def Animate_Grid(title,steps,n,gr,J,T,B,dens,M):
    nframes = steps
    fig = plt.figure(figsize = (15,15))
    plt.rcParams['font.size'] = 16
    plt.xticks(np.arange(n))
    plt.yticks(np.arange(n))
    plt.axis("off")
    plt.plot([],[], color = 'white', label = r'$s_{i} = \uparrow$')
    plt.plot([],[], color = 'black', label = r'$s_{i} = \downarrow$')
    plt.legend(bbox_to_anchor=(1, 1.1))
    anim = FuncAnimation(fig, animate2, frames=nframes, fargs=(gr,n,J,T,B,dens,M,), interval=(1000.0/nframes))
    anim.save(f'{title}.gif', writer='pillow')


@njit
def Get_E(mtx,n,J,B,x,y,mark = 1):
    temp_x = x+1
    temp_y = y+1
    if x == n -1: temp_x = 0 
    if y == n -1: temp_y = 0 
    if mark != 1: mtx[x,y] *= -1 
    neig = np.array([mtx[temp_x,y],mtx[x,temp_y],mtx[x-1,y],mtx[x,y-1]])
    neighbourhood = -J * np.sum(neig) * mtx[x,y]
    field = -B * np.sum(mtx)
    return neighbourhood + field

@njit
def fors(matrix,T,n,J,B):
    for i in range(n * n):
        mtxx = np.copy(matrix)
        x = np.random.randint(n)
        y = np.random.randint(n)
        E_0 = Get_E(mtxx,n,J,B,x,y)
        E_1 = Get_E(mtxx,n,J,B,x,y,-1)
        delta = E_1 - E_0
        if delta < 0: 
            matrix[x,y] *= -1
        elif rd.uniform(0,1) < np.exp(-1/T * delta): 
            matrix[x,y] *= -1


def Simulation(steps,matrix,n,M,T,J,B,gr,step_tit,anim_tit,dens):
    for step in rich.progress.track(range(steps)):
        fors(matrix,T,n,J,B)
        if step_tit != None: Print_Grid(step,np.mean(matrix),step_tit,matrix,n)
        if anim_tit != None: gr.append(np.flip(np.copy(matrix),0))
        M[step] = np.mean(matrix)
    if anim_tit != None: 
        Animate_Grid(anim_tit,steps,n,gr,J,T,B,dens,M)

def Ising(n,J,T,B,steps,dens,step_tit,anim_tit,magn):
    matrix = np.random.choice([1,-1],size = (n,n), p = [dens,1-dens])
    M = np.zeros(steps)
    gr = []
    Simulation(steps,matrix,n,M,T,J,B,gr,step_tit,anim_tit,dens)
    if magn != None: return M


def main():
    # start = time.time()
    argp = argparse.ArgumentParser()
    argp.add_argument("-n", default = 10)
    argp.add_argument("-j", default = 1)
    argp.add_argument("-T", default = 0.4)
    argp.add_argument("-B", default = 1)
    argp.add_argument("-s", default = 10)
    argp.add_argument("-d", default = 0.5)
    argp.add_argument("--stepimage")
    argp.add_argument("--gridanimation")
    argp.add_argument("--magnetization")
    args = argp.parse_args()

    print("Start")
    mgn = Ising(int(args.n),float(args.j),float(args.T),float(args.B),int(args.s),float(args.d),args.stepimage,args.gridanimation,args.magnetization)
    print("Stop")
    
    # stop = time.time()
    # print("Time: ", round(stop-start,2))

    #Time of single algorithm execution: 25.11 sec -> (13x faster with Numba) for -n 250 -j 1 -T 2 -B 0 -s 110 -d 0.5
    #Time of full script execution: 123.51 sec for -n 100 -j 1 -T 1 -B 0 -s 60 -d 0.5

    if args.magnetization != None:
        t, m = Get_Magnetization(int(args.s),mgn)
        DF = pd.DataFrame({"t" : t, "M" : m})
        DF.to_csv(f"{args.magnetization}.txt", index = False)
        plt.figure(figsize=(15,10))
        plt.title(f"Magnetization as timestep function | B = {args.B}")
        plt.ylabel("M(t)")
        plt.xlabel("t")
        _ = plt.plot(t,m, color = "violet")
        # plt.ylim(0,1)
        plt.savefig(f"{args.magnetization}.png")
    

if __name__ == '__main__':
    main()