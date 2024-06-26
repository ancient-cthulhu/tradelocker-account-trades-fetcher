import streamlit as st
from st_pages import show_pages_from_config, add_indentation
st.set_page_config(page_title='Info', page_icon="📊")
add_indentation()
show_pages_from_config()

def main():
    st.title("TradeLocker Account :grey[Trades Fetcher]")
    st.markdown("""---""")

    st.markdown("""
        The TradeLocker Account :grey[Trades Fetcher] script securely retrieves account data from TradeLocker using provided credentials. Below, each function used in the script is showcased with an explanation to how they operate.
    """)
 
    st.markdown("### Overview of TradeLocker Account :grey[Trades Fetcher]")

    st.markdown("""
        The TradeLocker Account :grey[Trades Fetcher] script allows users to securely retrieve data from TradeLocker, including account numbers, order history, and trading instruments. 
        
        **It operates in the following steps:**
        1. **Authentication**: Uses provided email, password, and server to obtain a JWT token for API access.
        2. **Data Fetching**: Utilizes the JWT token to fetch account numbers, orders history, and trading instruments.
        3. **Data Presentation**: Displays fetched data and enables downloading of JSON files for further analysis.
    """)

    st.markdown("## Security")
 
    st.markdown("""
        TradeLocker Account :grey[Trades Fetcher] utilizes these security measures to protect user data:
        - **HTTPS**: All data transmissions are encrypted using HTTPS, ensuring secure communication between TradeLocker and the user's browser.
        - **Client-Side Processing**: Data processing occurs entirely within the user's browser, minimizing exposure of sensitive information.
        - **No Server Storage**: No data is stored on the server, enhancing privacy and security.
    """)

    st.markdown("## Functions Overview")

    st.markdown("### Function: Authentication")

    st.code("""
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
    """)

    st.markdown("### Function: Fetch All Account Numbers")

    st.code("""
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
    """)

    st.markdown("### Function: Fetch Orders History")

    st.code("""
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
    """)

    st.markdown("### Function: Fetch Account Instruments")

    st.code("""
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
    """)

    st.markdown("### Function: File Manage and Download")

    st.code("""
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

    """)

    st.markdown("""
        ## Conclusion

        The TradeLocker Account :grey[Trades Fetcher] script offers a secure and efficient way to retrieve and analyze trading data from TradeLocker. By leveraging HTTPS for encrypted data transmission and performing all data processing client-side, it ensures user privacy and security. Each function is designed to handle specific tasks such as authentication, data fetching, and result presentation seamlessly within Streamlit.
    """)

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
            margin-top: 10px;  /* Adjust margin top to reduce space */
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


if __name__ == "__main__":
    main()
