/*var source = new ol.source.Vector({
  url: 'data.geojson',
  format: new ol.format.GeoJSON()
});*/

var features = new Array(1);
for (var i = 0; i < 1; ++i) {
  features[i] = new ol.Feature({
    'geometry': new ol.geom.Point(
        [-1.563389,47.210917]),
    'type': 'dechet'
  });
}

var view = new ol.View({
    center: [-1.563389, 47.210917],
    projection: 'EPSG:4326',
    zoom: 13,
})


var styles = {
  'dechet': new ol.style.Style({
    /*url: 'image/point.png'*/
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({color: '#0000CC'}),
      stroke: new ol.style.Stroke({color: '#FFFFFF', width: 1})
    })
  }),
  '20': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({color: '#666666'}),
      stroke: new ol.style.Stroke({color: '#bada55', width: 1})
    })
  })
  
};



var layers = [
  new ol.layer.Tile({
    source: new ol.source.XYZ({
      url: 'https://tile.jawg.io/d1272e85-8f6d-45fa-b74f-0bf372c6ecdf/{z}/{x}/{y}.png?access-token=7R3sFk6cRCKtNZ8SO9RwYnpZsGEUs48u4wQRlnbzJcC5M0TzX8mLIsboUE3URvq2'
    })
  }),
  new ol.layer.Vector({
    source: new ol.source.Vector({
        features: features,
        wrapX: false
      }),
    style: function(feature) {
      return styles[feature.get('type')];
    }
  }),
  source
];

var map = new ol.Map({
  target: document.getElementById('map'),
  layers: layers,
  view: view
});

var point = null;
var line = null;
var displaySnap = function(coordinate) {
  var closestFeature = vectorSource.getClosestFeatureToCoordinate(coordinate);
  if (closestFeature === null) {
    point = null;
    line = null;
  } else {
    var geometry = closestFeature.getGeometry();
    var closestPoint = geometry.getClosestPoint(coordinate);
    if (point === null) {
      point = new ol.geom.Point(closestPoint);
    } else {
      point.setCoordinates(closestPoint);
    }
    if (line === null) {
      line = new ol.geom.LineString([coordinate, closestPoint]);
    } else {
      line.setCoordinates([coordinate, closestPoint]);
    }
  }
  map.render();
};
/*
map.on('pointermove', function(evt) {
  if (evt.dragging) {
    return;
  }
  var coordinate = map.getEventCoordinate(evt.originalEvent);
  displaySnap(coordinate);
});

map.on('click', function(evt) {
  displaySnap(evt.coordinate);
});

var stroke = new ol.style.Stroke({
  color: 'rgba(255,255,0,0.9)',
  width: 3
});
var style = new ol.style.Style({
  stroke: stroke,
  image: new ol.style.Circle({
    radius: 10,
    stroke: stroke
  })
});
*/

/*
map.on('postcompose', function(evt) {
  var vectorContext = evt.vectorContext;
  vectorContext.setStyle(style);
  if (point !== null) {
    vectorContext.drawGeometry(point);
  }
  if (line !== null) {
    vectorContext.drawGeometry(line);
  }
});
map.on('pointermove', function(evt) {
  if (evt.dragging) {
    return;
  }
  var pixel = map.getEventPixel(evt.originalEvent);
  var hit = map.hasFeatureAtPixel(pixel);
  if (hit) {
    map.getTarget().style.cursor = 'pointer';
  } else {
    map.getTarget().style.cursor = '';
  }
});
*/