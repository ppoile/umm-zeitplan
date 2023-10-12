# UMM-Zeitplan #

### Setup project ###

```
git clone git@github.com:ppoile/umm-zeitplan.git --recurse-submodules
cd umm-zeitplan
python3 -m venv venv
. venv/bin/activate
pip install -r pip-requirements
```

### ...and use it ###

```
cd src
python umm2022.py -h
python umm2022.py saturday --horizon=56
python umm2022.py sunday --horizon=58
python umm2022.py saturday --horizon=56 --ratio-gap=.2

python umm2023.py saturday --horizon=55
python umm2023.py sunday --horizon=52
```
