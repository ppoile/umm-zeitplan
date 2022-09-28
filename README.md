# UMM-Zeitplan #

### Setup project ###

```
git clone https://github.com/ppoile/umm-zeitplan
cd umm-zeitplan
python3 -m venv venv
. venv/bin/activate
pip install -r pip-requirements
```

### ...and use it ###

```
cd src
python umm2022.py -h
python umm2022.py saturday --horizon=51 --time-limit=8h -v
```
