HistogramInterpolator
=====================

Python script for interpolating 1D histograms in ROOT files.

# Usage

    HistogramInterpolator.py setup.json --srcFile source.root
    
## Json structure
    
    { "src": 
      [ { "mass": 230.0, "name": "VBF_230" },
        { "mass": 250.0, "name": "VBF_250" },
        .....
        { "mass": 650.0, "name": "VBF_650" } ],
    "dst": 
      [ { "clone": "VBF_230", "mass": 232.0, "name": "VBF_232" },
        { "clone": "VBF_230", "mass": 234.0, "name": "VBF_234" },
        ..... ]
    }
