import requests
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
        # print(data)
        # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, features='html.parser')
        # Extracting all the <a> tags whose class name is 'result-title' into a list.
        post_listings = soup.find_all('li', {'class': 'result-row'})
        # print(post_listings, 'FINAL RESULTS LIST TEST!!!')
        # print(test_final_list[0].text)
        # print(post_listings[0].find('a').get('href'))
        # print(post_listings[0].find(class_='result-price').text)
        # print(post_listings[0].find(class_='result-title').text)
        # print(post_listings[0].find(class_='result-image').get('data-ids'))

        # post_title = post_listings[0].find(class_='result-title').text
        # post_url = post_listings[0].find('a').get('href')
        # post_price = post_listings[0].find(class_='result-price').text
        # post_image_id = post_listings[0].find(class_='result-image').get('data-ids')

        # currently working here...
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
                post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
            else:
                post_image_url = 'https://craigslist.org/images/peace.jpg'

            final_postings.append((post_title, post_url, post_price, post_image_url))

        print(final_postings, 'FINAL POSTINGS WOAH!!!')
        print(len(final_postings), 'that is the length!!!')
        print(final_postings[9], '9th item')

        # Need to build a post image URL.

        titles = soup.findAll('a', {'class': 'result-title'})

        prices = soup.findAll('span', {'class': 'result-price'})

        final_prices = []
        for price in prices:
            if price:
                final_prices.append(price.text)
            else:
                final_prices.append('N/A')

        print(final_prices, 'PRICES WOOHOO!!!!')

        images = soup.find_all("a", {"class": "result-image"})

        image_url = "https://images.craigslist.org/{}_300x300.jpg"

        final_image_urls = []
        for image in images:
            if image.get('data-ids'):
                # append the image URL to final images list
                final_image_urls.append(image_url.format((image.get('data-ids').split(',')[0].split(':')[1])))
            else:
                # append a "NOT AVAILABLE" image URL to final images list
                final_image_urls.append('https://craigslist.org/images/peace.jpg')

        print(final_image_urls)

        title_stuff = []
        for title, url, price in zip(titles, final_image_urls, final_prices):
            title_stuff.append((title.text, title.get('href'), url, price))

        print(title_stuff, '<--- STUFF!')

        stuff_for_frontend = {
            'title_stuff': title_stuff,
            'search': search,
            'final_postings': final_postings,
        }

        return render(request, 'my_app/new_search.html', stuff_for_frontend)
    return render(request, 'my_app/new_search.html')
