import requests
from bs4 import BeautifulSoup
import time
import re
import html  # Import the html module
import logging
import csv

logging.basicConfig(level=logging.INFO)

def save_to_csv(data, filename="threads.csv"):
    """Save thread data to a CSV file."""
    headers = ['Title', 'Link', 'Posts']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for thread in data:
            writer.writerow({
                'Title': thread['title'],
                'Link': thread['link'],
                # Join posts with a delimiter to store in one cell
                'Posts': " \n || \n".join(thread['posts'])
            })

    print(f"Data saved to {filename}")


def fetch_page(url):
    """Fetching URL"""
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; your-bot-name/1.0)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_html(html_content):
    """Parse URL"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def clean_text(text):
    "Removing HTLM Artifacts"
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Remove special characters and whitespaces
    text = text.replace('\n', ' ').replace('\r', ' ').strip()
    return text


def fetch_thread_content(thread_url):
    """Fetch thread content"""
    time.sleep(3)
    html_content = fetch_page(thread_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        posts = soup.find_all('div', class_='post_message')
        return [post.get_text().strip() for post in posts[:3]]
    else:
        return []


def extract_threads(soup):
    """Extract all threads"""
    thread_list = []
    base_url = 'https://www.flashback.org'  # Base URL

    for thread in soup.find_all('a', class_='thread-title')[:3]:
        title = thread.get_text().strip()  # Get thread title and strip any whitespace
        link = base_url + thread['href']  # Append 'href' to the base URL
        posts = fetch_thread_content(link)
        thread_list.append({'title': title, 'link': link, 'posts': posts})

    return thread_list


def main():
    """main function"""
    logging.info("Starting the scraper")
    url = 'https://www.flashback.org/aktuella-amnen'  # URL of the target page
    html_content = fetch_page(url)

    if html_content is None:
        print("Failed to fetch the webpage. Exiting")
        return

    soup = parse_html(html_content)
    current_threads = extract_threads(soup)
    for thread in current_threads:
        print(thread)
    
    save_to_csv(current_threads)

    logging.info("Scraper finished")


if __name__ == '__main__':
    main()
