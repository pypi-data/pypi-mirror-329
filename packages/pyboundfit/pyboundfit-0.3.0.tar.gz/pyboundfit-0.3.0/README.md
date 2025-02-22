# pyboundfit

Boundary fits using polynomials or splines, based on the method described in
[Cardiel 2009](https://ui.adsabs.harvard.edu/abs/2009MNRAS.396..680C/abstract).
This code is a Python implementation of part of the functionality
implemented in the original Fortran 77 code [boundfit](https://github.com/nicocardiel/boundfit).

The numerical minimization of the fit to splines is performed with the help of the package [lmfit](https://lmfit.github.io/lmfit-py/).

*Warning: this code is under development. Major changes are still being introduced.*

## Instaling the code

In order to keep your Python installation clean, it is highly recommended to 
first build a specific Python 3 *virtual enviroment*

### Creating and activating the Python virtual environment

```shell
$ python3 -m venv venv_pyboundfit
$ . venv_pyboundfit/bin/activate
(venv_pyboundfit) $ 
```

### Installing the package

The latest stable version is available via de [PyPI repository](https://pypi.org/project/pyboundfit/):

```shell
(venv_pyboundfit) $ pip install pyboundfit
```
**Note**: This command can also be employed in a Windows terminal opened through the 
``CMD.exe prompt`` icon available in Anaconda Navigator.

The latest development version is available through [GitHub](https://github.com/nicocardiel/pyboundfit):

```shell
(venv_pyboundfit) $ pip install git+https://github.com/nicocardiel/pyboundfit.git@main#egg=pyboundfit
```

### Testing the installation

```shell
(venv_pyboundfit) $ pip show pyboundfit
```

```shell
(venv_pyboundfit) $ ipython
```
```python
In [1]: import pyboundfit

In [2]: print(pyboundfit.__version__)
0.3.0

In [3]: pol1, pol2, spl1, spl2 = pyboundfit.demo()
Computing upper boundary (polynomial fit)... OK!
Computing lower boundary (polynomial fit)... OK!
Computing upper boundary (splines fit)... OK!
Computing lower boundary (splines fit)... OK!

In [4]: pol1.coef
Out[4]: 
array([  22.43919975,  -41.5216713 ,   -7.32451917,  140.23297889,
         41.59855497, -148.66578342])
...
```

The demo function computes the boundary fits to some example data and
generates the following plot:
![pyboundfit demo plot](https://guaix.fis.ucm.es/~ncl/pyboundfit/pyboundfit_example.png)

## Usage

Import the required packages
```python
import matplotlib.pyplot as plt
import numpy as np
import pyboundfit as bf
```

Generate some random data to be fitted
```python
npoints = 300
rng = np.random.default_rng(seed=1234)
xfit = np.linspace(1.0, 3.5, npoints)
yfit = np.sin(xfit) + rng.normal(loc=0, scale=0.1, size=npoints)
```

Fit upper and lower boundaries using polynomials
```python
pol_upper = bf.boundfit_poly(
    x=xfit, y=yfit, deg=5, 
    xi=10, niter=100, expweight=True,
    boundary='upper'
)
pol_lower = bf.boundfit_poly(
    x=xfit, y=yfit, deg=5, 
    xi=10, niter=100, expweight=True,
    boundary='lower'
)
```

Fit upper and lower boundaries using splines (the numerical minimization takes some time).

```python
spl_upper = bf.boundfit_adaptive_splines(
    x=xfit, y=yfit, t=5, 
    xi=100, niter=100, boundary='upper',
    adaptive=False,
    expweight=True
)
spl_lower = bf.boundfit_adaptive_splines(
    x=xfit, y=yfit, t=5, 
    xi=100, niter=100, boundary='lower',
    adaptive=False,
    expweight=True
)
```

Display the result

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(xfit, yfit, 'ko')
ax.plot(xfit, pol_upper(xfit), '-', label='upper boundary (polynomial)')
ax.plot(xfit, pol_lower(xfit), '-', label='lower boundary (polynomial)')
ax.plot(xfit, spl_upper(xfit), ':', label='upper boundary (splines)')
ax.plot(xfit, spl_lower(xfit), ':', label='lower boundary (splines)')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.legend()
plt.tight_layout()
plt.show()
```
![pyboundfit demo plot](https://guaix.fis.ucm.es/~ncl/pyboundfit/pyboundfit_usage.png)

**Please, note that the results are quite sensitive to the fitting parameters.**

## Citation

If you find this package useful, please cite
[Cardiel 2009](https://ui.adsabs.harvard.edu/abs/2009MNRAS.396..680C/abstract).

```
@ARTICLE{2009MNRAS.396..680C,
       author = {{Cardiel}, N.},
        title = "{Data boundary fitting using a generalized least-squares method}",
      journal = {\mnras},
     keywords = {methods: data analysis, methods: numerical, Astrophysics - Instrumentation and Methods for Astrophysics},
         year = 2009,
        month = jun,
       volume = {396},
       number = {2},
        pages = {680-695},
          doi = {10.1111/j.1365-2966.2009.14749.x},
archivePrefix = {arXiv},
       eprint = {0903.2068},
 primaryClass = {astro-ph.IM},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2009MNRAS.396..680C},
      adsnote = {Provided by the SAO/NASA Astrophysics Data Syste
```
