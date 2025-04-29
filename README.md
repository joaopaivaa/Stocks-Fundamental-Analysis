# Stocks Fundamental Analysis

This project is designed to scrape stock information from the **Ibovespa** and **S&P 500** indices, retrieve financial data using the **Yahoo Finance Python library (yfinance)**, and perform a **fundamental analysis** based on custom metrics. The tool ranks the stocks and emails the top 10 from each index once a month.

---

## Features

- **Web Scraping**:
  - Retrieves the list of stocks in the Ibovespa and S&P 500 indices directly from Wikipedia tables via web scraping.

- **Financial Data**:
  - Gets detailed financial information about the stocks using the [Yahoo Finance Python library](https://pypi.org/project/yfinance/).

- **Fundamental Analysis**:
  - Analyzes stocks based on parameters defined by the project author.
  - Assigns scores to each stock based on the analysis.

- **Ranking**:
  - Ranks the stocks from both indices based on their scores.
  - Identifies the top 10 stocks for each index.

- **Email Notifications**:
  - Automatically sends an email with the top 10 ranked stocks from each index as a PDF file to the user's email address.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- Wikipedia for stock lists
- Yahoo Finance Python library for financial data
