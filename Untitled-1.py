import requests
from bs4 import BeautifulSoup
import csv
import os

url = "https://www.imdb.com/search/title/?title_type=feature&num_votes=1000,&genres=sci-fi&sort=year,asc&start=1"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Function to extract movie details from a given movie item
def extract_movie_details(movie):
    title = movie.find('h3', class_='lister-item-header').find('a').text.strip()
    genre = movie.find('span', class_='genre').text.strip()
    rating = movie.find('div', class_='ratings-imdb-rating').strong.text.strip()
    year = movie.find('span', class_='lister-item-year').text.strip('()')
    dir_and_stars = movie.find('p', class_='').text.strip().split('|')
    length = movie.find('span', class_='runtime').text.strip()

    return {
        'Title': title,
        'Genre': genre,
        'Rating': rating,
        'Year': year,
        'Director and Stars': dir_and_stars,
        'Length': length
    }

# List to store all movie details
all_movies = []

# Loop through each page
while True:
    # Find all movie items on the current page
    movie_items = soup.find_all('div', class_='lister-item mode-advanced')
    
    # Extract movie details and add them to the list
    for movie in movie_items:
        movie_details = extract_movie_details(movie)
        all_movies.append(movie_details)

    # Check if there is a 'Next' button to navigate to the next page
    next_button = soup.find('a', class_='lister-page-next next-page')
    
    if next_button:
        next_url = 'https://www.imdb.com' + next_button['href']
        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        break

# Save movie details to a CSV file
filename = "movies.csv"

current_directory = os.getcwd()
file_path = os.path.join(current_directory, filename)

with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Genre', 'Rating', 'Year', 'Director and Stars', 'Length']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for movie in all_movies:
        writer.writerow(movie)

print(file_path)

