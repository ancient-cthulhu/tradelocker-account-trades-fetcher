# TradeLocker Account Trades Fetcher

This Streamlit application fetches account data from TradeLocker using their REST API. It fetches orders history and available instruments per account using JWT authentication.

## Features

- **Authentication**: Authenticate using email, password, and server URL.

- **Data Fetching**: Fetch orders history and instruments for multiple accounts.
 
- **CSV Upload**: Option to upload credentials via a CSV file.

- **Live Results**: Displays fetched data and provides download links for JSON files.

## How to Use

1\. **Installation**

   Clone the repository and navigate into the directory:

   ``
   git clone https://github.com/yourusername/tradelocker-data-fetcher.git
   ``
   
   ``
   cd tradelocker-data-fetcher
   ``

2\. **Setup**

   Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3\. **Running the App**

   Start the Streamlit app:

   ```
   streamlit run app.py
   ```

4\. **Using the App**

   - Choose an input method: either upload a CSV file with credentials or enter them manually.

   - Click "Fetch Data" to initiate data retrieval for each account.

   - Results will be displayed live with download links for fetched data.

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
