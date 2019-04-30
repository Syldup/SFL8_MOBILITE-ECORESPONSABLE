
var vectorSource = new ol.source.Vector();

var vector = new ol.layer.Vector({
   title: 'coordinates',
   source: vectorSource,
   style: new ol.style.Style({
     image: new ol.style.Circle({
       radius: 5,
       fill: new ol.style.Fill({color: '#0000CC'})
     })
   })
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

function updatePoint(data) {
      // we need to transform the geometries into the view's projection
      var transform = ol.proj.getTransform('EPSG:4326', 'EPSG:3857');
      // loop over the items in the response
      data.items.forEach(function(item) {
        // create a new feature with the item as the properties
        var feature = new ol.Feature(item);
        // add a url property for later ease of access
        feature.set('url', item.media.m);
        // create an appropriate geometry and add it to the feature
        var coordinate = transform([parseFloat(item.x), parseFloat(item.y)]);
        var geometry = new ol.geom.Point(coordinate);
        feature.setGeometry(geometry);
        // add the feature to the source
        vectorSource.addFeature(feature);
      });
    }
	
$.ajax({
  url: 'data.json',
  dataType: 'json',
  //jsonpCallback: 'jsonFlickrFeed',
  success: updatePoint
});
