"""Gets the top story on the Washington Post at runtime,
then writes a formatted txt file of the article's content
and saves the main image as jpg
"""

import requests
import json
import re
import datetime
import urllib.request
from bs4 import BeautifulSoup

def parse_date(arg):
    """Takes publish_date string from WaPo soup
    and returns the date as datetime object
    Time string from soup sometimes includes
    milliseconds, sometimes not
    """
    import datetime
    import sys
    for fmt in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ'):
        try:
            dt = datetime.datetime.strptime(arg, fmt)
            return dt
        except ValueError:
            pass
    raise ValueError('cannot parse time data')

def parse_authors(arg):
    """Parses soup for author names
    Author names within json sometimes
    appear in list of dicts, sometimes
    in dict
    """
    if isinstance(arg, list):
        names = ', '.join(arg['name'])[:-2]
        return names
    elif isinstance(arg, dict):
        names = arg['name']
        return names

def soupify(url):
    """pulls soup from site and processes into text"""
    response1 = requests.get(url)
    main_soup = BeautifulSoup(response1.text, 'html.parser')

    try:
        top_story_url = main_soup.find('h1').find('a')['href']
    except AttributeError:
        top_story_url = main_soup.find('div', {'class': 'headline normal x normal-style'}).find('a')['href']

    response2 = requests.get(top_story_url)
    story_soup = BeautifulSoup(response2.text, 'html.parser')

    meta_dict_str = story_soup.find('script', type="application/ld+json").text
    meta_json = json.loads(meta_dict_str)

    title = meta_json['headline']
    subtitle = meta_json['description']
    authors = meta_json['author']
    publish_date = meta_json['datePublished']
    modify_date = meta_json['dateModified']
    image_url = meta_json['image']['url']

    urllib.request.urlretrieve(image_url, 'image.jpg')

    return story_soup, title, subtitle, authors, publish_date, modify_date, image_url

def format_elements(story_soup, title, subtitle, authors, publish_date, modify_date, image_url):
    """takes soup objects, turns into formatted text and stores in lists"""
    elements = [title.upper(),
                f'**{subtitle}**',
                f'By {parse_authors(authors)}',
                parse_date(publish_date).strftime('%b. %d, %Y'),
                f"Updated {parse_date(modify_date).strftime('%H:%M')}"
                ]

    grafs = story_soup.find_all('p')

    # cut off junk text at end of article
    for index, par in enumerate(grafs):
        if re.search(r'contributed to this report.$', par.text):
            grafs = grafs[0:index+1]

    body = []
    for p in grafs:
        body.append(f'\t{p.text}')
    elements.append('\n'.join(body))

    return elements

def write_story():
    """takes soup and writes to file"""
    url = 'http://www.washingtonpost.com'
    elements = format_elements(*soupify(url))
    filename = 'wapo_top_story.txt'
    with open(filename, 'w') as story:
        for e in elements:
            story.write(e)
            story.write('\n\n')
        story.write('========')

if __name__ == '__main__':
    write_story()
