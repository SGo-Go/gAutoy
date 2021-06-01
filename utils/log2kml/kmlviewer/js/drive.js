// <!-- https://code.google.com/p/geoxml3/wiki/Usage -->

var parser;
var filesList = ['input/track.kml', 'input/drpoints.kml'];

var routesVisible;

function completeInit() {
    routesVisible  = $("#routes_toggle").is(":checked");
    if (routesVisible) {
        parser.showDocument(parser.docs[0]);
    }
    else {
        parser.hideDocument(parser.docs[0]);
    }

    $("#routes_toggle").on("click", function(e) {
        // console.log("in #routes_toggle" + routesVisible);
	if (routesVisible) {
	    parser.hideDocument(parser.docs[0]);
	    routesVisible = false;
	} else {
	    parser.showDocument(parser.docs[0]);
	    routesVisible = true;
	}
    });
}

$(document).ready(function() {
    var latlng = new google.maps.LatLng(48.2002097089,11.6186728142);
    var mapOptions = {
	zoom: 16,
	center: latlng,
	mapTypeId: google.maps.MapTypeId.ROADMAP,
	mapTypeControlOptions: {
	    style: google.maps.MapTypeControlStyle.DEFAULT
	}
    };
    mapInstance = new google.maps.Map(document.getElementById("map"), mapOptions);

    parser = new geoXML3.parser({
	map: mapInstance,
	processStyles: true,
	singleInfoWindow: true,
	zoom: true,
    });

    google.maps.event.addListener(parser, 'parsed', completeInit);

    parser.parse(filesList);
});

// var container = document.getElementById("controls");

function readImagesAndPreview(files) {
    // filesList = filesList.concat(files); // filesList.push.apply(filesList, [4,5]);

    for(var i=0; i < files.length; i++) {
        var f = files[i];
        filesList.push(f.name)
    //     log.console(f);
        
    //     var reader = new FileReader();
        
    //     reader.onload = function(e) {
    //         var img = document.createElement("img");
    //         img.src = e.target.result;
    //         img.width = 100;
            
    //         container.appendChild(img);
    //     }
        
    //     reader.readAsDataURL(f);
    }
    console.log(filesList);
}
