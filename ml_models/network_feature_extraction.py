import networkx as nx

def calculate_follower_following_ratio(followers, following):
    if following == 0:
        return float('inf')  # or a large number like 1000000
    return followers / following

def calculate_network_centrality(G, node):
    degree_centrality = nx.degree_centrality(G)[node]
    betweenness_centrality = nx.betweenness_centrality(G)[node]
    closeness_centrality = nx.closeness_centrality(G)[node]
    
    return {
        'degree_centrality': degree_centrality,
        'betweenness_centrality': betweenness_centrality,
        'closeness_centrality': closeness_centrality
    }

def calculate_clustering_coefficient(G, node):
    return nx.clustering(G, node)

def extract_network_features(user_id, followers, following, connections):
    G = nx.Graph()
    
    # Add nodes and edges based on the user's connections
    for connection in connections:
        G.add_edge(user_id, connection)
    
    follower_following_ratio = calculate_follower_following_ratio(followers, following)
    centrality_measures = calculate_network_centrality(G, user_id)
    clustering_coeff = calculate_clustering_coefficient(G, user_id)
    
    return {
        'follower_following_ratio': follower_following_ratio,
        'degree_centrality': centrality_measures['degree_centrality'],
        'betweenness_centrality': centrality_measures['betweenness_centrality'],
        'closeness_centrality': centrality_measures['closeness_centrality'],
        'clustering_coefficient': clustering_coeff
    }
