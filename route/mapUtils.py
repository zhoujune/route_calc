from posixpath import split
import requests
import re

KEY = 'apiKey=sXf-S7fTQa3en52D34u3kLAV5uRaYQTGKOQtFoXnd_4'

"""
Jun Zhou
2022/4/6
"""

def get_geocodes_from_addrs(addrs):
    """
    Return the gencodes as list given addrs string
    """

    addrs_list = addrs.split("\n")

    res = ''
    for addr in addrs_list:
        address = re.sub(r",", "+", addr, flags=re.UNICODE)
        address = re.sub(r"\s+", "+", addr, flags=re.UNICODE)
        rest_get_location = 'https://geocode.search.hereapi.com/v1/geocode?q='+address+'+'+'United_states&' + KEY
        r = requests.get(rest_get_location)
        data = r.json()
        print(str(data['items'][0]['position']['lat'])+","+str(data['items'][0]['position']['lng']))
        print(rest_get_location)
        res += str(data['items'][0]['position']['lat'])+","+str(data['items'][0]['position']['lng'])+"\n"
    return res


def get_distance_matrix(geocodes):
    """
    return the Euclidian distance matrix given geocodes list
    """
    geo_list = geocodes.split("\n")
    distance_matrix = [[0]*len(geo_list)]*len(geo_list)
    for i in range(len(geo_list)):
        for j in range(len(geo_list)):
            import math
            distance_matrix[i][j] = int(math.sqrt((int(geo_list[i].split(",")[0])-int(geo_list[j].split(",")[0]))**2+(int(geo_list[i].split(",")[1])-int(geo_list[j].split(",")[1])**2))*10000000)
    return distance_matrix

def get_location_matrix_tsp(geocodes):
    
    """
    return the Euclidian distance*10000 matrix given geocodes list, this is for easier calculation in TSP graph
    """
    geo_list = geocodes.split("\n")
    res = []
    for i in range(len(geo_list)):
        if len(geo_list[i]) == 0:
            break
        res.append([int(float(geo_list[i].split(",")[0])*100000), int(float(geo_list[i].split(",")[1])*100000)])
    return res

def get_location_matrix(geocodes):
    """
    return the location matrix (coordinate list for each location) given geocodes
    """
    geo_list = geocodes.split("\n")
    res = []
    for i in range(len(geo_list)):
        if len(geo_list[i]) == 0:
            break
        res.append([float(geo_list[i].split(",")[0]), float(geo_list[i].split(",")[1])])
    return res

def get_map_url_distance(geocodes):
    """
    given geocodes list, return a tuple that contains: mapURL, total distance and total time of the optimal path
    """
    path = get_tsp_path(get_location_matrix_tsp(geocodes))
    matrix = get_location_matrix(geocodes)
    map_api_address = 'https://image.maps.ls.hereapi.com/mia/1.6/routing?'+KEY
    map_api_options = '&lc=1652B4&lw=6&t=0&ppi=600&w=1000&h=400'
    distance_api_address = 'https://route.ls.hereapi.com/routing/7.2/calculateroute.xml?'+KEY
    distance_api_options = '&routeattributes=wp,sm,sh,sc&mode=shortest;car'
    for i in range(len(path)):
        lat = matrix[path[i]][0]
        lng = matrix[path[i]][1]
        map_api_address = map_api_address + "&waypoint"+str(i)+"="+str(lat)+","+str(lng)
        distance_api_address = distance_api_address + "&waypoint"+str(i)+"="+str(lat)+","+str(lng)
    map_api_address = map_api_address + "&waypoint"+str(len(path)) +"="+str(matrix[path[0]][0])+","+str(matrix[path[0]][1]) + map_api_options
    distance_api_address = distance_api_address + "&waypoint"+str(len(path)) +"="+str(matrix[path[0]][0])+","+str(matrix[path[0]][1]) + distance_api_options
    print(map_api_address)
    r = requests.get(distance_api_address)
    distance = int(r.text.split('<Distance>')[1].split('<')[0].split('.')[0])
    print(distance_api_address)
    
    time = r.text.split('<Text>')[1].split("&lt;span class=&quot;time&quot;&gt;")[1].split('&lt')[0]
    print(time)
    return map_api_address, distance, time



def get_tsp_path(data):
    """
    get the tsp optimal path using Christofides algorithm
    """
    G = build_graph(data)
    MSTree = minimum_spanning_tree(G)
    print("MSTree: ", MSTree)

    odd_vertexes = find_odd_vertexes(MSTree)
    minimum_weight_matching(MSTree, G, odd_vertexes)
    eulerian_tour = find_eulerian_tour(MSTree, G)

    current = eulerian_tour[0]
    path = [current]
    visited = [False] * len(eulerian_tour)

    length = 0

    for v in eulerian_tour[1:]:
        if not visited[v]:
            path.append(v)
            visited[v] = True

            length += G[current][v]
            current = v

    print("Result path: ", path)

    path=path[1:]
    path = path[path.index(0):]+path[:path.index(0)]
    print(path+[0])

    return path


def get_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1.0 / 2.0)


def build_graph(data):
    graph = {}
    for this in range(len(data)):
        for another_point in range(len(data)):
            if this != another_point:
                if this not in graph:
                    graph[this] = {}

                graph[this][another_point] = get_length(data[this][0], data[this][1], data[another_point][0],
                                                        data[another_point][1])

    return graph


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree


def find_odd_vertexes(MST):
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes


def minimum_weight_matching(MST, G, odd_vert):
    import random
    random.shuffle(odd_vert)

    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)


def find_eulerian_tour(MatchedMSTree, G):
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])


    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP


def remove_edge_from_matchedMST(MatchedMST, v1, v2):

    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST



