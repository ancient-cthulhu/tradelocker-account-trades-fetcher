# TradeLocker Account Trades Fetcher

This Streamlit application fetches account data from TradeLocker using their REST API. It fetches orders history and available instruments per account using JWT authentication.

[App hosted through Streamlit](https://tradelocker-atf.streamlit.app/)

## Features

- **Authentication**: Authenticate using email, password, and server URL.

- **Data Fetching**: Fetch orders history and instruments for multiple accounts.
 
- **CSV Upload**: Option to upload credentials via a CSV file.

- **Live Results**: Displays fetched data and provides a .zip file containing the .json files. 
 
## Security Details

- **HTTPS Encryption**: All data transmissions between the application and TradeLocker's API are encrypted using HTTPS, ensuring secure communication.
  
- **Client-Side Processing**: Data processing occurs entirely within the user's browser, minimizing exposure of sensitive information to the server.


## How to Use

1\. **Installation**

   Clone the repository and navigate into the directory:

   ``
   git clone https://github.com/ancient-cthulhu/tradelocker-account-trades-fetcher.git
   ``
   
   ``
   cd tradelocker-account-trades-fetcher
   ``

2\. **Setup**

   Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3\. **Running the App**

   Start the Streamlit app:

   ```
   streamlit run home.py
   ```

4\. **Using the App**

   - Choose an input method: either upload a CSV file with credentials or enter them manually.

   - Click "Submit" to initiate data retrieval for each account.

   - Results will be displayed live with an option to download a .zip file containing the fetched data.

## Example CSV Format

```

email,password,server

user1@example.com,password123,demo.tradelocker.com

user2@example.com,securepass,prod.tradelocker.com

```

## Disclaimer

This Streamlit page is not affiliated with TradeLocker. TradeLocker is a registered trademark owned by its respective owners. This page is created solely for educational and demonstrative purposes to showcase data fetching and processing capabilities using TradeLocker APIs.

---

### Author

Made with ☕ by [ancient-cthulhu](https://github.com/ancient-cthulhu)

---
