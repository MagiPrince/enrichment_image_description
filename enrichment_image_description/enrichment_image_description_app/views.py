
from django.http import HttpResponse
from django.shortcuts import redirect, render
from enrichment_image_description import settings
from .sparql_requests import *
from .osm import *
import flickrapi

# Create your views here.
def index(request):
    flickr = flickrapi.FlickrAPI(settings.flickr_api_key, settings.flickr_api_secret, format='parsed-json')
    #print(flickr.photos.getInfo(photo_id='43253825941'))
    context = {
        'error_message': False,
        'warning_message': False, 
    }
    if request.method == 'POST':
        if request.POST.get('fref', '') != '':
            try:
                api_response = flickr.photos.getInfo(photo_id=request.POST['fref'])
                flickr_response = {
                    'url': 'https://live.staticflickr.com/{}/{}_{}_b.jpg'.format(api_response['photo']['server'], api_response['photo']['id'], api_response['photo']['secret']), # api_response['photo']['urls']['url'][0]['_content'],
                    'tags_array': [element['_content'] for element in api_response['photo']['tags']['tag']] if 'tags' in api_response['photo'] else '',
                    'latitude': api_response['photo']['location']['latitude'] if 'location' in api_response['photo'] else '',
                    'longitude': api_response['photo']['location']['longitude'] if 'location' in api_response['photo'] else '',
                }
                request.session['flickr_response'] = flickr_response
                return redirect(visualizer)
            except Exception as e:
                print(e)
                context['error_message'] = True
        else:
            context['warning_message'] = True

    return render(request, 'index.html', context)


def visualizer(request):
    flickr_response = request.session.get('flickr_response')
    context = {
        'url': flickr_response['url'],
        'tags': flickr_response['tags_array'],
        'latitude': flickr_response['latitude'],
        'longitude': flickr_response['longitude'],
    }
    print(flickr_response['latitude'])
    return render(request, 'visualizer.html', context)


def results(request):
    tags = request.POST.getlist('tag')
    #tags = list(set(tags))
    flickr_response = request.session.get('flickr_response')
    
    # Algorithme
    lists_infered_tags = []
    for tag in tags:
        lists_infered_tags.append(concat_sparql_functions(tag))

    list_infered_tags_flattened = [tag for sublist in lists_infered_tags for tag in sublist]

    lat = flickr_response['latitude']
    long =  flickr_response['longitude']

    if lat != '' and long != '':
        list_infered_tags_flattened += search_from_pos_nodes(lat, long)

    list_infered_tags_flattened = list(set(list_infered_tags_flattened))

    new_infered_list = []

    for tag_infered in list_infered_tags_flattened:
        found = False
        for tag in tags:
            if tag.lower() == tag_infered.lower():
                found = True
        if not found:
            new_infered_list.append(tag_infered)

    context = {
        'url': flickr_response['url'],
        'tags': tags,
        'latitude': lat,
        'longitude': long,
        'enriched_tags': new_infered_list,
    }

    return render(request, 'results.html', context)