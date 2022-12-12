from django.shortcuts import render
from django.http import HttpResponse
import networkx as nx
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json
import numpy as np
from networkx.readwrite import json_graph
from django.http import JsonResponse

# Create your views here.


def index(request):
    G = nx.Graph()
    G.add_edge(1,2)
    return HttpResponse(G.nodes)

@api_view(['POST'])
def getMeasures(request):
    G = nx.Graph()
    x = list(request.body)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # body = dict(body)
    data = body['edges']
    for i in data:
        # print(i)
        edge = [(i['country1_name'],i['country2_name'],i)]
        G.add_edges_from(edge)

    b_val = betweenness(G)
    degree_val = degree(G)
    closeness_val = closeness(G)
    eigen_val = eigen(G)
    transitivity_val = transitivity(G)
    pageRank_val = pageRank(G)
    clustering_val = clustering(G)
    # cross_cliques = crossclique_centrality(data)
    di ={}
    di['betweenness'] = b_val
    di['degree_val'] = degree_val
    di['closeness_val'] = closeness_val
    di['eigen_val'] = eigen_val
    di['transitivity_val'] = transitivity_val
    di['pageRank_val'] = pageRank_val
    di['clustering_val'] = clustering_val
    # di['cross-clique'] = cross_cliques

    # print(cross_cliques)
    res=[]
    res.append(di)
    # print(np.matrix(res))
    return JsonResponse({'data':json.dumps(res)})




def betweenness(G):
    return nx.betweenness_centrality(G, weight='weight')

def degree(G):
    return nx.degree_centrality(G)

def closeness(G):
    return nx.closeness_centrality(G)

def eigen(G):
    return nx.eigenvector_centrality(G, weight='weight')

def transitivity(G):
    return nx.transitivity(G)

def pageRank(G):
    return nx.pagerank_numpy(G,weight='weight')

def clustering(G):
    return nx.clustering(G)
  
  #cross-clique
def getHash(edges):
    d={}
    for i in edges:
        country_name = i['country1_name']
        hashtag = i['attribute']
        if country_name in d:
            d[country_name].append(hashtag)
        else:
            d[country_name] = [hashtag]
    return d


def getLen(country,edges):
    d = getHash(edges)
    return len(d[country])


def crossclique_centrality(edges):
    cen = {}
    for i in edges:
        cen[i['country1_name']] = getLen(i['country1_name',edges])
    return cen
