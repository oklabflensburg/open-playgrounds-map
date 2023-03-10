fetch('./spielplaetze_flensburg.geojson', {
    method: 'GET'
})
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        marker(data);
    })
    .catch(function (error) {
        console.log(error);
    });

const map = L.map('map').setView([54.7836, 9.4321], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let geocoder = L.Control.Geocoder.nominatim();

if (typeof URLSearchParams !== 'undefined' && location.search) {
    // parse /?geocoder=nominatim from URL
    let params = new URLSearchParams(location.search);
    let geocoderString = params.get('geocoder');

    if (geocoderString && L.Control.Geocoder[geocoderString]) {
        console.log('Using geocoder', geocoderString);
        geocoder = L.Control.Geocoder[geocoderString]();
    } else if (geocoderString) {
        console.warn('Unsupported geocoder', geocoderString);
    }
}

const osmGeocoder = new L.Control.geocoder({
    query: 'Flensburg',
    position: 'topright',
    placeholder: 'Adresse oder Ort',
    defaultMarkGeocode: false
}).addTo(map);

osmGeocoder.on('markgeocode', e => {
    const bounds = L.latLngBounds(e.geocode.bbox._southWest, e.geocode.bbox._northEast);
    map.fitBounds(bounds);
});

function marker(data) {
    let markers = L.markerClusterGroup({
        zoomToBoundsOnClick: true,
        disableClusteringAtZoom: 18
    });

    const geojsonGroup = L.geoJSON(data, {
        onEachFeature: function (feature, layer) {
            layer.on('click', function (e) {
                document.getElementById('filter').scrollTo({
                    top: 0,
                    left: 0
                });

                map.setView(e.latlng, 19);

                let name = e.target.feature.properties.name
                let attributes = e.target.feature.properties.attributes
                let url = e.target.feature.properties.image
                let image = '';

                if (Array.isArray(attributes)) {
                    attributes = attributes.join(', ')
                }

                if (url.length > 0) {
                    image = '<img class="mt-1 mb-3" src="' + url + '" alt="Spielplatz">';
                }

                document.getElementById('details').classList.remove('hidden');
                document.getElementById('address').innerHTML = name;
                document.getElementById('attributes').innerHTML = attributes;
                document.getElementById('img').innerHTML = image;
            })
        },
        pointToLayer: function (feature, latlng) {
            let label = String(feature.properties.address);

            return L.marker(latlng).bindTooltip(label, {
                permanent: false,
                direction: 'top'
            }).openTooltip();
        }
    });

    markers.addLayer(geojsonGroup);
    map.addLayer(markers);
}