import requests
import pandas as pd
import os
from sklearn.impute import SimpleImputer

def prepare_store_data(df):
    # Reassign the sale_date column to be a datetime type
    df.sale_date = pd.to_datetime(df.sale_date)
    
    # Sort rows by the date and then set the index as that date
    df = df.set_index("sale_date").sort_index()
    
    #Create month column
    df['month'] = df.index.month_name()

    #Create day column
    df['day_of_week'] = df.index.day_name()
    
    #Create sales_total column
    df['sales_total'] = df['sale_amount'] * df['item_price']
    
    return df

def prepare_german_energy_data(df):
    # Reassign the sale_date column to be a datetime type
    df.Date = pd.to_datetime(df.Date)
    
    # Sort rows by the date and then set the index as that date
    df = df.set_index("Date").sort_index()
    
    #Create a month column 
    df['month'] = df.index.month_name()

    #Create a year column
    df['year'] = df.index.year
    
    imputer = SimpleImputer(strategy='most_frequent')

    #We will create a for loop that will impute all the null values in each one of our columns.
    for col in df.columns:
        df[[col]] = imputer.fit_transform(df[[col]])
        
    return df 