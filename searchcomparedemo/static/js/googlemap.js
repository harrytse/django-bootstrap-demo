/**
 * google map
 */
var map;
var marker;

function initialize(lastlng,lastlat) {
    var startPos = new google.maps.LatLng(lastlat,lastlng);
    var mapOptions = {
        zoom : 15,
        center : startPos,
        mapTypeId : google.maps.MapTypeId.ROADMAP
    };
    var image = '/static/img/marker-mini.png'
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    marker = new google.maps.Marker({
        position : startPos,
        map : map,
        icon: image
    });

    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng);
    });
}

function placeMarker(location) {
    marker.setPosition(location);
    document.getElementById('id_lng').value = location.lng();
    document.getElementById('id_lat').value = location.lat();
    document.getElementById('id_geoLatLng').value = "geo(gpoi,"+location.lng()+":"+location.lat()+",1000)"
    document.getElementById('id_distLatLng').value = "dist(gpoi,"+location.lng()+":"+location.lat()+")"

};


function setPosition() {
    var pos = new google.maps.LatLng(document.getElementById('id_lat').value,
            document.getElementById('id_lng').value);
    map.setCenter(pos);
    placeMarker(pos);
}

function findPosition(){

var word = document.getElementById('posWord').value;
var req = new XMLHttpRequest();
req.open('GET', "https://maps.google.com/maps/api/geocode/json?address="+word+"&sensor=true", false);
req.send(null);
var respnseBody = req.responseText

var json = '{"result":true,"count":1}',
obj = JSON.parse(respnseBody);

lat = obj.results[0].geometry.location.lat;
lng = obj.results[0].geometry.location.lng;

document.getElementById('id_lng').value = lat;
document.getElementById('id_lat').value = lng;






var pos = new google.maps.LatLng(lat,lng);
map.setCenter(pos);
placeMarker(pos);

}
/*
function resetPosition() {
    map.setCenter(startPos);
    placeMarker(startPos);
}*/