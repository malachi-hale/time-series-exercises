import requests
import pandas as pd
import os

def get_items():
    '''
    This function obtains data for the items in our Dataset.
    '''
    base_url = 'https://python.zgulde.net/'
    response = requests.get(base_url + '/api/v1/items')

    data = response.json()
    df_1 = pd.DataFrame(data['payload']['items'])

    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    df_1 = pd.concat([df_1, pd.DataFrame(data['payload']['items'])]).reset_index()

    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    df_1 = pd.concat([df_1, pd.DataFrame(data['payload']['items'])]).reset_index()

    return df_1

def get_stores():
    '''
    Here we obtain data for stores.
    '''
    base_url = 'https://python.zgulde.net/'
    response = requests.get(base_url + '/api/v1/stores')

    data = response.json()

    df_2 = pd.DataFrame(data['payload']['stores'])

    return df_2


def get_sales_data():
    '''
    Here we acquire teh sales data.
    '''
    url = 'https://python.zgulde.net/api/v1/sales'
    response = requests.get(url)

    filename = 'sales.csv'
    if os.path.isfile(filename):
        sales = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            extracted_data = list()
            payload = response.json()['payload']
            max_page = payload['max_page']
            for n in range(max_page):
                extracted_data.extend(payload['sales'])
                try:
                    new_url = url[:25] + payload['next_page']
                    print(new_url)
                    response = requests.get(new_url)
                    payload = response.json()['payload']
                except:
                    pass
                
            sales = pd.DataFrame(extracted_data)
            sales.to_csv(filename)

        else:
            print(response.status_codeup_code)
    return sales


def full_dataframe():
    '''
    We will combine the DataFrames made by the previosu three functions.
    '''
    df_1 = get_items()

    df_2 = get_stores()

    df_3 = get_sales_data()

    df = pd.concat([df_1, df_2, df_3], axis = 1)

    return df

def get_germany_wind_solar_data():
    '''
    Here we will acquire the data for German wind and solar power. 
    '''
    url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    germany_wind_and_solar = pd.read_csv(url)

    return germany_wind_and_solar