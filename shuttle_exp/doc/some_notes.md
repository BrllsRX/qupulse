# Programming Notes (qupulse)

*It is obvious a good habit to write down some notes during Programming.*

## Installation

> ### Observation:
> `python -m pip install -e .` and `python setup.py develop` are doing different things.

> ### My understand:
> Both of them should make an editable installation with a locally cloned package. However, the former command installed a pre-released version say v-0.7 independent of any changes in the package. The other one works as intended that by making an egg-link in the `site-packages` folder of a `venv` instead of installing a package, all local modification can be reloaded and used by other scripts. 
> - ONLY tested with Jupyter Notebook in VS Code. `python 3.7.9` in a virtual environment is used.

