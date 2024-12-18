from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

def get_news():
    # Fetch the RSS feed
    rss_url = "https://bianet.org/rss/kurdi"
    response = requests.get(rss_url)

    # Parse the RSS feed content
    root = ET.fromstring(response.content)

    # List to store news items as dictionaries
    news_items = []

    # Loop through each news item and store details in a dictionary
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        pub_date = item.find("pubDate").text
        media_content = item.find("{http://search.yahoo.com/mrss/}content")

        # Get the image URL if available
        image_url = media_content.attrib.get('url') if media_content is not None else None
        # Create a dictionary for the news item
        news_item = {
            "title": title,
            "link": link,
            "description": description,
            "published": pub_date,
            "image_url": image_url
        }

        # Add the dictionary to the list
        news_items.append(news_item)
    
    return news_items

@app.route('/news', methods=['GET'])
def news():
    news_data = get_news()
    return jsonify(news_data)
