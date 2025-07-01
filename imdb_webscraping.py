# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# url = "https://m.imdb.com/chart/top/"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
# }
# response = requests.get(url, headers=headers)
# print(response.url)
# print(response.text[:1000])

# # Check if we got the page
# print("Status Code:", response.status_code)
# soup = BeautifulSoup(response.content, "html.parser")

# # Step 2: Locate the table containing the top movies
# movie_table = soup.find("table", class_="chart")

#     # Step 3: Get all rows of the table except the header
# rows = movie_table.find_all("tr")[1:]

#     # Step 4: Parse each row
# data = []

# for row in rows:
#     title_column = row.find("td", class_="titleColumn")
#     rating_column = row.find("td", class_="ratingColumn imdbRating")

#     rank = int(title_column.get_text(strip=True).split('.')[0])
#     title = title_column.a.text
#     year = title_column.span.text.strip("()")
#     rating = rating_column.strong.text if rating_column.strong else None
#     movie_url = "https://www.imdb.com" + title_column.a["href"]

#     data.append({
#         "Rank": rank,
#         "Title": title,
#         "Year": year,
#         "Rating": float(rating) if rating else None,
#         "URL": movie_url
#     })

#     # Step 5: Store in a DataFrame
# df = pd.DataFrame(data)

# print(df.head())  # Preview the data

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

url = "https://m.imdb.com/chart/top/"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch page.")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all movie containers
    movies = soup.select("div.ipc-metadata-list-summary-item__tc")

    data = []
    for rank, movie in enumerate(movies, start=1):
        title_tag = movie.select_one("h3")
        title = title_tag.text.strip() if title_tag else "N/A"

        year_tag = movie.select_one("ul li span")
        year = year_tag.text.strip("()") if year_tag else "N/A"

        rating_tag = movie.select_one("span.ipc-rating-star")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        link_tag = movie.find("a", href=True)
        url = "https://www.imdb.com" + link_tag["href"] if link_tag else "N/A"

        data.append({
            "Rank": rank,
            "Title": title,
            "Year": year,
            "Rating": rating,
            "URL": url
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    print(df.head())
