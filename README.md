## Affinitree Visualization Project

Table of Contents

1. [Affinitree](#affinitree)
2. [Mathematical Operations](#mathematical-operations)
   - [Normalization](#normalization)
   - [Distance Calculation](#distance-calculation)
   - [Dimensionality Reduction](#dimensionality-reduction)
3. [How to Run](#how-to-run)
4. [Acknowledgements](#acknowledgements)
5. [License](#license)

### Affinitree 

Affinitree is an interactive data visualization project that uses the Plotly Python graphing library. It utilizes a hierarchical clustering algorithm to categorize data and constructs a graph of interconnected nodes from the results. Each node represents an individual with certain character traits. By clicking on a node, a radial bar chart, which displays the individual's character traits, pops up.

This project consists of three files:

* 'affinitreeBeta.py': The primary Python script performing data preprocessing, clustering, graph creation, and radial bar chart generation.
* 'affinitree.js': A JavaScript file that enhances the interactivity of the Plotly graph.
* 'index.html': An HTML file that showcases the interactive graph, generated by affinitreeBeta.py.

### Mathematical Operations

The Affinitree visualization tool computes distances between individuals based on their TCI personality test scores. The process includes the following steps:

1. Normalization: The raw TCI scores are normalized using the MinMaxScaler from the sklearn library. This scaling transforms each score to a range between 0 and 1, which ensures that each dimension contributes equally to the distance calculation.

```
from sklearn.preprocessing import MinMaxScaler
columns_to_normalize = [...]  # List of columns to normalize
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df[columns_to_normalize]), columns=columns_to_normalize)
```

2. Distance Calculation: Pairwise distances are computed between every pair of individuals using the Euclidean distance metric. The pairwise_distances function from sklearn.metrics is used for this computation. The Euclidean distance formula is:

distance(P, Q) = sqrt((x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2)

where P and Q are the normalized TCI score vectors for two individuals.

```
from sklearn.metrics import pairwise_distances
similarity_matrix = pairwise_distances(df_normalized)
```

3. Dimensionality Reduction: Multidimensional scaling (MDS) is used to reduce the dimensionality of the data from the original number of TCI dimensions to two dimensions. This is achieved using the MDS function from the sklearn.manifold library. MDS aims to preserve the pairwise distances between the data points while reducing the dimensions, allowing for a meaningful visualization in 2D space.

```
from sklearn.manifold import MDS
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
pos = mds.fit_transform(similarity_matrix)
```
With these mathematical operations, the Affinitree Visualization tool calculates distances using the Euclidean distance formula and generates a 2D representation of the hierarchical data based on individuals' TCI personality test scores.

## How to Run

The project runs in Python 3.9 and requires the following libraries:

* pandas
* numpy
* networkx
* matplotlib
* scikit-learn
* plotly
* base64
* os

To run the project, follow these steps:

1. Install the required libraries. If you haven't installed these libraries yet, you can do so via pip:

```
pip install pandas numpy networkx matplotlib scikit-learn plotly base64 os
```

2. Run affinitreeBeta.py with Python:

```
python affinitreeBeta.py
```

The script will read the data from Neuma_TCI_Score.csv, perform hierarchical clustering, and generate an interactive graph visualization of the clustered data. The resulting Plotly figure is saved as index.html.

3. Open index.html in a web browser to view and interact with the graph. Click on a node to view a radial bar chart of the individual's personality traits.

The code is well-documented and can be easily customized. If you encounter any issues, make sure your Python environment has all the necessary packages installed. Feel free to reach out if you have any questions or suggestions.
Acknowledgements

This project is a creation by [Affinitree1 & Friends].
License

This project is licensed under the MIT License.