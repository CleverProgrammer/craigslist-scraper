import requests
import re
from requests.compat import quote_plus
from django.shortcuts import render
from .models import Search
from bs4 import BeautifulSoup
from bs4.element import Tag

page = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=41.8843&lon=-87.6324#.XIRQYFNKgUE'
)


# Create your views here.
def home(request):
    return render(request, 'my_app/index.html')


# access the search model
# create new search
# save & commit that to database
# then redirect to homepage

def new_search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        Search.objects.create(search=search)

        url = "https://losangeles.craigslist.org/search/?query={}&min_price={}&max_price={}"
        # print(urljoin(url, quote_plus(search)))
        min_price = request.POST.get('min_price', 0)
        max_price = request.POST.get('max_price', 1000)
        final_url = url.format(quote_plus(search), min_price, max_price)

        # Getting the webpage, creating a Response object.
        response = requests.get(final_url)
        # Extracting the source code of the page.
        data = response.text
        # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, features='html.parser')
        # Extracting all the <a> tags whose class name is 'result-title' into a list.
        post_listings = soup.find_all('li', {'class': 'result-row'})

        final_postings = []
        for post in post_listings:
            post_title = post.find(class_='result-title').text
            post_url = post.find('a').get('href')

            if post.find(class_='result-price'):
                post_price = post.find(class_='result-price').text
            else:
                new_response = requests.get(post_url)
                new_data = new_response.text
                new_soup = BeautifulSoup(new_data, features='html.parser')
                post_text = new_soup.find(id='postingbody').text

                r1 = re.findall(r'\$\w+', post_text)
                if r1:
                    post_price = r1[0]
                else:
                    post_price = 'N/A'


            if post.find(class_='result-image').get('data-ids'):
                post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
            else:
                post_image_url = 'https://craigslist.org/images/peace.jpg'

            final_postings.append((post_title, post_url, post_price, post_image_url))

        stuff_for_frontend = {
            'search': search,
            'final_postings': final_postings,
        }

        return render(request, 'my_app/new_search.html', stuff_for_frontend)
    return render(request, 'my_app/new_search.html')
