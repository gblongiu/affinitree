import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import base64
from io import BytesIO
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
from matplotlib.lines import Line2D
import json
import plotly.offline as pyo


print(os.getcwd())

# your data path
data_path = "/Users/gabriellong/Documents/Decentralized Organization/Neuma_TCI_Score.csv"
df = pd.read_csv(data_path)


# your function to assign color
def assign_color(row_data):
    dominant_trait = max(row_data['HA Total'], row_data['NS Total'], row_data['RD Total'])

    if dominant_trait == row_data['HA Total']:
        return 'cyan'
    elif dominant_trait == row_data['NS Total']:
        return 'yellow'
    else:
        return 'magenta'


# your function to create a radial bar chart
def create_radial_bar_chart(df, node_index):
    values = df.loc[
        node_index, ['P Total', 'HA Total', 'NS Total', 'RD Total', 'SD Total', 'ST Total', 'CO Total']].values
    user_handle = df.loc[node_index, 'Identifier']
    categories = ['P Total', 'HA Total', 'NS Total', 'RD Total', 'SD Total', 'ST Total', 'CO Total']
    n_categories = len(categories)

    rotation_offset = np.pi / 14
    angles = [(n / float(n_categories) * 2 * np.pi) + rotation_offset for n in range(n_categories)]
    angles += angles[:1]

    max_value = max(values)
    normalized_values = [value / max_value * 3 for value in values]

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'polar': True})

    custom_colors = ['#8B4513', '#FF0000', '#FFA500', '#FF69B4', '#0000FF', '#7E2F94', '#4CAF50']
    custom_colors_legend = ['#8B4513', '#FF0000', '#FFA500', '#FF69B4', '#4CAF50', '#7E2F94', '#0000FF']

    custom_lines = [Line2D([0], [0], color=color, lw=4) for color in custom_colors_legend]

    bars = []
    for i in range(n_categories):
        bars.append(ax.bar(angles[i], normalized_values[i], width=0.4, color=custom_colors[i], alpha=0.7))

    plt.xticks(angles[:-1], categories, fontsize=12, fontweight='bold', color='gray')
    ax.set_yticklabels([])

    ax.set_ylim(0, max(normalized_values) * 1.1)

    ax.set_facecolor('#F5F5F5')
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    plt.title(f"{user_handle}", fontsize=18, fontweight='bold', color='gray', y=1.1, x=0.7)

    temperament_labels = ["P: Persistence", "HA: Harm Avoidance", "NS: Novelty Seeking", "RD: Reward Dependence"]
    character_labels = ["CO: Cooperativeness", "ST: Self-Transcendence", "SD: Self-Directedness"]

    temperament_legend = ax.legend(custom_lines[:4], temperament_labels,
                                   bbox_to_anchor=(1.06, 0.84), loc='upper left', fontsize=12, title="Temperament",
                                   title_fontsize=14)

    temperament_title = temperament_legend.get_title()
    temperament_title.set_color('black')

    ax.add_artist(temperament_legend)

    character_legend = ax.legend(custom_lines[4:], character_labels,
                                 bbox_to_anchor=(1.09, 0.6), loc='upper left', fontsize=12, title="Character",
                                 title_fontsize=14)
    character_title = character_legend.get_title()
    character_title.set_color('black')

    for i in range(len(temperament_labels)):
        temperament_legend.texts[i].set_color('black')

    for i in range(len(character_labels)):
        character_legend.texts[i].set_color('black')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    buf.seek(0)
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    print(f"Image for node index {node_index} created with size {len(encoded_image)}")
    return encoded_image

# normalizing the data
columns_to_normalize = ['NS1', 'NS2', 'NS3', 'NS4', 'NS Total',
                        'HA1', 'HA2', 'HA3', 'HA4', 'HA Total',
                        'RD1', 'RD2', 'RD3', 'RD4', 'RD Total',
                        'P1', 'P2', 'P3', 'P4', 'P Total',
                        'SD1', 'SD2', 'SD3', 'SD4', 'SD5', 'SD Total',
                        'CO1', 'CO2', 'CO3', 'CO4', 'CO5', 'CO Total',
                        'ST1', 'ST2', 'ST3', 'ST Total']
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df[columns_to_normalize]), columns=columns_to_normalize)

# clustering
cluster = AgglomerativeClustering(n_clusters=4, metric='euclidean', linkage='ward')
df['Role'] = cluster.fit_predict(df_normalized)

# mapping role
role_mapping = {0: 'Root', 1: 'Trunk', 2: 'Branch', 3: 'Leaf'}
df['Role'] = df['Role'].map(role_mapping)

# assigning color
df['Color'] = df.apply(assign_color, axis=1)

# calculating similarity
similarity_matrix = pairwise_distances(df_normalized)

# applying MDS
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
pos = mds.fit_transform(similarity_matrix)

# creating the position dataframe
mds_df = pd.DataFrame(pos, columns=['x', 'y'])
mds_df['Role'] = df['Role']
mds_df['Color'] = df['Color']

# creating the graph
G = nx.Graph()

for index, current_row in mds_df.iterrows():
    identifier = df.loc[index, 'Identifier']
    G.add_node(identifier, role=current_row['Role'], color=current_row['Color'],
               **{'P Total': df.loc[index, 'P Total']})

# creating the layout
layout = {node: (mds_df.loc[df[df['Identifier'] == node].index[0], 'x'],
                 mds_df.loc[df[df['Identifier'] == node].index[0], 'y']) for node in G.nodes()}

# Define your get_edge_trace function here
def get_edge_trace(input_graph, input_layout):
    edge_x = []
    edge_y = []
    for edge in input_graph.edges():
        x0, y0 = input_layout[edge[0]]
        x1, y1 = input_layout[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    return go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='rgba(128, 128, 128, 0.5)', width=1))

# Then you can call your get_edge_trace function
edge_trace = get_edge_trace(G, layout)

# Get the node trace
def get_node_trace(input_graph, input_layout):
    node_x = []
    node_y = []
    node_colors = []
    node_text = []
    for node in input_graph.nodes():
        x, y = input_layout[node]
        node_x.append(x)
        node_y.append(y)
        node_colors.append(input_graph.nodes[node]['color'])
        node_text.append(f"{node} ({input_graph.nodes[node]['role']})")
    return go.Scatter(x=node_x, y=node_y, mode='markers', text=node_text, hoverinfo='text',
                      marker=dict(showscale=False, colorscale='YlGnBu', reversescale=True, color=node_colors,
                                  size=10, line_width=2))

node_trace = get_node_trace(G, layout)
node_trace['customdata'] = df.index.map(lambda x: create_radial_bar_chart(df, x), na_action=None)
edge_trace = get_edge_trace(G, layout)

# Update the hovertemplate
node_trace['hovertemplate'] = '<b>%{text}</b><br><extra></extra>'

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(text='Affinitree', x=0.5),
                    titlefont=dict(size=26),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    clickmode='event+select',
                    width=1400,  # Set the width
                    height=800))   # Set the height


fig.write_html('Affinitree_plot.html', full_html=False, include_plotlyjs='cdn')

# Save the plot as an HTML file
config = {'displayModeBar': True}
fig.write_html('Affinitree_plot.html', full_html=False, include_plotlyjs='cdn')

# Print the number of nodes in each role
role_counts = df['Role'].value_counts()
print(role_counts)

html_string = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Affinitree</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="affinitree-plot"></div>
    <div id="radial-chart-container"></div> <!-- Add this line -->
    <script id="plot-data" type="application/json">{fig.to_json()}</script>
    <script src="affinitree.js"></script>
</body>
</html>
"""



# Save the html_string to a file named Affinitree_plot.html
with open('Affinitree_plot.html', 'w') as f:
    f.write(html_string)

