# SportsLine

This repository contains a python class to scrape mlb odd from sportsline. 

# Required packages to include in virtual environment

```
import pandas as pd
import urllib.request as request
import json
from tzlocal import get_localzone
```

# How it works

```
import pySportsScraper as pss
import pandas as pd

sportsline = pss.pySportsScraper()

data = sportsline.get_raw_data()

book_dict = sportsline.game_data_simplified(data)

pd.DataFrame(book_dict)
```
