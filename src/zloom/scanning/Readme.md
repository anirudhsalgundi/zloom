# usage

run 

```python

python -m simple_scanning.py --help
```
for detailed usage guide.

sample usage: (if you want to chose the fiolter)

```python

uv run simple_scanning.py --n_tabs 3 --n_days 7 --creds $BOOM_CREDENTIALS
```

# sample usage if youalready know the filter you want to use

```python

uv run simple_scanning.py --filter_name test_filter --n_tabs 3 --n_days 5 --creds $BOOM_CREDENTIALS
```