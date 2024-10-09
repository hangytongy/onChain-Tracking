import Dunes_query
import wallet_token_data
import pandas as pd
import os

# Input parameters
api_key_ethscan = os.getenv('api_key_ethscan', default="") #remember to remove default
api_key_dunes = os.getenv('api_key_dunes', default='' ) #remember to remove default
#token = 'wquil'
#days = 7


def run_main(token,days):

    #Run on Dunes platform to get top 10 address 
    df = Dunes_query.dunes_query(token,days,api_key_dunes)
    addresses, result = Dunes_query.get_wallet_data(df)


    dfs = []

    #get token contract
    tokens = pd.read_csv('token_list.csv', index_col = 0)
    contract_address = tokens['contract'].loc[token] 

    #get tx data
    for address in addresses:
        print(address)
        data = wallet_token_data.get_data(address,contract_address,api_key_ethscan,days)
        print(f"no of tx : {len(data)}")
        dfs.append(data)
        
    
    #plot tx data
    print("-----------------running plotting data---------------------")
    image_path = wallet_token_data.plotting(addresses,dfs,token,days)

    return addresses, image_path, result


#if __name__ == "__main__":
#    run_main()
