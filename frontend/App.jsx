import React, {Component} from 'react';
import {render} from 'react-dom';
import {Map, TileLayer, Marker, Popup} from 'react-leaflet';
import axios from 'axios';
import MarkerClusterGroup from 'react-leaflet-markercluster';

const tileProvider = 'http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
const mapCenter = [30.0444, 31.2357];
const zoomLevel = 17;
const scrollWheelZoom = false;

const MyPopupMarker = ({position, mcc, radio, range}) => (
    <Marker position={position}>
        <Popup>
            <p><strong>Radio:</strong> {radio}</p>
            <p><strong>MCC:</strong> {mcc}</p>
            <p><strong>Range:</strong> {range}m</p>
        </Popup>
    </Marker>
);

const MyMarkersList = ({markers}) => {
    if (markers.length === 0) {
        return (<div>/</div>);
    }

    const items = markers.map(({key, ...props}) => (
        <MyPopupMarker key={key} {...props} />
    ));
    return <MarkerClusterGroup>{items}</MarkerClusterGroup>
};

export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            api: {
                getCellTowers: 'http://localhost:5000/api/v1/cell_towers'
            },
            currentBounds: false,
            currentZoomLevel: zoomLevel,
            markers: []
        };
    }

    componentDidMount() {
        const leafletMap = this.leafletMap.leafletElement;

        leafletMap.panBy([0, 1]);

        this.setState({
            curentZoomLevel: leafletMap.getZoom(),
            currentBounds: leafletMap.getBounds()
        });

        this.getCellTowers();

        leafletMap.on('moveend', () => {
            let stateUpdater = {};
            const updatedBounds = leafletMap.getBounds();
            const updatedZoomLevel = leafletMap.getZoom();

            if (updatedZoomLevel !== this.state.currentZoomLevel) {
                console.log('Zoom level changed...');
                stateUpdater['currentZoomLevel'] = updatedZoomLevel;
            }

            if (updatedBounds !== this.state.currentBounds) {
                console.log('Bounds changed...');
                stateUpdater['currentBounds'] = updatedBounds;
            }

            if (Object.keys(stateUpdater).length > 0) {
                this.setState(stateUpdater);
                if (this.state.currentZoomLevel >= zoomLevel) {
                    this.getCellTowers();
                }
            }
        });
    }


    getCellTowers() {
        if (!this.state.currentBounds) {
            return false;
        }

        let northEastLat = this.state.currentBounds._northEast.lat;
        let northEastLng = this.state.currentBounds._northEast.lng;
        let southWestLat = this.state.currentBounds._southWest.lat;
        let southWestLng = this.state.currentBounds._southWest.lng;
        let bbox = northEastLng + ',' + northEastLat + ',' + southWestLng + ',' + southWestLat;

        axios
            .get(this.state.api.getCellTowers + '/' + bbox)
            .then(resp => {
                let coords = JSON.parse(resp.data);
                let newMarkers = [];
                coords.forEach(coord => {
                    newMarkers.push(
                        {
                            key: coord['id'],
                            mcc: coord['mcc'],
                            radio: coord['radio'],
                            range: coord['range'],
                            position: [coord['lat'], coord['lon']]
                        }
                    );
                });
                this.setState({markers: newMarkers});
            })

    }

    render() {
        return (
            <Map
                ref={
                    m => {
                        this.leafletMap = m;
                    }
                }
                center={mapCenter}
                zoom={zoomLevel}
                scrollWheelZoom={scrollWheelZoom}
            >
                <MyMarkersList markers={this.state.markers}/>
                <TileLayer url={tileProvider}/>
            </Map>
        );
    }
}

render(
    <App />,
    document.getElementById('root')
);
