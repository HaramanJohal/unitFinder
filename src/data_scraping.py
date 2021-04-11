import os
import requests
from bs4 import BeautifulSoup as bs


BBC_HOMEPAGE_URL = "https://www.bbc.co.uk"
BBC_NEWS_URL = BBC_HOMEPAGE_URL + "/news"


def contains_number(input_string):
    return any(char.isdigit() for char in input_string)


def is_article_href(href):
    return contains_number(href) and href.startswith("/news/") and href.count("/") == 2


def get_numeric_paragraphs_from_url(url):
    response = requests.get(url)
    soup = bs(response.content, "html.parser")
    article = soup.find("article")
    return [p.get_text() for p in article.find_all("p") if contains_number(p.get_text())]


def get_bbc_urls():
    response = requests.get(BBC_NEWS_URL)
    soup = bs(response.content, "html.parser")
    links = soup.find_all("a")
    return set([BBC_HOMEPAGE_URL + l["href"] for l in links if is_article_href(l["href"])])


def extract_number(input_string):
    words = input_string.split(" ")
    numbers = []
    for i, word in enumerate(words):
        if contains_number(word):
            if i < len(words) - 1 and "illion" in words[i + 1]:
                numbers.append((word + " " + words[i + 1], i))
            else:
                numbers.append((word, i))
    return numbers


if __name__ == "__main__":
    delimiter = os.environ["DATA_DELIMITER"]

    with open("data/scrapedData.txt", "a") as f:
        for url in get_bbc_urls():
            print(f"Processing: {url}")
            for para in get_numeric_paragraphs_from_url(url):
                numbers = extract_number(para)
                for (number, index) in numbers:
                    text = para.replace("\n", "")
                    f.write(f"{index}{delimiter}{number}{delimiter}{text}\n")
