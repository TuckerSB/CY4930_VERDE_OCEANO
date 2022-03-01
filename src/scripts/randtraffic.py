import random
import requests

def query_google():
    """
    Request a google search using a random word from a list.
    """
    query_template = "https://www.google.com/search?q="
    query_words = [
        "apple",
        "banana",
        "orange",
        "Aristotle",
        "Plato",
        "Socrates",
        "Cloth",
        "Paper",
        "Plastic",
    ]
    query = query_template + random.choice(query_words)
    return requests.get(query)

def query_reddit():
    """
    Request a Reddit page using a random name from a list.
    """
    query_template = "https://www.reddit.com/r/"
    query_words = [
        "NEU",
        "privacy",
        "Python",
    ]
    query = query_template + random.choice(query_words)
    return requests.get(query)

def main():
    query_google()
    query_reddit()
    # f = open("./temp/temp.html", "w+", encoding="utf-8")
    # f.write(resp.text)

if __name__ == '__main__':
    main()