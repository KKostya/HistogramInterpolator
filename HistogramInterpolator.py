import ROOT
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate,sqrt


def mynorm(x1, x2):
    return sqrt((x1[0]+x1[1]-x2[0]-x2[1])**2+10*(x1[0]-x1[1]-x2[0]+x2[1])**2)

class Interpolator:
    def __init__(self, setup):
        data = []
        setup.sort(key=lambda x: x['mass'])
        for mp in setup:
            tfile = ROOT.TFile(mp['file'])
            hist  = tfile.Get(mp['name']) 
            if(hist.GetNbinsX() == 1):
                data += [(hist.GetBinCenter(1),mp['mass'],hist.GetBinContent(1))]
            else:
                data += [(hist.GetBinCenter(i),mp['mass'],hist.GetBinContent(i)) for i in range(hist.GetNbinsX()+2)]
            tfile.Close()
        x,y,z = [np.array(d) for d in zip(*data)]
        self.spline = interpolate.Rbf(x,y,z,epsilon=10,function='quintic', norm = mynorm)
        self.minx,self.maxx = min(x),max(x)
        self.miny,self.maxy = min(y),max(y)

    def MakePlot(self, title, plotfile):
        XI, YI = np.meshgrid( np.linspace(self.minx,self.maxx,100),
                              np.linspace(self.miny,self.maxy,100))
        ZI = self.spline(XI, YI)

        fig = plt.figure()
        plt.contourf(XI, YI, ZI, 8,alpha=.75,cmap=cm.jet)
        C = plt.contour(XI, YI, ZI, 8,colors='black', linewidth=.5)
        plt.clabel(C, inline=1, fontsize=8, fmt = '%1.1f')
        plt.title(title)
        plt.xlabel("Histogram bin")
        plt.ylabel("Mass point")
        plt.axes().set_aspect('equal', 'datalim')
        plt.savefig(plotfile,bbox_inches='tight',pad_inches=0.0)

    def FillHists(self,setup):
        ints = {}
        for mp in setup:
            tfile = ROOT.TFile(mp['file'],"UPDATE")
            hist  = tfile.Get( mp['clone']) 
            newH  = hist.Clone(mp['name']) 
            if newH.GetNbinsX()==1:
                x = hist.GetBinCenter(1)
                z = self.spline(x,mp['mass'])
                newH.SetBinContent(1,z if z > 0 else 0) 
            else:
                for i in range(newH.GetNbinsX()+2):
                    x = hist.GetBinCenter(i)
                    z = self.spline(x,mp['mass'])
                    newH.SetBinContent(i,z if z > 0 else 0) 
            newH.Write()
            ints[mp["mass"]] = newH.Integral()
            tfile.Close()
        return ints 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Histograms interpolator.')
    parser.add_argument('setupJson',  help='*.json file, containing detailed info on mass point histograms')
    parser.add_argument('--srcroot', dest= 'srcFile',default="",help='ROOT file, containing source histograms.')
    parser.add_argument('--dstroot', dest= 'dstFile',default="",help='ROOT file to write interpolated histograms. (will use srcRoot if not provided)')
    parser.add_argument('--plot',    dest='plotFile',default="",help='File for 2d spline plot.')
    parser.add_argument('--ratejson',dest='rateFile',default="",help='Json file to store integrals of the produced histograms')
    args = parser.parse_args()

    with open(args.setupJson,"r") as jsonF:
        jsonData = json.load(jsonF,"ascii")

    if ("src" not in jsonData) or ("dst" not in jsonData): 
        raise Exception("Top level of the json file should contain \"src\" and \"dst\" keys.")

    setupSrc = jsonData['src']
    # Processing/Checking src setup
    for mp in setupSrc:
        if ("name" not in mp) or ("mass" not in mp): raise Exception("\"src\" json entries must contain \"mass\" and \"name\" keys.")
        if "file" not in mp: 
            if not args.srcFile: raise Exception("Need source root file either in json or as a parameter.")
            mp["file"] = args.srcFile
        
    setupDst = jsonData['dst']
    # Processing/Checking dst setup
    for mp in setupDst:
        if ("name" not in mp) or ("mass" not in mp) or ("clone" not in mp): 
            raise Exception("\"dst\" json entries must contain \"mass\", \"name\" and \"clone\" keys.")
        if "file" not in mp: 
            if not args.srcFile: raise Exception("Cannot deduce destination ROOT filename.")
            mp["file"] = args.dstFile if args.dstFile else args.srcFile
        
    itp = Interpolator(setupSrc)
    if args.plotFile: itp.MakePlot("",args.plotFile)
    rates = itp.FillHists(setupDst)
    if args.rateFile:
        with open(args.rateFile, "w") as jswrite:
             json.dump(rates,jswrite,sort_keys=True,indent=4, separators=(',', ': '))



