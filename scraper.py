import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an HTTP error
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def extract_books(soup):
    book_list = []

    # Each book is contained in an 'article' tag with class 'product_pod'
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        link = 'https://books.toscrape.com/' + book.h3.a['href']
        price = book.find('p', class_='price_color').get_text()
        book_list.append({'title': title, 'link': link, 'price': price})

    return book_list


def main():
    url = 'https://books.toscrape.com/'
    html_content = fetch_page(url)
    soup = parse_html(html_content)
    books = extract_books(soup)
    for book in books:
        print(book)


if __name__ == '__main__':
    main()
