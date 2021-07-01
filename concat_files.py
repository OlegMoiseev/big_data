import pandas as pd
import glob

files = glob.glob(r'*.csv')

df = pd.concat([pd.read_csv(f) for f in files])
df.to_csv('all_csv.csv')
