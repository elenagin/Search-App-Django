import requests
from requests.compat import quote_plus  # this will automtically put + between words
from django.shortcuts import render
from bs4 import BeautifulSoup

from . import models

BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_='result-title').text
    # post_url = post_listings[0].find('a').get('href')

    # post_titles = soup.find_all('a', {'class': 'result-title'})
    # print(post_titles[0].text)
    # print(post_titles[0].get('href'))

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image = 'https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png'
        final_postings.append((post_title, post_url, post_price, post_image))

    frontend_data = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', frontend_data)
