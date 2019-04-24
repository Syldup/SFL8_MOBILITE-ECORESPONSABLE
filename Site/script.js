var map = new ol.Map({
  target: document.getElementById('map'),
	layers : [
	  new ol.layer.Tile({
		source: new ol.source.XYZ({
			url: 'https://tile.jawg.io/d5083f83-4b58-4bca-8a5c-c4888af10610/{z}/{x}/{y}.png?access-token=7R3sFk6cRCKtNZ8SO9RwYnpZsGEUs48u4wQRlnbzJcC5M0TzX8mLIsboUE3URvq2'
		})
	  })
	],
	   view : new ol.View({
		center: [-1.563389, 47.210917],
		projection: 'EPSG:4326',
		zoom: 13
	})
});
 new ol.layer.Vector({
   title: 'coordinates',
   source: new ol.source.Vector({
		url: 'data.geojson',
		format: new ol.format.GeoJSON()	 
   }),
   style: new ol.style.Style({
     image: new ol.style.Circle({
       radius: 5,
       fill: new ol.style.Fill({color: '#0000CC'})
     })
   })
 })
