# onChain-Tracking

## Goal
> To track the top 10 wallets accumulating/distributing specified tokens at a fixed interval

## Staring the Script

1. **Clone the Repository**
   
   ```
   git clone https://github.com/hangytongy/onChain-Tracking/
   ```

2. **Set both the ethscan and dunes keys as environment variables**
    
   Replace the `<API-KEY>` with your actual api keys. 
    ```sh
    export api_key_ethscan=<API_KEY>
    export api_key_dunes=<API_KEY>
    ```
   - Etherscan : https://ethscan.io/apis
     
   - Dunes: https://dune.com  

    
4. **Go into the repo,create your python environment and install the dependencies**

   ```
   cd onChain-Tracking
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

5. **Run the script and enjoy**

   ```
   streamlit run app.py
   ```
   When you run the script, the http link would usually be your server IP followed by the port `8501`. eg. `http://11.22.33.44:8501/`


### Notes

To add more tokens into the list, head to `token_list.csv` and add in the corresponding data inside.

- Token : the token symbol to display
- 1 : query ID for 1 day for corresponding token
- 7 : query ID for 7 days for corresponding token
- contract: contract address for corresponding token

### Limitations

This script was created with the querying of top holders using Dunes. In Dunes, in order to dynamically query the token contract address over a certain period of time, we can create parameters ({contract} & {time}). However, parameters are a paid feature. Therefore, current script hard codes the parameters into the individual queries and thus each permutation will have different query IDs. Not practicle if user wants a whole list of tokens and diff range of dates to track.
