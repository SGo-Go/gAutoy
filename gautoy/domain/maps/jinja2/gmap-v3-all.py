<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Polylines on Map</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

function initialize() {
    var locations = [
        {% for lbl in map.labels %} ["{{lbl._info}}", {{lbl.position[0]}}, {{lbl.position[1]}}, "{{lbl.icon_url}}"],
        {% endfor %}
    ];

    window.map = new google.maps.Map(document.getElementById('map'), {
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var bounds = new google.maps.LatLngBounds();

    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map,
            icon: locations[i][3] //locations[i][3]
        });

        bounds.extend(marker.position);

        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                infowindow.setContent(locations[i][0]);
                infowindow.open(map, marker);
            }
        })(marker, i));
    }

    var polylines = [
        {% for path in map.paths %}{% set pathsloop = loop %}
        // Path "{{path.name}}"
        [[{% for lat, lng in path.path %} [{{lat}}, {{lng}}],
          {% endfor %}
         ], '{{path.color}}', {{path.opacity}}, {{path.weight}}, "{{path._info}}</p>"],
        {% endfor %}
    ];

    for (i = 0; i < polylines.length; i++) {
        var polyline = polylines[i];
        var polylineCoordinates = [];
        for(j = 0; j < polyline[0].length; j++) {
            pathPointLatLng = {lat: polyline[0][j][0], lng: polyline[0][j][1] }
            polylineCoordinates.push(pathPointLatLng);
            bounds.extend(pathPointLatLng);
        }
        var polylinePath = new google.maps.Polyline({
            path: polylineCoordinates,
            geodesic: true,
            icons: [{
                icon: {path: google.maps.SymbolPath.FORWARD_OPEN_ARROW},
                offset: '100%'}],
            strokeColor:   polyline[1],
            strokeOpacity: polyline[2],
            strokeWeight:  polyline[3]
        });

        polylinePath.setMap(map);
        polylinePath.addListener('click', function (event) {
            infowindow.setContent(polyline[4]);
            infowindow.setPosition(event.latLng);
            infowindow.open(map);
        });
    }

    map.fitBounds(bounds);
}

function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' + 'callback=initialize';
    document.body.appendChild(script);
}

window.onload = loadScript;
    </script>
    <!-- <script async defer -->
    <!--     src="https://maps.googleapis.com/maps/api/js?callback=initMap"></script> -->
  </body>
</html>
<!-- template = """ """ -->
