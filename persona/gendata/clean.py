from datetime import datetime
import pandas as pd
from rnddate import random_date
from random import randint

#"first_name","last_name","company_name","address","city","county","state","zip","phone1","phone2","email","web"

df = pd.read_csv('us-500.csv')

#reduce data
d2 = df[["last_name","first_name","zip"]]

#some zips were 4 digits... :-|
d2['zip'] = [str(randint(10000,99999)) for _ in df['zip']]

#generate random bdays
early = datetime(1950,1,1)
late = datetime(1999,12,31)
nums = [random_date(early,late).date() for _ in range(len(d2['zip']))]
d2['dateofbirth'] = pd.Series(nums, index=d2.index)

#reorder according to actual schema
d2 = d2[["last_name","first_name","dateofbirth","zip"]]

print(d2.to_string())
d2.index +=1    #dont use id 0
d2.to_csv('clean500.csv', header=False) #, index=False)
