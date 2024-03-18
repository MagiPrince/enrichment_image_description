from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api
import overpy
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

def search_from_pos_nodes(lat, long):

    nominatim = Nominatim()

    pos = nominatim.query(lat, long, reverse=True, zoom=20)
    tags_pos = []

    #print(pos.toJSON())
    for element in pos.toJSON():
        if 'town' in element['address']:
            # print(element['address']['town'])
            tags_pos.append(element['address']['town'])
        if 'state' in element['address']:
            # print(element['address']['state'])
            tags_pos.append(element['address']['state'])
        if 'postcode' in element['address']:
            # print(element['address']['postcode'])
            tags_pos.append(element['address']['postcode'])
        if 'country' in element['address']:
            # print(element['address']['country'])
            tags_pos += (element['address']['country']).split('/')
        if 'country_code' in element['address']:
            # print(element['address']['country_code'])
            tags_pos.append(element['address']['country_code'].upper())
        if 'building' in element['address']:
            # print(element['address']['building'])
            tags_pos.append(element['address']['building'])
    #print("------------------")

    # query = overpassQueryBuilder(bbox=[float(lat)-0.001, float(long)-0.001, float(lat)+0.001, float(long)+0.001], elementType='node[~"."~"."]', out='meta', includeGeometry=True)
    # overpass = Overpass()
    # busStops = overpass.query(query)
    # for element in busStops.toJSON()['elements']:
    #     if 'name' in element['tags']:
    #         #print(element['tags']['name'])
    #         tags_pos.append(element['tags']['name'])

    api = overpy.Overpass()

    result = api.query("[out:json];(node[~'.'~'.']({},{},{},{}););out;".format(float(lat)-0.001, float(long)-0.001, float(lat)+0.001, float(long)+0.001))
    for node in result.nodes:
        if 'name' in node.tags:
            for name in node.tags['name'].split(" - "):
                    tags_pos.append(name.title().replace(' ', ''))

    return tags_pos


# query = overpassQueryBuilder(bbox=[float(46.17554), float(6.139), float(46.17754), float(6.141)], elementType='node[~"."~"."]', out='json', includeGeometry=True)
# overpass = Overpass()
# busStops = overpass.query(query)
# print(busStops.toJSON()['elements'])
# for element in busStops.toJSON()['elements']:
#     if 'name' in element['tags']:
#         print(element['tags']['name'])


# array = []

# api = overpy.Overpass()

# result = api.query("[out:json];(node[~'.'~'.'](46.17554,6.139,46.17754,6.141););out;")
# for node in result.nodes:
#     if 'name' in node.tags:
#         for name in node.tags['name'].split(" - "):
#                 array.append(name.title().replace(' ', ''))