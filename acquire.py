import requests
import pandas as pd
import os

def get_items():
    '''
    This function obtains data for the items in our Dataset.
    '''
    ## Set up base url 
    base_url = 'https://python.zgulde.net/'
    # Define response to obtain data for items
    response = requests.get(base_url + '/api/v1/items')

    #use json to read the data
    data = response.json()
    #create the DataFrame
    df_1 = pd.DataFrame(data['payload']['items'])

    #obtain datafor page 2
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    df_1 = pd.concat([df_1, pd.DataFrame(data['payload']['items'])]).reset_index()

    #obtain data for page 3
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    df_1 = pd.concat([df_1, pd.DataFrame(data['payload']['items'])]).reset_index()

    return df_1

def get_stores():
    '''
    Here we obtain data for stores.
    '''
    #define base url
    base_url = 'https://python.zgulde.net/'

    #define response to obtain data for stores
    response = requests.get(base_url + '/api/v1/stores')

    #use json to read the data
    data = response.json()

    #create the DataFrame
    df_2 = pd.DataFrame(data['payload']['stores'])

    return df_2


def get_sales_data():
    '''
    Here we acquire teh sales data.
    '''

    #Define url and response
    url = 'https://python.zgulde.net/api/v1/sales'
    response = requests.get(url)
    #create file
    filename = 'sales.csv'
    #obtain the file if the file already exists
    if os.path.isfile(filename):
        sales = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            #Create list, to which we will add our data
            extracted_data = list()
            #Get the amount of page numbers we need to loop through
            payload = response.json()['payload']
            max_page = payload['max_page']
            #add the sales data for each page
            for n in range(max_page):
                extracted_data.extend(payload['sales'])
                try:
                    #define url for each page number
                    new_url = url[:25] + payload['next_page']
                    #print page number
                    print(new_url)
                    #define response for each page number
                    response = requests.get(new_url)
                    #refine payload for the next iteration of the loop
                    payload = response.json()['payload']
                except:
                    pass
            #Read data into a DataFrame   
            sales = pd.DataFrame(extracted_data)
            #Create a new file with the data
            sales.to_csv(filename)

        else:
            print(response.status_codeup_code)
    return sales


def full_dataframe():
    '''
    We will combine the DataFrames made by the previosu three functions.
    '''
    #Obtain DataFrame for items
    df_1 = get_items()

    #Obtain DataFrame for stores
    df_2 = get_stores()

    #Obtain DataFrame for sales_data
    df_3 = get_sales_data()

    #Concatenate three DataFrames
    df = pd.concat([df_1, df_2, df_3], axis = 1)

    return df

def get_germany_wind_solar_data():
    '''
    Here we will acquire the data for German wind and solar power. 
    '''
    #Define url to the CSV data for Germany's wind and solar power. 
    url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    #Read the CSV data into a DataFrame
    germany_wind_and_solar = pd.read_csv(url)

    return germany_wind_and_solar