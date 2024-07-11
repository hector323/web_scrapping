Using the code from the Basic Python Roundup lecture notebook, create three functions:

scrape_book_results_page(page_num, headers): This function takes a page number and a headers dictionary as arguments and returns a dictionary with the following keys:
page_url: The URL of the books results page
response: The Response object of that page
soup: The BeautifulSoup object created from the source code
book_urls: A list of the URLs for each book on this page
scrape_book_product_page(book_product_url, headers): This function takes a book product URL (the URL for the book product page) and a headers dictionary as arguments and returns a dictionary with the following keys:
book_url: The URL of the book product page
response: The Response object of that page
soup: The BeautifulSoup object created from the source code
scrape_book_range(page_range, filename, headers): This function takes a page range (range object), a filename for the a CSV file, and a headers dictionary as arguments and will use the other two functions to scrape the book information for every book found in the specified page range. This book information should be saved as separate rows in a CSV file (see if you can include the CSV file writing code in this function).
Make sure to include proper documentation (docstring) for your code.

Before writing to CSV, make the following changes to the book data:

Convert price_in_pounds value to float type.
Convert avg_rating to int type.
Extract the number of available books from the num_books_available string and convert to int type.