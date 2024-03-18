from SPARQLWrapper import SPARQLWrapper, JSON, GET
import copy
#from enrichment_image_description import settings


sparql_url_endpoint = 'http://127.0.0.1:7200/repositories/doggOntology'

def sparql_research_dog_bread(dog_bread):

    #sparql_url_endpoint = settings.sparql_url_endpoint
    sparql = SPARQLWrapper(sparql_url_endpoint)

    sparql.setReturnFormat(JSON)
    sparql.setMethod(GET)

    sparql_request_header = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ns0: <http://www.semanticweb.org/david/ontologies/2022/3/doggOntology#>
    """

    sparql_request = """
        {sparql_request_header}
        SELECT DISTINCT * WHERE {{
            {{?dog_class rdfs:subClassOf [ owl:hasValue "{dog_bread}" ;
                                                        owl:onProperty ns0:hasAlternativeLabel  ] .}}
            UNION
            {{?dog_class rdfs:subClassOf[ owl:hasValue "{dog_bread}" ;
                                                        owl:onProperty ns0:hasLabel  ] .}}
            FILTER(isUri(?dog_class) && STRSTARTS(STR(?dog_class), STR(ns0:)))
        }}

    """.format(sparql_request_header=sparql_request_header, dog_bread=dog_bread)

    #print(sparql_request)

    sparql.setQuery(sparql_request)

    results = sparql.query().convert()
    #print(results)

    if len(results['results']['bindings']) > 0:
        dog_class = results['results']['bindings'][0]['dog_class']['value']
        if len(results['results']['bindings']) > 1:
            dog_class = 'http://www.semanticweb.org/david/ontologies/2022/3/doggOntology#{}'.format(dog_bread)

        return dog_class
    
    # Return an empty array if there is no results
    return ''


def sparql_recursive_research_super_class(name_class):
    #sparql_url_endpoint = settings.sparql_url_endpoint
    sparql = SPARQLWrapper(sparql_url_endpoint)

    sparql.setReturnFormat(JSON)
    sparql.setMethod(GET)

    sparql_request_header = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ns0: <http://www.semanticweb.org/david/ontologies/2022/3/doggOntology#>
    """

    sparql_request = """
        {sparql_request_header}
        SELECT DISTINCT * WHERE {{
            {{ns0:{name_class} rdfs:subClassOf [ owl:someValuesFrom ?value ;
                                            owl:onProperty ?property  ]}}
            UNION
            {{ns0:{name_class} rdfs:subClassOf [ owl:hasValue ?value ;
                                            owl:onProperty ?property  ]}}
        }}

    """.format(sparql_request_header=sparql_request_header, name_class=name_class)

    sparql.setQuery(sparql_request)

    results = sparql.query().convert()

    if len(results['results']['bindings']) > 0:

        results_parsed = []

        # Parse the results in JSON to get an array with the value of super_class
        for result in results['results']['bindings']:
            if result['property']['value'] == 'http://www.semanticweb.org/david/ontologies/2022/3/doggOntology#comesFrom':
                results_parsed.append('comesFrom{}'.format(result['value']['value']))
            elif result['property']['value'].split('#')[-1] != 'hasAlternativeLabel':
                results_parsed.append(result['value']['value'])
            
            #results_parsed = [result['value']['value'] for result in results['results']['bindings'] if result['property']['value'].split('#')[-1] != 'hasAlternativeLabel']

        results_other = []

        for result in results_parsed:
            if len(result.split('#')) > 1:
                results_other+=sparql_recursive_research_super_class(result.split('#')[-1])
            else :
                results_other.append(result.replace(' ', ''))

        return list(set(results_other))
    
    # Return an empty array if there is no results
    return []


def sparql_research_super_class(name_class):

    #sparql_url_endpoint = settings.sparql_url_endpoint
    sparql = SPARQLWrapper(sparql_url_endpoint)

    sparql.setReturnFormat(JSON)
    sparql.setMethod(GET)

    sparql_request_header = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ns0: <http://www.semanticweb.org/david/ontologies/2022/3/doggOntology#>
    """

    sparql_request = """
        {sparql_request_header}
        SELECT DISTINCT * WHERE {{
            <{name_class}> rdfs:subClassOf ?super_class .
            FILTER(isUri(?super_class) && STRSTARTS(STR(?super_class), STR(ns0:)))
        }}

    """.format(sparql_request_header=sparql_request_header, name_class=name_class)

    #print(sparql_request)

    sparql.setQuery(sparql_request)

    results = sparql.query().convert()

    if len(results['results']['bindings']) > 0:
        
        # Parse the results in JSON to get an array with the value of super_class
        results_parsed = [result['super_class']['value'].split('#')[-1] for result in results['results']['bindings']]

        results_other = copy.deepcopy(results_parsed)

        for result in results_parsed:
            results_other+=sparql_recursive_research_super_class(result)

        return list(set(results_other))
    
    # Return an empty array if there is no results
    return []

def concat_sparql_functions(tag):
    tag = tag.lower().title()
    dog_class = sparql_research_dog_bread(tag)
    if dog_class != '':
        results = sparql_research_super_class(dog_class)

        return list(set(results))
    
    return []

