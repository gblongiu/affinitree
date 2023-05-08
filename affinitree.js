document.addEventListener('DOMContentLoaded', function () {
  var plotData = JSON.parse(document.getElementById('plot-data').textContent);

  var layout = plotData.layout;

  // Update layout to use window's inner width and height
  layout.width = window.innerWidth;
  layout.height = window.innerHeight;

  const config = {
    displayModeBar: false,  // The toolbar will be hidden at all times
    responsive: true
  };

  Plotly.newPlot('affinitree-plot', plotData.data, layout, config).then(function () {
    var plotDiv = document.getElementById('affinitree-plot');
    var nodeClicked = false;

    plotDiv.on('plotly_click', function (data) {
      nodeClicked = true;
      const pointIndex = data.points[0].pointIndex;
      const encodedImage = data.points[0].customdata;

      const imgData = "data:image/png;base64," + encodedImage;

      const img = document.createElement('img');
      img.src = imgData;
      img.style.width = '900px';

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

      modal.appendChild(img);

      document.body.appendChild(modal);

      modal.addEventListener('click', function () {
        document.body.removeChild(modal);
      });

      img.addEventListener('click', function (event) {
        event.stopPropagation();
      });
    });


    window.addEventListener('resize', function () {
      // Get the new window size
      var width = window.innerWidth;
      var height = window.innerHeight;

      // Update the layout with the new size
      var update = {
        width: width,
        height: height
      };

      // Restyle the plot with the new layout
      Plotly.relayout('affinitree-plot', update);
    });

  });
});