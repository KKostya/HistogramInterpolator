HistogramInterpolator
=====================

Python script for interpolating 1D histograms in ROOT files.

# Usage

    HistogramInterpolator.py setup.json --srcroot source.root --dstroot destination.root
    
## Json structure
Example of json setup file:    

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
* `src` with information of source histograms to base interpolation on
    + `mass` gives the value for the mass
    + `name` entry is a key of the `TH1` in the source root file 
    + `file` is an optional entry that gives you an alternative way to set a source file 
* `dst` with data on the histograms that should be created
    + `mass` gives the value for the mass to find interpolated histogram at
    + `name` entry gives a name for the histogram to write
    + `clone` mandatory entry that provides the prototype `TH1` in the destination file
    + `file` is an optional entry that gives you an alternative way to set a destination file 
