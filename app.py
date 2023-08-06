import os
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import base64

# Begin scraping functions
def get_internal_links(url):
    #st.write(f"Fetching internal links from {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    domain = url.split("//")[-1].split("/")[0]
    links = [a['href'] for a in soup.find_all('a', href=True) if domain in a['href'] or a['href'].startswith('/')]
    return links

def scrape_emails_from_website(url):
    links = get_internal_links(url)
    all_emails = []

    for link in links:
        # Convert relative links to absolute
        if link.startswith('/'):
            link = url + link

        #st.write(f"Scraping {link} for emails...")
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        website_text = soup.get_text()

        # Extract all email addresses
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}"
        emails = re.findall(email_pattern, website_text)
        all_emails.extend(emails)

    st.write(f"Found {len(all_emails)} emails for {url}.")
    return list(set(all_emails))  # Remove duplicates

def categorize_emails(emails, website):
    domain = website.split("//")[-1].split("/")[0]
    main_emails = []
    other_emails = []

    for email in emails:
        if domain in email:
            main_emails.append(email)
        else:
            other_emails.append(email)
    
    return main_emails, other_emails
# End scraping functions

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="emails.csv">Download CSV file</a>'

def save_data_to_csv(data):
    """Save data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv('emails.csv', index=False)

def refresh_sidebar():
    """Refresh the sidebar to show the download link."""
    if os.path.exists('emails.csv'):
        st.sidebar.empty()
        st.sidebar.markdown(get_table_download_link(pd.read_csv('emails.csv')), unsafe_allow_html=True)

def main():
    st.title("Website Email Scraper")

    # Sidebar
    st.sidebar.header("Captured emails history files:")
    
    # Uploader in the main area
    uploaded_file = st.file_uploader("Upload a txt file", type="txt")
    
    if uploaded_file is not None:
        # Counting the number of websites in the uploaded file
        websites = [line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines()]
        
        if st.button('Start Scraping'):
            data = []

            # Adjusting the layout
            col1, col2 = st.columns([0.4, 0.6])
            
            col1.header("Processed websites")
            col2.header("Collected emails")

            # Initializing empty list for logs
            logs = []

            for idx, website in enumerate(websites, 1):
                log_msg = f"Processing {website}..."
                logs.insert(0, log_msg)
                with col1:
                    col1.markdown(logs[0], unsafe_allow_html=True)
                    for log in logs[1:]:
                        col1.markdown(f'<span style="color: lightgray">{log}</span>', unsafe_allow_html=True)
                    try:
                        emails = scrape_emails_from_website(website)
                        data.append({
                            'website': website,
                            'emails': ", ".join(emails)
                        })

                    except Exception as e:
                        error_msg = f"Error processing {website}: {e}"
                        logs.insert(0, error_msg)
                        data.append({
                            'website': website,
                            'emails': "error or no email."
                        })

                    with col2:
                        col2.markdown(f"**{data[-1]['website']}**:")
                        col2.text(data[-1]['emails'])

                # Save the data to a CSV file after processing each website
                save_data_to_csv(data)
                refresh_sidebar()  # Refresh the sidebar after each save

            # Display download link in the main area
            st.markdown(get_table_download_link(pd.DataFrame(data)), unsafe_allow_html=True)

    # Call the function to ensure the sidebar is updated at the beginning
    refresh_sidebar()

if __name__ == '__main__':
    main()
