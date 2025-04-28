# Circuit Level optimizations
The following code attempts to calculate the cost of various circuit-level optimizations that can be applied to Shor's algorithm. Similar to the work done in [[GE21](https://arxiv.org/pdf/1905.09749)] and [[GS23](https://arxiv.org/pdf/2103.06159)].  Will be using the new adder from[[Fed25](https://arxiv.org/pdf/2501.07060)]. 

Directory Overview:

```
C:.
│   LICENSE
│   README.md
│
├───circuits
│   ├───2025
│   │   │   clean.py
│   │   │   compare.py
│   │   │   errorrates(1).csv
│   │   │   errorrates(2).csv
│   │   │   errorratevariation(1).csv
│   │   │   errorratevariation.csv
│   │   │   error_correction.py
│   │   │   estimate.py
│   │   │   estimateoldadder.csv
│   │   │   estimates.csv
│   │   │   estimates1.csv
│   │   │   estimatesupdatednewadder.csv
│   │   │   extraoplate.py
│   │   │   gid+ekera(more).csv
│   │   │   gid+ekera.csv
│   │   │   gou.csv
│   │   │   latexgen.py
│   │   │   openingdata1e3.csv
│   │   │   openingdata1e3wrunway(1).csv
│   │   │   openingdata1e3wrunway.csv
│   │   │   openingdata1e6.csv
│   │   │   params.csv
│   │   │   structures.py
│   │   │   structurespt2.py
│   │   │   tests.py
│   │   │
│   │   └───__pycache__
│   │           clean.cpython-310.pyc
│   │           error_correction.cpython-310.pyc
│   │           structures.cpython-310.pyc
│   │
│   ├───GE2021
│   │   │   estimate_costs.py
│   │   │   estimate_costs_test.py
│   │   │   fill-in-table.py
│   │   │   plot_costs.py
│   │   │   struct.py
│   │   │
│   │   └───__pycache__
│   │           struct.cpython-310.pyc
│   │
│   └───GS21
│       │   cout_shor.py
│       │   error_correction.py
│       │   tools.py
│       │
│       └───__pycache__
│               error_correction.cpython-310.pyc
│               tools.cpython-310.pyc
│
└───graphs
        compare.py
        errorratersa.png
        Figure_2.png
        Figure_3.png
        Figure_4.png
        gammaglm1.png
        glmplotwreg.png
        hoursforeach.png
        qubitsforeach.png
        rsadaysloglogstage3.png
        rsaqubitsloglogstage3.png
        rsavolumeloglog.png
        rsavolumeloglogscaleex.png
        rsavolumeloglogstage1.png
        rsavolumeloglogstage2.png
        rsavolumeloglogstage3.png
        rsavolumenologscaleex.png
        rsavolumexlogscaleex.png
        shorvsgnfs.png
        shorvsgnfs2.png
```


Introductory papers:
1. [[VBE96](https://arxiv.org/pdf/quant-ph/9511018)]
2. [[CDKP-M03](https://arxiv.org/pdf/quant-ph/0410184)]
3. [[Dra00](https://arxiv.org/pdf/quant-ph/0008033)]
4. [[Bea03](https://arxiv.org/pdf/quant-ph/0205095)]
5. [[Gid18](https://arxiv.org/pdf/1709.06648)]
6. [[Gid19](https://arxiv.org/pdf/1905.07682)]
7. [[Zal06](https://arxiv.org/pdf/quant-ph/0601097)]

<b>VERY HELPFUL</b> for surface codes
1. [[FMC12](https://arxiv.org/pdf/1208.0928)]

Currently reading:
1. [[Gid19](https://arxiv.org/pdf/1905.08488)]
3. [[Zal98](https://arxiv.org/pdf/quant-ph/9806084)]

