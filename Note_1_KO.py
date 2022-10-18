import argparse
from collections import Counter as ctr
from ascii_graph.colordata import vcolor
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
import string
import random as rd

"""
Task 1 Basic : Kamil Orzechowski
Exec: python main.py <sourcefile_name>
Flags:
-n : min. number of word to print (optional)
-l : min. length of word to print (optional)
"""

patterns = [Red,Gre,Yel,Blu,Pur,Cya,Whi]

def do_primitive_histo(file, N, N_w):
	global patterns
	with open(file,"r",encoding="utf-8") as f: data = f.read()#.lower()
	data = data.translate(str.maketrans('', '', string.punctuation))
	hist = list(ctr(data.split()).items())
	hist = sorted(hist,key=lambda x: x[1],reverse = True)
	hist = list(filter(lambda w: len(w[0]) >= N_w,hist))
	graph = Pyasciigraph()
	data = vcolor(hist[:N], rd.choices(patterns,k=N))
	for line in graph.graph(f" Tribal histo of Animal Farm novel | Words: {N} | Min. length: {N_w}",data): print(line)

if __name__ == '__main__':
	argp = argparse.ArgumentParser()
	argp.add_argument("filename")
	argp.add_argument("-n","--numb_of_words", default = 10)
	argp.add_argument("-l","--len_of_words", default = 0)
	args = argp.parse_args()
	do_primitive_histo(args.filename,int(args.numb_of_words),int(args.len_of_words))
	