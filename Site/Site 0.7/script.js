var vectorSource = new ol.source.Vector();

var styles = {
  'a': new  ol.style.Style({
    image: new ol.style.Icon(/** @type {module:ol/style/Icon~Options} */ ({
          src: 'img/point.png'
        }))
  }),
  'b': new ol.style.Style({
    image: new ol.style.Icon(/** @type {module:ol/style/Icon~Options} */ ({
          src: 'img/co2.png'
        }))
  }),
}

var vector = new ol.layer.Vector({
   source: vectorSource
 })


 var center = ol.proj.transform([-1.563389, 47.210917], 'EPSG:4326', 'EPSG:3857');

 var map = new ol.Map({
  target: document.getElementById('map'),
  layers : [
    new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'https://tile.jawg.io/d5083f83-4b58-4bca-8a5c-c4888af10610/{z}/{x}/{y}.png?access-token=7R3sFk6cRCKtNZ8SO9RwYnpZsGEUs48u4wQRlnbzJcC5M0TzX8mLIsboUE3URvq2'
      })
    }),
    vector
  ],
     view : new ol.View({
    center: center,
    zoom: 13
  })
});

var element = document.getElementById('popup');

var popup = new ol.Overlay({
        element: element,
        positioning: 'bottom-center',
        stopEvent: false,
        offset: [0, -20]
      });
map.addOverlay(popup);

map.on('click', function(evt) {
  var feature = map.forEachFeatureAtPixel(evt.pixel,
    function(feature) {
      return feature;
    });
  if (feature) {
    var coordinates = feature.getGeometry().getCoordinates();
    popup.setPosition(coordinates);

    $(element).popover({
      placement: 'top',
      html: true,
      content: feature.get('msg')
    });
    $(element).popover('show');
  } else {
    $(element).popover('dispose');
  }
});

// change mouse cursor when over marker
map.on('pointermove', function(e) {
  if (e.dragging) {
    $(element).popover('dispose');
    return;
  }
  var pixel = map.getEventPixel(e.originalEvent);
  var hit = map.hasFeatureAtPixel(pixel);
  map.getTarget().style.cursor = hit ? 'pointer' : '';
});
