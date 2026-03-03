from astropy.time import Time
true = True
false = False

all_filters = {

"your_filter1": [],

"your_filter2": []

#and so on
}



try:
    from zloom.filters._all_filters_local import all_filters
except ImportError:
    pass