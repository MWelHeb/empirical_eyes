# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:54:26 2020

@author: Marc Wellner
"""

import pandas as pd

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
confirmed = pd.read_csv(url, error_bad_lines=False)
print(confirmed)