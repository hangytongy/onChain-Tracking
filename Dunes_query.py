import requests
import pandas as pd
import time

tokens = pd.read_csv('token_list.csv', index_col=0)

def get_query_no(token,days):
    try:
        query_no = tokens[str(days)].loc[token]
        return query_no
    except Exception as e:
        print(f'error {e}')

def dunes_query(token,days,api_key):

    #get dunes query number
    query_no = get_query_no(token,days)
    
    url = f'https://api.dune.com/api/v1/query/{query_no}/execute'
    
    # Set up the headers
    headers = {
        'X-Dune-API-Key': api_key
    }

    print(f"execute request for token {token} across {days} day(s)")
    # Make the GET request
    response = requests.post(url, headers=headers)

    execution_id = response.json()['execution_id']

    print("request executed")

    # Get Query Status
    url_status = f"https://api.dune.com/api/v1/execution/{execution_id}/status"

    counter = 10
    while not requests.get(url_status,headers=headers).json()['state'] == "QUERY_STATE_COMPLETED":
        print(f"awaiting query.......{counter}s")
        print(requests.get(url_status,headers=headers).json())
        time.sleep(10)
        counter+=10
        
    print("query done, getting results")
    
    #Get query result
    url_results = f"https://api.dune.com/api/v1/execution/{execution_id}/results"
    
    response_result = requests.get(url_results, headers=headers)

    # Check if the request was successful
    if response_result.status_code == 200:
        # Parse the JSON response
        data = response_result.json()['result']
        df = pd.DataFrame(data['rows'])
        print("results returned")
        return df
        
    else:
        print(f"Error: {response.status_code} - {response.text}")


def get_wallet_data(df):
    addresses = df['holder'].tolist()
    wallets = {'Holder': df['holder'].tolist(), 'Accumated' : df['Balance'].tolist(), 'Wallet_type' : df['Trans_Status'].tolist()}

    intent_1 = f"{'Holder':<30} | {'Accumulation':<15} | {'Wallet Type':<15}" + "/n" + '-' * 65
    intent_2 = ""
    for i in range(len(wallets['Holder'])):
        intent_2 = intent_2 + "/n" + f"{wallets['Holder'][i]:<30} | {wallets['Accumulation'][i]:<15} | {wallets['wallet_type'][i]:<15}"
    result = intent_1 + intent_2

    return addresses,wallets
    


