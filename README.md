```
███████╗██╗      ██████╗  ██████╗ ███╗   ███╗
╚══███╔╝██║     ██╔═══██╗██╔═══██╗████╗ ████║
  ███╔╝ ██║     ██║   ██║██║   ██║██╔████╔██║
 ███╔╝  ██║     ██║   ██║██║   ██║██║╚██╔╝██║
███████╗███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝

#  Zloom - A python wrapper for BOOM api for playing with ZTF and LSST alerts
```

step 0: clone the repository
```bash
git clone
```

step 1: install the package and required dependencies

For uv users, run the following commands in your terminal:
```bash
uv pip install -r requirements.txt
uv pip install -e .
```

for pip users, run the following commands in your terminal:
```bash
pip install -r requirements.txt
pip install -e .
```

for conda users, run the following commands in your terminal:
```bash
conda install --file requirements.txt
pip install -e .
```


step 2: set up your BOOM credentials in environment variables 

open bashrc or zshrc and add the following lines, replacing with your actual BOOM username and password:
```bash
export BOOM_USERNAME=your_boom_username
export BOOM_PASSWORD=your_boom_password
```
You are all set up to use the package! You can use the CLI commands to run the scripts.

Examples

1. Counting number of alerts for ZTF and LSST in the last "N" days:

```bash
# you can use --help flags for more details on the arguments you can pass
zloom-zloom-nalerts --n_days 2 # by default n_days is set to 1
```

If you want to check only for ZTF or LSST, you can use the following flags:

```bash
zloom-nalerts-lsst # you can use --help flags for more details on the arguments you can pass
zloom-nalerts-ztf # you can use --help flags for more details on the arguments you can pass
```

2. Scanning the nightly alerts that passed your filter: (max 7 days). You can use this to check how many alerts passed your filter in the last "N" days and also to explore the alerts that passed your filter visually in the babamul page. The script will open "n_tabs" number of tabs in your browser (you can set the number of tabs you want to open with the --n_tabs flag) with the babamul page for the alerts that passed your filter. If you have more alerts that passed your filter than the number of tabs you set, it will show you the most recent ones.

YOU WILL NEED TO HAVE YOUR FILTER SAVED IN THE `all_filters` DICTIONARY IN `src/zloom/filters/all_filters.py` TO BE ABLE TO USE THIS SCRIPT.

```bash
# you can use --help flags for more details on the arguments you can pass
zloom-scan-nightly 
```

You can store your filter with a name in [`src/zloom/filters/all_filters.py`](src/zloom/filters/all_filters.py) and then use the following command to run the scan for that filter:

You can copy your filter from the skyportal (which will be a list of dictionaries) and store it in the `all_filters` dictionary in `src/zloom/filters/all_filters.py` with a name as the key. For example:
  ```python
    from astropy.time import Time
    true = True
    false = False

    all_filters = {

    "your_filter1": [],

    "your_filter2": []

    #and so on
    }
      ```
now, you have two filters with names "your_filter1" and "your_filter2". You can start scanning the nightly alerts using the following command (you will have an option to choose which filter you want to use for scanning, so you can save as many as you want and use them whenever you want!):

```bash
# you can use --help flags for more details on the arguments you can pass
zloom-scan-nightly 
```
If you want, you can pass the filter name as an argument and skip the filter choosing step:

```bash
zloom-scan-nightly --filter_name your_filter1 # you can use --help flags for more options
```
