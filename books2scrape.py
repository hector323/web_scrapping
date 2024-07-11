import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

# Example usage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def scrape_book_results_page(page_num, headers):
    """
    scrape_book_results_page 
    
    :param page_num: page number 
    :param headers: request headers
    :return: dictionary with the following keys:
        page_url: The URL of the books results page
        response: The Response object of that page
        soup: The BeautifulSoup object created from the source code
        book_urls: A list of the URLs for each book on this page
    """
    
    # For each results page, scrape the URLs for each book page
    page_url = f'https://books.toscrape.com/catalogue/page-{page_num}.html' 
    response = requests.get(page_url, headers=headers)
    
    # Check if the response is successful
    if response.status_code != 200:
        return {
            'page_url': page_url,
            'response': response,
            'soup': None,
            'book_urls': []
        }
    
    text = BeautifulSoup(response.text, 'html.parser')
    
    # Get the book page URLs and add the domain, then add to book page URL list
    book_divs = text.find_all('div', attrs={'class': 'image_container'})
    book_urls = [tag.find('a').get('href') for tag in book_divs]
    complete_book_urls = [f'https://books.toscrape.com/catalogue/{end_part}' for end_part in book_urls]
    
    # return book_dict
    return {
        'page_url': page_url,
        'response': response,
        'soup': text,
        'book_urls': complete_book_urls
    }



        
def scrape_book_product_page(book_url, headers=headers):
    """
    scrape_book_product_page docstring (book_product_url, headers): 
    
    This function takes a book product URL (the URL for the book product page) 
    
    and a headers dictionary as arguments 
    
    and returns a dictionary with the following keys:
        book_url: The URL of the book product page
        response: The Response object of that page
        soup: The BeautifulSoup object created from the source code
    """
    

    response = requests.get(book_url, headers=headers)
    text = BeautifulSoup(response.text, 'html.parser')
    
    if response.status_code != 200:
        raise Exception(f'The status code is not 200! It is {response.status_code}.')
    
    # return book_dict
    return {
        'book_url': book_url,
        'response': response,
        'soup': text,
    }


def scrape_book_range(page_range, filename, headers=headers):
    """
    scrape_book_range docstring
    
    
    scrape_book_range(page_range, filename, headers): 
    This function takes a page range (range object), a filename for the a CSV file, 
    and a headers dictionary as arguments and will use the other two functions to scrape the book information 
    for every book found in the specified page range. 
    This book information should be saved as separate rows in a CSV file 
    (see if you can include the CSV file writing code in this function).
    
    
    :param page_range: range of int
    :param filename: filename
    :param headers: request headers
    :return: None
    """
    acceptable_page_range = list(range(1,51))
    page_range = [i for i in page_range if i in acceptable_page_range]
    
    # Create a new CSV file
    with open(filename, 'w', encoding = 'utf-8', newline='') as csvfile:
        # Create the CSV writer object
        book_writer = csv.writer(csvfile)
        # Write the initial header row
        book_writer.writerow(['title', 'price_in_pounds', 'avg_rating', 'genre', 'upc', 'num_books_available'])
        stars_map = {'One': 1 , 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        
        for page in page_range:
              results = scrape_book_results_page(page, headers)
              for book_url in results['book_urls']:
                  book = scrape_book_product_page(book_url)
                  text = book['soup']
                  
                
                  # Get title
                  title = text.find('div', attrs = {'class': 'col-sm-6 product_main'}).find('h1').string
                  # Get price
                  price_in_pounds = text.find('p', attrs = {'class':'price_color'}).string
                  # Get average rating
                  avg_rating_tag = text.find(lambda tag: 'star-rating' in tag.get('class') if tag.get('class') else False)
                  avg_rating = avg_rating_tag.get('class')[1]
                  # Get genre
                  li_tag = text.find('ul', attrs={'class':'breadcrumb'}).find_all('li')[2]
                  genre = li_tag.find('a').string
                  # Get UPC
                  tr_tag = text.find('table', attrs = {'class':'table table-striped'}).find_all('tr')[0]
                  upc = tr_tag.find('td').string
                  # Get number of books available
                  num_books_available = text.find('p', attrs = {'class':'instock availability'}).get_text()
              
                  # Store info in the dictionary
                  book_dict = {}
                  book_dict['title'] = title
                
                  book_dict['price_in_pounds'] = float(re.search('[0-9.]+' , price_in_pounds).group())
                    
                  book_dict['avg_rating'] = stars_map.get(avg_rating)
                  book_dict['genre'] = genre
                  book_dict['upc'] = upc
                  #book_dict['num_books_available'] = num_books_available
                  book_dict['num_books_available'] = ''.join(re.findall(r'\b\d+\b', num_books_available))  
                  #book_dict['num_books_available'] = int(re.search('\d+', num_books_available).group())
                  book_writer.writerow(book_dict.values())

