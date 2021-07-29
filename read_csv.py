import pandas as pd 
import csv

filepath = "/home/hp/workspace/pph/flask_project/flask_scraping/test.csv"

df = pd.read_csv(filepath, sep='delimiter', header=None, engine='python')

print(df[0])

# for i in df:
#     print(i)