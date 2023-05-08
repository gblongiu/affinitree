function updateImageSize(img) {
  if (window.innerWidth < 1024) { // Mobile devices
    if (window.innerWidth > window.innerHeight) { // Landscape orientation
      img.style.width = '70%';
    } else { // Portrait orientation
      img.style.width = '90%';
    }
  } else { // Desktop devices
    img.style.width = '900px';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const plotElement = document.getElementById('affinitree-plot');

  if (plotElement) {
    plotElement.on('plotly_click', function (data) {
      const pointIndex = data.points[0].pointIndex;
      const encodedImage = data.points[0].customdata;

      const imgData = "data:image/png;base64," + encodedImage;

      const img = document.createElement('img');
      img.src = imgData;

      updateImageSize(img);

      const radialChartContainer = document.getElementById('radial-chart-container');
      radialChartContainer.innerHTML = ''; // Clear previous radial chart
      radialChartContainer.appendChild(img);
    });

    // Resize radial chart on orientation change
    window.addEventListener('resize', function () {
      const img = document.querySelector('#radial-chart-container img');
      if (img) {
        updateImageSize(img);
      }
    });
  }
});
