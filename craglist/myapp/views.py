from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from myapp.models import Search
# Create your views here.
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"
BASE_CRAGLIST_URL = "https://pakistan.craigslist.org/search/?query={}"
def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRAGLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li',{'class':'result-row'})
    # print(post_titles[0].text)
    post_title = post_listings[0].find(class_="result-title").text
    post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_="result-price").text
    # print(post_title)
    # print(post_url)
    # print(post_price)
    final_listing = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(",")[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_listing.append((post_title,post_url,post_price,post_image_url))
  
    stuff = {
        'search':search,
        'final_list':final_listing,
        }
    return render(request,'myapp/new_search.html',stuff)