#!/usr/bin/python

import requests
from lxml import html
import sys  
import urlparse
import collections

link = raw_input("Input URL to scrape: ")

urls_queue = collections.deque()  
urls_queue.append(link)  
found_urls = set()  
found_urls.add(link)

while len(urls_queue):  
    url = urls_queue.popleft()
    response = requests.get(url)
    parsed_body = html.fromstring(response.content)

    # Grab links to all images
    images = parsed_body.xpath('//img/@src')  
    if not images:  
        sys.exit("Found No Images")
        
    # Convert any relative urls to absolute urls
    images = [urlparse.urljoin(response.url, url) for url in images]  
    print 'Found %s images' % len(images)
    
    for img in images:  
        r = requests.get(img)
        f = open('downloaded_images/%s' % img.split('/')[-1], 'w')
        f.write(r.content)
        f.close()
    
    
    # Find all links
    links = {urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if urlparse.urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        found_urls.add(link)
        urls_queue.append(link)
