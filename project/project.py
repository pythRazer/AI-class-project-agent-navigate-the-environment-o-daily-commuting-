from collections import defaultdict
import folium
from pprint import pprint
import os
import json

class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

edges_time = [
('home', 'imadegawa', 3),
('imadegawa', 'karasuma', 4),
('karasuma', 'yamashina', 12),
('karasuma', 'kyoto', 5),
('kyoto', 'yamashina', 5),
('yamashina', 'seta', 12),
('seta', 'seta_local_bus', 0),
('seta_local_bus', 'ritsumeikan', 18),
('seta', 'minami_kusatsu', 3),
('minami_kusatsu', 'shuttle_bus', 0),
('minami_kusatsu', 'panasonic', 0),
('minami_kusatsu', 'kakayaki', 0),
('panasonic', 'ritsumeikan', 25),
('kakayaki', 'ritsumeikan', 20),
('shuttle_bus', 'ritsumeikan', 15)
]

edges_money = [
('home', 'imadegawa', 0),
('imadegawa', 'karasuma', 0),
('karasuma', 'yamashina', 220),
('karasuma', 'kyoto', 0),
('kyoto', 'yamashina', 0),
('yamashina', 'seta', 0),
('seta', 'ritsumeikan', 320),
('seta', 'minami_kusatsu', 0),
('minami_kusatsu', 'shuttle_bus', 0),
('minami_kusatsu', 'panasonic', 0),
('minami_kusatsu', 'kakayaki', 0),
('panasonic', 'ritsumeikan', 230),
('kakayaki', 'ritsumeikan', 230),
('shuttle_bus', 'ritsumeikan', 180)
]

m = folium.Map(location=[35.028971, 135.757294], zoom_start=13)
home_imadegawa = os.path.join('home_ima.json')
imadegawa_karatsuma =  os.path.join('ima_karasuma.json')
karasuma_kyoto = os.path.join('karasuma_kyoto.json')
kyoto_yamashina = os.path.join('kyoto_yamashina.json')
yamashina_seta = os.path.join('yamashina_seta.json')
seta_minamikusatsu = os.path.join('seta_minami_kusatsu.json')
minamikusatsu_school = os.path.join('minami')
shuttle_bus = os.path.join('shuttle_bus.json')
seta_local_bus = os.path.join('seta_ritsumeikan.json')
kyoto_minami = os.path.join('kyoto_minami.json')

home = os.path.join('home.json')
imadegawa = os.path.join('imadegawa.json')
karasuma = os.path.join('karasuma.json')
kyoto = os.path.join('kyoto.json')
yamashina = os.path.join('yamashina.json')
seta = os.path.join('seta.json')
minamikusatsu = os.path.join('minami_kusatsu.json')
ritsumeikan = os.path.join('ritsumeikan.json')

def draw_route(path):
    m = folium.Map(location=[35.028971, 135.757294], zoom_start=13)

    if 'seta_local_bus' in path:
        folium.Marker(location=[35.028971, 135.757294],popup='home').add_to(m)
        folium.GeoJson(imadegawa, name='imadegawa').add_to(m)
        folium.GeoJson(karasuma, name='karasuma').add_to(m)
        folium.GeoJson(kyoto, name='kyoto').add_to(m)
        folium.GeoJson(yamashina, name='yamahsina').add_to(m)
        folium.GeoJson(seta, name='seta').add_to(m)
        folium.GeoJson(ritsumeikan, name='ritsumeikan').add_to(m)

        folium.GeoJson(home_imadegawa, name='home_ima').add_to(m)
        folium.GeoJson(imadegawa_karatsuma, name='imadegawa_karasuma').add_to(m)
        folium.GeoJson(karasuma_kyoto, name='karasuma_kyoto').add_to(m)
        folium.GeoJson(kyoto_yamashina, name='kyoto_yamashina').add_to(m)
        folium.GeoJson(yamashina_seta, name='yamashina_seta').add_to(m)
        folium.GeoJson(seta_local_bus, name='sseta_local_bus').add_to(m)
       
    if 'shuttle_bus' in path:
        folium.Marker(location=[35.028971, 135.757294],popup='home').add_to(m)
        folium.GeoJson(imadegawa, name='imadegawa').add_to(m)
        folium.GeoJson(karasuma, name='karasuma').add_to(m)
        folium.GeoJson(kyoto, name='kyoto').add_to(m)
        folium.GeoJson(yamashina, name='yamahsina').add_to(m)
        folium.GeoJson(seta, name='seta').add_to(m)
        folium.GeoJson(minamikusatsu, name='minamikusatsu').add_to(m)
        folium.GeoJson(ritsumeikan, name='ritsumeikan').add_to(m)

        folium.GeoJson(home_imadegawa, name='home_ima').add_to(m)
        folium.GeoJson(imadegawa_karatsuma, name='imadegawa_karasuma').add_to(m)
        folium.GeoJson(karasuma_kyoto, name='karasuma_kyoto').add_to(m)
        folium.GeoJson(kyoto_yamashina, name='kyoto_yamashina').add_to(m)
        folium.GeoJson(yamashina_seta, name='yamashina_seta').add_to(m)
        folium.GeoJson(seta_minamikusatsu, name='seta_minamikusatsu').add_to(m)
        folium.GeoJson(shuttle_bus, name='shuttle_bus').add_to(m)
    print("The route are drawn on the map, please open route.html in results folder to see the result")
    m.save(os.path.join('results', 'route.html'))


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    draw_route(path)
    return path, current_shortest_weight

graph = Graph()


def u_input():
    user_input = input('Enter 1 for fastest route, enter 2 for save money route:')
    if(user_input == '1'):
        for edge in edges_time:
            graph.add_edge(*edge)

        fastest_route = dijsktra(graph, start, end)
        print('Fastest route: ')
        print(fastest_route)
    elif(user_input == '2'):
        for edge in edges_money:
            graph.add_edge(*edge)
        money_route = dijsktra(graph, start, end)

        print('Save money route: ')
        print(money_route)
    else:
        u_input()


start = 'home'
end = 'ritsumeikan'
u_input()


