from django.shortcuts import render, HttpResponse
from django.urls import resolve
from bs4 import BeautifulSoup
import requests
import re

def strip_html(request):
    url = request.GET['u']
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    for script in soup(["script", "style", "link"]): # remove all javascript and stylesheet code
        script.extract()

    for img in soup(["img"]): # remove all javascript and stylesheet code
        alt = img.get('alt') or 'img_alt'
        para = soup.new_tag('p')
        para.string = alt
        img.replaceWith(para)


    return HttpResponse(str(soup))


def show_headings(request):
    url = request.GET['u']
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    newsoup = BeautifulSoup('', 'html.parser')

    for x in soup.find_all(re.compile(r'h\d+')):
        newsoup.append(x)


    return HttpResponse(newsoup.prettify())
