document.addEventListener('DOMContentLoaded', function () {
  var plotData = JSON.parse(document.getElementById('plot-data').textContent);
  var layout = plotData.layout;

  layout.width = window.innerWidth;
  layout.height = window.innerHeight;
  layout.dragmode = false;  // Disable click and drag zooming

  const config = {
    displayModeBar: false,
    responsive: true,
    scrollZoom: false // Disable scroll zooming
  };

  // We double the data so that we can control visibility independently
  var traces = plotData.data.concat(plotData.data);

  Plotly.newPlot('affinitree-plot', traces, layout, config).then(function () {
    var plotDiv = document.getElementById('affinitree-plot');

    plotDiv.on('plotly_hover', function(data) {
      plotDiv.style.cursor = 'default';
    });

    plotDiv.on('plotly_click', function (data) {
      // Remove any existing modal if present
      const existingModal = document.getElementById('modal');
      if (existingModal) {
        document.body.removeChild(existingModal);
      }

      // If a point was clicked
      if (data.points.length > 0) {
        const pointIndex = data.points[0].pointIndex;
        const encodedImage = data.points[0].customdata

        const imgData = "data:image/png;base64," + encodedImage;

        const img = document.createElement('img');
        img.src = imgData;
        img.id = 'modal-image';
        img.style.maxWidth = '100%';
        img.style.maxHeight = '100%';
        img.style.position = 'absolute';
        img.style.left = '50%';
        img.style.top = '50%';
        img.style.transform = 'translate(-50%, -50%)';

        const modal = document.createElement('div');
        modal.id = 'modal';
        modal.style.display = 'flex';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        modal.style.position = 'fixed';
        modal.style.top = 0;
        modal.style.left = 0;
        modal.style.zIndex = 9999;

        modal.appendChild(img);

        document.body.appendChild(modal);

        modal.addEventListener('click', function () {
          document.body.removeChild(modal);
          // Reset marker opacity
          for (let i = 0; i < traces.length; i++) {
            Plotly.restyle('affinitree-plot', 'marker.opacity', [[1]], [i]);
          }
        });
      }

      // Reset trace selection
      for (let i = 0; i < traces.length; i++) {
          Plotly.restyle('affinitree-plot', 'selectedpoints', [null], [i]);
      }
    });

    plotDiv.on('plotly_unhover', function(data){
      plotDiv.style.cursor = 'pointer';
    });

    // Add an event listener for window resize to handle orientation changes
    window.addEventListener('resize', function() {
      // Update the layout dimensions
      layout.width = window.innerWidth;
      layout.height = window.innerHeight;

      // Resize the plot
      Plotly.relayout('affinitree-plot', layout);
    });

  });
});
