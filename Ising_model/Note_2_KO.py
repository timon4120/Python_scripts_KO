import argparse
import numpy as np
import random as rd
import rich
import rich.progress
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as c
from matplotlib.animation import FuncAnimation
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

# def animate(i):
#     im = plt.imread('Step_'+str(i)+'.png')
#     plt.imshow(im)

class Ising():
    def __init__(self,n,J,beta,B,steps,dens):
        self.n = n
        self.J = J
        self.beta = beta
        self.B = B
        self.steps = steps
        self.dens = dens
        self.matrix = np.random.choice([1,-1],size = (self.n,self.n), p = [self.dens,1-self.dens])
        self.XD2 = np.c_[self.matrix[:,-1],self.matrix,self.matrix[:,0]]
        self.XD2 = np.r_[[self.XD2[-1,:]],self.XD2,[self.XD2[0,:]]]
        self.M = []
        self.gr = []
    
    def Get_E(self,x,y,mark = 1):
        xx, yy = np.indices(self.XD2.shape)
        mask = np.hypot(xx - x - 1, yy - y - 1) == 1
        if mark != 1: self.matrix[x,y] *= -1
        neighbourhood = -self.J * np.sum(self.matrix[x,y] * self.XD2[mask])
        field = -self.B * np.sum(self.matrix)
        return neighbourhood + field

    def Simulation(self,step_tit,anim_tit):
        for step in rich.progress.track(range(self.steps)):
            for i in range(self.n * self.n):
                x,y = np.random.randint(self.n, size = 2)
                E_0 = self.Get_E(x,y)
                E_1 = self.Get_E(x,y,-1)
                delta = E_1 - E_0
                if delta < 0: pass#self.matrix[x,y] *= -1
                else:
                    if rd.uniform(0,1) >= np.exp(-self.beta * delta): self.matrix[x,y] *= -1
            if step_tit != None: self.Print_Grid(step,np.mean(self.matrix),step_tit)
            self.gr.append(np.flip(self.matrix.copy(),0))
            self.M.append(np.mean(self.matrix))
        if anim_tit != None: 
            self.Animate_Grid(anim_tit)
    
    def Get_Magnetization(self):
        return np.arange(0,self.steps), self.M
    
    def Print_Grid(self,i,mm, title):
        plt.rcParams['font.size'] = 16
        cMap = c.ListedColormap(['darkred','darkgreen'])
        plt.figure(figsize = (15,15))
        plt.pcolormesh(np.flip(self.matrix,0),cmap=cMap)
        plt.xticks(np.arange(self.n))
        plt.yticks(np.arange(self.n))
        plt.plot([],[], color = 'darkgreen', label = r'$s_{i} = \uparrow$')
        plt.plot([],[], color = 'darkred', label = r'$s_{i} = \downarrow$')
        plt.legend(bbox_to_anchor=(1, 1.1))
        plt.title(f'Model Isinga \n Siatka: {self.n}x{self.n}  | Krok czasowy: {i} | Magnetyzacja: {round(mm,3)} \n Kamil Orzechowski')
        plt.grid(which='major', alpha=0.5)
        plt.savefig(f'{title}_{i}.png')
        plt.close()

    def animate2(self,i):
        self.cMap = c.ListedColormap(['darkred','darkgreen'])
        plt.title(f'Model Isinga \n Siatka: {self.n}x{self.n}  | Krok czasowy: {i} \n Kamil Orzechowski')
        plt.pcolormesh(self.gr[i],cmap=self.cMap)
        
    def Animate_Grid(self,title):
        nframes = self.steps
        self.fig = plt.figure(figsize = (15,15))
        plt.rcParams['font.size'] = 16
        plt.xticks(np.arange(self.n))
        plt.yticks(np.arange(self.n))
        plt.plot([],[], color = 'darkgreen', label = r'$s_{i} = \uparrow$')
        plt.plot([],[], color = 'darkred', label = r'$s_{i} = \downarrow$')
        plt.legend(bbox_to_anchor=(1, 1.1))
        
        self.anim = FuncAnimation(self.fig, self.animate2, frames=nframes, interval=(10000.0/nframes))
        self.anim.save(f'{title}.gif', writer='pillow')

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("-n", default = 10)
    argp.add_argument("-j", default = 1)
    argp.add_argument("-b", default = 0.4)
    argp.add_argument("-B", default = 1)
    argp.add_argument("-s", default = 10)
    argp.add_argument("-d", default = 0.5)
    argp.add_argument("--stepimage")
    argp.add_argument("--gridanimation")
    argp.add_argument("--magnetization")
    args = argp.parse_args()
    model = Ising(int(args.n),float(args.j),float(args.b),float(args.B),int(args.s),float(args.d))
    print("Start")
    model.Simulation(args.stepimage,args.gridanimation)
    print("Koniec")
    if args.magnetization != None:
        t, m = model.Get_Magnetization()
        DF = pd.DataFrame({"t" : t, "M" : m})
        DF.to_csv(f"{args.magnetization}.txt", index = False)
        plt.figure(figsize=(15,10))
        plt.title("Magnetyzacja w funkcji kroku czasowego")
        plt.ylabel("M(t)")
        plt.xlabel("t")
        _ = plt.plot(t,m, color = "violet")
        # plt.ylim(0,1)
        plt.savefig(f"{args.magnetization}.png")

if __name__ == '__main__':
    main()