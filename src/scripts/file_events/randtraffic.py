import random
import requests
import dns.resolver
import mysql.connector

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

def query_dns():
    """
    Request the project DNS resolve google's URL.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["3.214.123.0"]
    answer = resolver.resolve("google.com")
    return answer

def query_web_server():
    """
    Request the project web server page.
    """
    return requests.get("http://3.214.123.0:80")

def query_mysql():
    """
    Request the databases from the project SQL server.
    """
    db = mysql.connector.connect(
        host="3.214.123.0",
        user="user",
        password="pass"
    )
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    return [x for x in cursor]

def main():
    query_google()
    query_reddit()
    query_web_server()
    try:
        query_dns()
    except:
        pass
    try:
        query_mysql()
    except:
        pass

    # f = open("./temp/temp.html", "w+", encoding="utf-8")
    # f.write(resp.text)

if __name__ == '__main__':
    main()
