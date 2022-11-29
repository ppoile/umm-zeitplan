# UMM-Zeitplan #

### Setup project ###

```
git clone --recurse-submodules https://github.com/ppoile/umm-zeitplan
cd umm-zeitplan
python3 -m venv venv
. venv/bin/activate
pip install -r pip-requirements
```

### ...and use it ###

```
cd src
python umm2022.py -h
python umm2022.py saturday --horizon=56 -v
python umm2022.py sunday --horizon=58 -v
python umm2022.py saturday --horizon=56 -v --ratio-gap=.2
```
