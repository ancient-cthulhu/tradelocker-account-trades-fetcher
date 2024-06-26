import streamlit as st
import requests
import json
import pandas as pd
import zipfile
from io import BytesIO
from st_pages import show_pages_from_config, add_indentation

st.set_page_config(page_title='TradeLocker Data Fetcher', page_icon="📈")
add_indentation()
show_pages_from_config()


# Function to authenticate and fetch JWT tokens
def authenticate(email, password, server):
    auth_url = 'https://demo.tradelocker.com/backend-api/auth/jwt/token'
    payload = {
        "email": email,
        "password": password,
        "server": server
    }
    try:
        response = requests.post(auth_url, json=payload)
        if response.status_code == 201:
            auth_data = response.json()
            return auth_data.get('accessToken', None), auth_data.get('refreshToken', None)
        else:
            st.error(f"Error: Unable to authenticate. Status code: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None, None

# Function to fetch all account numbers using JWT access token
def fetch_all_account_numbers(api_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'accept': 'application/json'  
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get('accounts', [])  
        else:
            st.error(f"Error: Unable to fetch account numbers. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch orders history for a specific account using JWT access token and account number
def fetch_orders_history(api_url_orders_history, access_token, acc_num):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'accept': 'application/json',  
        'accNum': str(acc_num) 
    }
    try:
        response = requests.get(api_url_orders_history, headers=headers)
        if response.status_code == 200:
            return response.json().get('d', {}).get('ordersHistory', [])
        else:
            st.error(f"Error: Unable to fetch orders history. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch instruments available for trading
def fetch_account_instruments(api_url_base, access_token, acc_num, locale='en'):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'accept': 'application/json',
        'accNum': str(acc_num)
    }
    params = {
        'locale': locale
    }
    try:
        response = requests.get(api_url_base, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('d', {}).get('instruments', [])
        else:
            st.error(f"Failed to fetch instruments. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching instruments: {e}")
        return None

# Function to store JSON data for download button
def store_download_data(data_store, data, filename):
    json_data = json.dumps(data, indent=4)
    data_store[filename] = BytesIO(json_data.encode())

# Function to create a zip archive of all stored data
def create_zip_archive(data_store):
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, 'w') as zipf:
        for filename, filedata in data_store.items():
            zipf.writestr(filename, filedata.getvalue())
    return zip_data

# Streamlit App
def main():
    st.markdown("# TradeLocker Account :grey[Trades Fetcher]")
    st.markdown("""---""")

    input_method = st.radio("Select Input Method", ["Single Credential Input", "Upload CSV with credentials"])

    credentials_df = None
    
    if input_method == "Upload CSV with credentials":
        st.markdown("""
            #### CSV Format for Credentials
            Upload a CSV file with columns: `email`, `password`, `server`.
            
            Example:
            ```
            email,password,server
            user1@example.com,password123,demo.tradelocker.com
            user2@example.com,securepass,prod.tradelocker.com
            ```
        """)
        
        st.subheader("Upload CSV with Credentials")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            credentials_df = pd.read_csv(uploaded_file)
            if set(['email', 'password', 'server']).issubset(credentials_df.columns):
                st.success("CSV file uploaded successfully")
            else:
                st.error("CSV must contain 'email', 'password', and 'server' columns")
                return
        else:
            st.info("Please upload a CSV file.")
            return
    else:
        st.subheader("Single Credential Input")
        email = st.text_input("Email")
        col1, col2 = st.columns([1, 1])
        with col1:
            password = st.text_input("Password", type="password")
        with col2:
            server = st.text_input("Server")
        
        if st.button("Submit"):
            if not email or not password or not server:
                st.error("Please provide all required credentials.")
                return
            credentials_df = pd.DataFrame([{'email': email, 'password': password, 'server': server}])

    if credentials_df is None:
        st.info("Please enter credentials or upload a CSV file.")
        return

    api_url_base = 'https://demo.tradelocker.com/backend-api/trade/accounts'
    api_url_accounts = 'https://demo.tradelocker.com/backend-api/auth/jwt/all-accounts'
    
    st.markdown("### Results")
    st.code("Fetching data... Please wait.")
    result_data = []
    data_store = {}

    for index, row in credentials_df.iterrows():
        email = row['email']
        password = row['password']
        server = row['server']

        # Authenticate and get tokens
        access_token, _ = authenticate(email, password, server)
        if not access_token:
            st.error(f"Authentication failed for user {email}. Skipping to next user.")
            continue

        # Fetch all account numbers
        account_numbers = fetch_all_account_numbers(api_url_accounts, access_token)
        if not account_numbers:
            st.error(f"Failed to fetch account numbers for user {email}. Skipping to next user.")
            continue

        user_results = {
            'email': email,
            'account_numbers': []
        }

        for account in account_numbers:
            acc_num = account.get('accNum')
            acc_id = account.get('id')

            # Fetch orders history for the account
            api_url_orders_history_base = f'{api_url_base}/{acc_id}/ordersHistory'
            orders_history = fetch_orders_history(api_url_orders_history_base, access_token, acc_num)
            if orders_history:
                filename = f'orders_history_{acc_id}.json'
                store_download_data(data_store, orders_history, filename)
                st.success(f"🐕 Fetched orders history for account {acc_id} of user {email}")
                user_results['account_numbers'].append({
                    'acc_id': acc_id,
                    'orders_history': orders_history
                })

            # Fetch instruments available for trading
            api_url_instruments_base = f'{api_url_base}/{acc_id}/instruments'
            account_instruments = fetch_account_instruments(api_url_instruments_base, access_token, acc_num)
            if account_instruments:
                filename = f'instruments_{acc_id}.json'
                store_download_data(data_store, account_instruments, filename)
                st.success(f"🐕 Fetched instruments for account {acc_id} of user {email}")
                user_results['account_numbers'].append({
                    'acc_id': acc_id,
                    'instruments': account_instruments
                })

        result_data.append(user_results)

    
   
    zip_data = create_zip_archive(data_store)

    
    st.download_button(
        label="🗂️ Download All Files as ZIP",
        data=zip_data,
        file_name='TradeLocker_data.zip',
        mime='application/zip'
    )

    
    st.markdown("### File Contents")
    for filename, filedata in data_store.items():
        with st.expander(f"Contents of {filename}"):
            st.code(filedata.getvalue().decode())

if __name__ == "__main__":
    main()
    
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #262730;
            color: #FAFAFA;
            text-align: center;
            padding: 3px 0; 
            border-top: 1px solid #262730;
            height: 45px; 
        }
        .footer p {
            margin-bottom: 0; 
            font-size: 12px;
        }
        .footer a {
            color: #808495; 
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .disclaimer {
            font-size: 12px;
            color: #343a40;
            margin-top: 10px; 
        }
        .disclaimer p {
            font-size: 12px;
            line-height: 1.5;
            margin-bottom: 5px;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="disclaimer">
            <p><strong>Disclaimer</strong></p>
            <p>This Streamlit page is not affiliated with TradeLocker.<br>
            TradeLocker is a registered trademark owned by its respective owners.<br>
            This page is created solely for educational and demonstrative purposes to showcase data fetching and processing capabilities using TradeLocker APIs.</p>
        </div>
        """
        , unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            <p>TradeLocker Account <span style="color:#808495;">Trades Fetcher</span></p>
            <p>Made with ☕ by <a href="https://github.com/ancient-cthulhu" target="_blank">ancient-cthulhu</a></p>
        </div>
        """
        , unsafe_allow_html=True
    )
