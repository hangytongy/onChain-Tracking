import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import seaborn as sns
from math import ceil
import os
sns.set()

def get_token_transactions(address, contract_address, api_key, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc'):
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'tokentx',  # To fetch ERC20 token transactions
        'contractaddress': contract_address,  # Token contract address
        'address': address,  # Address to fetch transactions for
        'startblock': startblock,
        'endblock': endblock,
        'page': page,
        'offset': offset,
        'sort': sort,
        'apikey': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
    

def get_data(address,contract_address,api_key,days):
    
    try:
        transactions = get_token_transactions(address, contract_address, api_key)
        df = pd.DataFrame(transactions['result'])
        token = df['tokenSymbol'].iloc[0]
        print("token symbol : ", token)
        df['time'] = pd.to_datetime(df['timeStamp'].astype(int), unit='s')
        df = df.drop(columns = ['timeStamp','blockNumber','hash','nonce','blockHash','tokenName','input','gas','gasPrice',
                           'gasUsed','cumulativeGasUsed','confirmations','transactionIndex'])
        cond_buy = df['from'] != address.lower()
        df['txType'] = np.where(cond_buy, 'buy', 'sell')
        df['value'] = df['value'].astype(float)
        df['value_tx'] = df['value']/(10**int(df['tokenDecimal'].iloc[0]))
        df.loc[df['txType'] == 'sell', 'value_tx'] *= -1
        
        #get stipuated period of data
        now = datetime.now()
        days_before = now + timedelta(days = -days)
        days_before = days_before + timedelta(hours = -8) #convert to GMT +0
        cond = df['time'] > days_before
        df = df[cond]
        
        df['cumulative'] = df['value_tx'].cumsum()
        df['line'] = 0
        
        return df
        
#        df['date'] = df['time'].dt.date
#        df_grouped = df.groupby(['date'])['value_tx'].sum().reset_index()
#        df_grouped['cumulative'] = df_grouped['value_tx'].cumsum()
#        df_grouped['line']=0
#    
#        return df_grouped, token
    
    except Exception as e:
        print(f"error : {e}")
        return
    
def get_tx_dist(df):
    no_of_tx = len(df)
    avg_accumulation = round(df['value_tx'].sum()/no_of_tx,2)
    
    return no_of_tx, avg_accumulation

def plotting(addresses,dfs,token,days):
    
    current_date = datetime.now()
    start_date = current_date - timedelta(days=days)
    start_date = start_date + timedelta(hours = -8)
    
    no_of_add = len(addresses)

    print(f"number of addresses : {no_of_add}")
    
    fig, axs = plt.subplots(ceil(no_of_add/2), 2, figsize=(23,23)) #rows, columns
    
    for i in range(0,no_of_add):
        
        address = addresses[i]

        if i < ceil(no_of_add/2):
            j = 0
            k = i
        else:
            j = 1
            k = i - ceil(no_of_add/2)

        print(f"address : {address}")

        fontsize = 14

        try:
            dates = dfs[i]['time'].tolist()
            time_deltas = [(dates[i+1] - dates[i]).total_seconds() for i in range(len(dates)-1)]
            average_delta = np.mean(time_deltas)
            half_block_width = average_delta / (3 * 86400)
            
        except:
            half_block_width = 0.01
        
        print("width for buy/sell block done")
        
        no_of_tx, avg_accumulation = get_tx_dist(dfs[i])
        tx_text = f"num of tx = {no_of_tx} \nAvg Accum = {avg_accumulation}"
        print(tx_text)

        axs[k,j].fill_between(dfs[i]['time'], dfs[i]['cumulative'], color = 'skyblue', edgecolor = 'black', label = 'cumulative token')
        axs[k,j].set_title(f'cumulative Token {token} by address {address}', fontsize = fontsize)
        axs[k,j].set_xlabel("Date", fontsize = fontsize)
        axs[k,j].set_ylabel("# of Token", fontsize = fontsize)
        axs[k,j].tick_params(axis='x', rotation=30)
        axs[k,j].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        axs[k,j].xaxis.set_major_locator(mdates.AutoDateLocator())
        axs[k,j].set_xlim([start_date, current_date])
        axs[k,j].grid(True)
        axs[k,j].legend(fontsize = fontsize)


        colors = dfs[i]['value_tx'].apply(lambda x : 'lime' if x >= 0 else 'red')
        axs[k,j].bar(dfs[i]['time'], dfs[i]['value_tx'] , color = colors, width = half_block_width, edgecolor = 'black', linestyle=":", label = 'buy/sell',alpha =0.5)
        axs[k,j].plot(dfs[i]['time'],dfs[i]['line'], color = 'black')
        axs[k,j].set_title(f'Buy/Sell for Token {token} by address {address}', fontsize = fontsize)
        axs[k,j].set_xlabel("Date", fontsize = fontsize)
        axs[k,j].set_ylabel("# of Token", fontsize = fontsize)
        axs[k,j].tick_params(axis='x', rotation=30)
        axs[k,j].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        axs[k,j].xaxis.set_major_locator(mdates.AutoDateLocator())
        axs[k,j].set_xlim([start_date, current_date])
        axs[k,j].grid(True)
        axs[k,j].legend(fontsize = fontsize)
        axs[k,j].text(0.02, 0.95, tx_text, fontsize=fontsize, transform=axs[k,j].transAxes, verticalalignment='top',horizontalalignment='left',
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5',alpha = 0.7))
        #plt.gcf().autofmt_xdate()
        
        print("################################################")
    plt.tight_layout()
    #plt.show()
    
    current_directory = os.getcwd()
    image_path = os.path.join(current_directory,"charts.png")

    plt.savefig(image_path)
    plt.close()  # Close the plot to free up memory

    return image_path

