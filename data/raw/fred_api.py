import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import matplotlib.pyplot as plt

#finds .env and loads up the API Key so os.getenv can see it
load_dotenv()
#create a FRED connection using the API key.
fred = Fred(api_key=os.getenv('FRED_API_KEY'))

#get the GDP growth as a panda series
#drop rows with missing values
#convert index to proper datetime format so slicing and plotting easy
#name the series so when save to csv column has a name
def get_gdp_growth():
    gdp = fred.get_series('A191RL1Q225SBEA')
    print(gdp.isna().sum()) #should have 0 missing values
    gdp = gdp.dropna()
    gdp.index = pd.to_datetime(gdp.index)
    gdp.name = 'gdp_growth'
    return gdp

gdp = get_gdp_growth()
gdp.to_csv('data/gdp_growth.csv', header=True) #save data locally
print(gdp.head(10))

gdp.plot(kind="line", 
         xlabel="Date", 
         ylabel="GDP Growth (%)",
         title="US Real GDP Growth (Annualised)",
         figsize=(12, 4),
         color="steelblue")
plt.axhline(y=0, color="black", linewidth=0.8)
#we show on the plot that we ignore the massive outliers of 2020 Q2 and Q3
plt.axvspan('2020-04-01', '2020-10-01', color='red', alpha=0.2, label='COVID excluded')
plt.legend()
plt.tight_layout()
plt.show()


#Hamilton's recession dates based on GDP-indicator
nber = fred.get_series('JHDUSRGDPBR')
nber.index = pd.to_datetime(nber.index)
nber.to_csv('data/nber.csv', header=True)
print(nber.head(20))