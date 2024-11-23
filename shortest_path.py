import networkx as nx
from math import sqrt

# Tính toán khoảng cách giữa 2 tỉnh liền kề
def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tạo ra đồ thị của bản đồ
def create_province_graph(southern_vietnam, provinces, adjacency_list):
    G = nx.Graph()
    for province in provinces:
        province_shape = southern_vietnam[southern_vietnam['NAME_1'] == province]
        coords = province_shape.geometry.centroid
        G.add_node(province, pos=(coords.x.iloc[0], coords.y.iloc[0]))
    # Danh sách khoảng cách các tỉnh
    weighted_adjacency_list = []
    for province1, province2 in adjacency_list:
        coord1 = G.nodes[province1]['pos']
        coord2 = G.nodes[province2]['pos']
        distance = calculate_distance(coord1, coord2)
        weighted_adjacency_list.append((province1, province2, distance))

    G.add_weighted_edges_from(weighted_adjacency_list)
    return G

# Tìm đường đi ngắn nhất 
def find_shortest_path(graph, start, end):
    try:
        return nx.shortest_path(graph, source=start, target=end, weight='weight')
    except nx.NetworkXNoPath:
        return []

def plot_shortest_path(ax, graph, path):
    coords = [graph.nodes[province]['pos'] for province in path]
    x, y = zip(*coords)
    return ax.plot(x, y, color='blue', linewidth=1, marker='o')