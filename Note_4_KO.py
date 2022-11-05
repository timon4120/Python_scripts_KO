import requests
from bs4 import BeautifulSoup
import argparse
import json
import matplotlib.pyplot as plt

"""
Kamil Orzechowski
Exec: python Note_4_KO.py 
Flags:
-n : output .json filename
-f : The Sejm MPS' ditribution filename. Shows pie chart with parties' distribution. If you dont't use the flag, nothing will happen.
"""

def Get_Sejm():
    req = requests.get("https://www.sejm.gov.pl/Sejm9.nsf/kluby.xsp")
    soup = BeautifulSoup(req.text, "html.parser")
    parties = soup.find("ul", {"class":"partie"})
    parties_info = {}

    for party in parties.find_all("li"):
        name = party.find("a").find("h3")
        if name == None: name = party.find("h3")
        MPS_number = party.find("p").find("a")
        parties_info.update({name.text : int(MPS_number.text.split()[0])})
    
    return parties_info
 
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("--filename", default = "output")
    argp.add_argument("--canva", default = None)
    args = argp.parse_args()
    parties = Get_Sejm()

    with open(f"{args.filename}.json","w") as f:
        json.dump(parties,f) 
    
    if args.canva != None:
        plt.figure(figsize=(20,10))
        plt.title("Rozkład mandatów w polskim Sejmie")
        plt.axis("equal")
        w,t = plt.pie(parties.values(), labels=parties.keys(), explode=[0.05]*len(parties))
        plt.legend(w, parties.values())
        plt.savefig(f"{args.canva}.png")

if __name__ == '__main__':
    main()
