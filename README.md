## AffiniTree Visualization Project

### Table of Contents

1. Overview
2. Features
3. Project Structure
4. Mathematical Operations
5. Installation and Usage
6. Contributing
7. License

### Overview

The AffiniTree Visualization project is a data visualization tool that utilizes interactive tree structures to represent hierarchical data. This tool is built primarily using Plotly.js, a JavaScript library that allows the creation of rich, interactive data visualizations. It also relies on Python for data processing and preparation, as well as HTML for web page structure.

### Features

* Interactive Tree Structure: The tree can be interactively manipulated by users. Clicking on a node will reveal an associated image, providing a deeper layer of information access.
* Image Pop-up: Clicking on a node will display a related image in a pop-up window.
* Node Deselection: Clicking anywhere outside the selected node will deselect it, providing a clean and intuitive user interface.

### Project Structure

The project consists of four primary files:

1. affinitreeBeta.py: This Python script is responsible for generating the data that forms the basis of the tree structure in the visualization. It prepares the data and encodes the associated images for use in the Plotly visualization.
2. index.html: This HTML file contains the primary structure and layout of the webpage. It includes the visualization plot and serves as the container for the Plotly chart.
3. affinitree.js: This JavaScript file handles the interactive aspects of the visualization. It communicates with the Plotly chart, handles node clicks, and manages the display of associated images.
4. Affinitree_plot.html: This is the HTML output generated from the Python script. It contains the final interactive tree plot which is displayed on the webpage. It is the culmination of the data prepared in affinitreeBeta.pyand the interactive features defined inaffinitree.js`.

### Mathematical Operations

The AffiniTree Visualization tool computes distances between individuals based on their TCI personality test scores. The process involves the following steps:

1. Normalization: The raw TCI scores are normalized using the MinMaxScaler from the sklearn library. This scales each score to a range between 0 and 1, which ensures that each dimension contributes equally to the distance calculation.

```
from sklearn.preprocessing import MinMaxScaler
columns_to_normalize = [...]  # List of columns to normalize
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df[columns_to_normalize]), columns=columns_to_normalize)
```

2. Distance Calculation: Pairwise distances are computed between every pair of individuals using the Euclidean distance metric. The pairwise_distances function from sklearn.metrics is used for this computation. The Euclidean distance formula is:

`distance(P, Q) = sqrt((x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2)`

* where P and Q are the normalized TCI score vectors for two individuals.

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

* With these mathematical operations, the AffiniTree Visualization tool computes distances using the Euclidean distance formula and generates a 2D representation of the hierarchical data based on individuals' TCI personality test scores.

### Installation and Usage

Before you begin, make sure you have Python (version 3.6 or higher) installed on your system.

You will need the following Python libraries:

* numpy
* pandas
* plotly
* base64
* PIL (Pillow)

You can install these libraries using pip:

#### pip install numpy pandas plotly base64 pillow

To use this tool:

1. Clone this repository or download the files.
2. Run the Python script (affinitreeBeta.py) to generate the data for your specific use case. Modify the script as needed to fit your data.
3. Open the Affinitree.html in a web browser to view the visualization. You should see the interactive tree structure generated from the data you provided.

#### Note: 
The Python script and HTML file must be in the same directory for the visualization to work correctly.

### Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page for open issues or create a new one. Please make sure to update tests as appropriate.

### License

This project is licensed under the terms of the MIT license.