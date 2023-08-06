# email-scraper
A simple streamlit application where using can upload a txt file containing website links then start scraping for anything that resembles an email address.

# How to use:
1. Make sure you have python on your computer. Download the installer from [here](https://www.python.org/) <br />

2. Install required packages by opening your Command Prompt and typing the following <br />
`pip install streamlit pandas requests beautifulsoup4`

3. Navigate your Command Prompt to the project folder <br />
`cd <the project folder ex. C:\Users\You\Downloads\email-scraper`

4. Run the app. <br />
`streamlit run app.py`

# Supported file
For simplicity, this application will only support text file. Inside your text file, separate your websites by line break.

Once you have the application running, then uploaded your txt file, just hit Start Scraping. It will show which website is currently being processed and the collected emails.
After processing all the website links, it will give the option to **download everything in CSV**.
