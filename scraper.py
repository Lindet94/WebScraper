import requests
from bs4 import BeautifulSoup
import time


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


def fetch_thread_content(thread_url):
    """Fetch thread content"""
    time.sleep(1)
    html_content = fetch_page(thread_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        posts = soup.find_all('div', class_='post_message')
        return [post.get_text().strip() for post in posts[:5]]
    else:
        return []


def extract_threads(soup):
    """Extract all threads"""
    thread_list = []
    base_url = 'https://www.flashback.org'  # Base URL

    for thread in soup.find_all('a', class_='thread-title'):
        title = thread.get_text().strip()  # Get thread title and strip any whitespace
        link = base_url + thread['href']  # Append 'href' to the base URL
        posts = fetch_thread_content(link)
        thread_list.append({'title': title, 'link': link, 'posts': posts})

    return thread_list


def main():
    """main function"""
    url = 'https://www.flashback.org/aktuella-amnen'  # URL of the target page
    html_content = fetch_page(url)

    if html_content is None:
        print("Failed to fetch the webpage. Exiting")
        return

    soup = parse_html(html_content)
    current_threads = extract_threads(soup)
    for thread in current_threads:
        print(thread)


if __name__ == '__main__':
    main()
