<div style="float:left;margin:0 10px 10px 0" markdown="1">
    
    test
    test
    test
    
</div>

HistogramInterpolator
=====================

Python script for interpolating 1D histograms in ROOT files.

# Requirements

* [PyROOT](http://root.cern.ch/drupal/content/pyroot)
* [SciPy](http://www.scipy.org/)
* [Matplotlib](http://matplotlib.org/)

#### Note for CMS people @ lxplus 
It almost works out of the box with recent CMMSW >= 6 distributions, 
the only problem is the error with `dateutil.rrule` import for matplotlib.
The simplest solution is to get the correct package into the script directory:

     wget http://niemeyer.net/download/python-dateutil/python-dateutil-1.5.tar.gz
     tar xvvf python-dateutil-1.5.tar.gz
     cp -r ./python-dateutil-1.5/dateutil/ .
     rm -rf python-dateutil-1.5
     rm python-dateutil-1.5.tar.gz

# Usage

    HistogramInterpolator.py setup.json --srcroot source.root --dstroot destination.root
    
## Json structure
The information about (existing/required) histograms is provided by means of a [json](http://en.wikipedia.org/wiki/JSON) setup file.
Here is an example of it:    

    { 
    "src": 
      [ { "mass": 230.0, "name": "VBF_230" },
        { "mass": 250.0, "name": "VBF_250" },
        .....
        { "mass": 650.0, "name": "VBF_650" } ],
    "dst": 
      [ { "clone": "VBF_230", "mass": 232.0, "name": "VBF_232" },
        { "clone": "VBF_230", "mass": 234.0, "name": "VBF_234" },
        ..... ]
    }
    
It should contain two sections: 
* `src` provides information on source histograms:
    + `mass` gives the value for the mass
    + `name` entry is a key of the `TH1` in the source root file 
    + `file` is an optional entry that gives you an alternative way to set a source file 
* `dst` contains information on histograms that should be created:
    + `mass` gives the value for the mass, where the interpolated histogram should be produced
    + `name` is a name of the new histogram
    + `clone` mandatory entry that provides the prototype `TH1` object in the destination file. From that object the script learns how many bins one needs in the resulting histogram.
    + `file` is an optional entry that gives you an alternative way to set a destination file 

## Extra outputs
* Using `--plot plotname.pdf` argument you are able to ask the script to make a 2D contour plot of the spline, used in interpolation. Useful when you want to see how good the interpolation is.
* With the `--ratejson rate.json` argument the script creates anothe json file with integrals of the produced histograms. It could be useful for some batch processing.
