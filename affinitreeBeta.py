import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64
from IPython.display import display, HTML
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

data_path = "/Users/gabriellong/Documents/Decentralized Organization/Neuma_TCI_Score.csv"
df = pd.read_csv(data_path)

def assign_color(row_data):
    dominant_trait = max(row_data['HA Total'], row_data['NS Total'], row_data['RD Total'])

    if dominant_trait == row_data['HA Total']:
        return 'cyan'
    elif dominant_trait == row_data['NS Total']:
        return 'yellow'
    else:
        return 'magenta'


df['Color'] = df.apply(assign_color, axis=1)


def create_radial_bar_chart(df, node_index):
    values = df.loc[node_index, ['P Total', 'HA Total', 'NS Total', 'RD Total', 'SD Total', 'ST Total', 'CO Total']].values
    user_handle = df.loc[node_index, 'Identifier']

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

    temperament_legend.get_frame().set_linewidth(1)
    temperament_legend.get_frame().set_edgecolor('black')
    character_legend.get_frame().set_linewidth(1)
    character_legend.get_frame().set_edgecolor('black')

    buf = BytesIO()
    fig.canvas.print_png(buf)
    plt.close(fig)
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return encoded_image


columns_to_normalize = ['NS1', 'NS2', 'NS3', 'NS4', 'NS Total',
                        'HA1', 'HA2', 'HA3', 'HA4', 'HA Total',
                        'RD1', 'RD2', 'RD3', 'RD4', 'RD Total',
                        'P1', 'P2', 'P3', 'P4', 'P Total',
                        'SD1', 'SD2', 'SD3', 'SD4', 'SD5', 'SD Total',
                        'CO1', 'CO2', 'CO3', 'CO4', 'CO5', 'CO Total',
                        'ST1', 'ST2', 'ST3', 'ST Total']
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df[columns_to_normalize]), columns=columns_to_normalize)

cluster = AgglomerativeClustering(n_clusters=4, metric='euclidean', linkage='ward')
df['Role'] = cluster.fit_predict(df_normalized)

role_mapping = {0: 'Root', 1: 'Trunk', 2: 'Branch', 3: 'Leaf'}
df['Role'] = df['Role'].map(role_mapping)

df['Color'] = df.apply(assign_color, axis=1)

similarity_matrix = pairwise_distances(df_normalized)

mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
pos = mds.fit_transform(similarity_matrix)

mds_df = pd.DataFrame(pos, columns=['x', 'y'])

mds_df['Role'] = df['Role']
mds_df['Color'] = df['Color']

G = nx.Graph()

for index, current_row in mds_df.iterrows():
    identifier = df.loc[index, 'Identifier']
    G.add_node(identifier, role=current_row['Role'], color=current_row['Color'],
               **{'P Total': df.loc[index, 'P Total']})

layout = {node: (mds_df.loc[df[df['Identifier'] == node].index[0], 'x'],
                 mds_df.loc[df[df['Identifier'] == node].index[0], 'y']) for node in G.nodes()}


def get_node_trace(G, pos):
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2))
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple([G.nodes[node]['P Total']])
        node_info = f"{node}<br>Role: {G.nodes[node]['role']}<br>P Total: {G.nodes[node]['P Total']}"
        node_trace['text'] += tuple([node_info])

    return node_trace


def get_edge_trace(G, pos):
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    return edge_trace


node_trace = get_node_trace(G, layout)
edge_trace = get_edge_trace(G, layout)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(text='Affinitree', x=0.5),
                    titlefont=dict(size=26),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
)


# Main layout
app.layout = html.Div([
    dcc.Graph(id='affinitree', figure=fig),
    html.Img(id='radial-bar-chart', style={'width': '80%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
])


# Add click event to display individual radial bar chart
@app.callback(
    Output("radial-bar-chart", "src"),
    [Input("affinitree", "clickData")],
)
def display_radial_bar_chart(clickData):
    if clickData is None:
        raise PreventUpdate
    else:
        node_identifier = clickData["points"][0]["text"].split()[0]  # Extract Identifier from the text
        node_index = df[df['Identifier'] == node_identifier].index[0]
        encoded_image = create_radial_bar_chart(df, node_index)
        return f"data:image/png;base64,{encoded_image}"


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
