document.addEventListener('DOMContentLoaded', function () {
  var plot_data = JSON.parse(document.getElementById('plot-data').textContent);

  Plotly.newPlot('affinitree-plot', plot_data.data, plot_data.layout).then(function () {
    var plotDiv = document.getElementById('affinitree-plot');
    var nodeClicked = false;  // Variable to track whether a node was clicked

    plotDiv.on('plotly_click', function (data) {
      nodeClicked = true;  // Set to true as this event only fires when a node is clicked
      // Existing node click handler code
      const pointIndex = data.points[0].pointIndex;
      const encodedImage = data.points[0].customdata;

      const imgData = "data:image/png;base64," + encodedImage;

      const img = document.createElement('img');
      img.src = imgData;
      img.style.width = '1000px'; // Set a larger width for the image

            // Create a modal
      const modal = document.createElement('div');
      modal.style.display = 'block';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
      modal.style.position = 'fixed';
      modal.style.top = 0;
      modal.style.left = 0;
      modal.style.zIndex = 9999;
      modal.style.textAlign = 'center';
      modal.style.paddingTop = '100px';

      // Add the image to the modal
      modal.appendChild(img);

      // Add the modal to the body
      document.body.appendChild(modal);

      // Close the modal when clicking outside of the image
      modal.addEventListener('click', function () {
        document.body.removeChild(modal);
      });

      // Prevent the modal from closing when clicking on the image
      img.addEventListener('click', function (event) {
        event.stopPropagation();
      });
    });

    // Event listener for clicks on the entire plot area
    plotDiv.addEventListener('click', function () {
      if (!nodeClicked) {  // If no node was clicked
        // Deselect the current node
        var update = {'selectedpoints': null};
        Plotly.restyle('affinitree-plot', update);
      }
      nodeClicked = false;  // Reset the variable for the next click
    });
  });
});

