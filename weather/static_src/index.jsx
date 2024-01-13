import React, { useState, useRef, useCallback } from "react";
import ReactDOM from "react-dom/client";
import {
  useLoadScript,
  Marker,
  StandaloneSearchBox,
  StreetViewService,
  GoogleMap,
} from "@react-google-maps/api";
import WeatherWidget from "./components.jsx";
import getWeatherForecast from "./services.jsx";

const APP_CONFIG = Window.APP_CONFIG;
const DetailingTypeOptions = APP_CONFIG.DetailingTypeOptions || [];
const loaderId = "ownersTownGoogleMapApiId";
const config = {
  googleMapsApiKey: APP_CONFIG.GOOGLE_MAP_API_KEY,
  language: "en",
  region: "IN",
  version: "weekly",
  libraries: ["places"],
  preventGoogleFontsLoading: true,
  id: loaderId,
};

function App() {
  const { isLoaded, loadError } = useLoadScript(config);
  const Loading = <div>Loader</div>;
  const center = { lat: 12.972442, lng: 77.580643 };
  const [location, setLocation] = useState(center);
  const [detailingType, setDetailingType] = useState(
    DetailingTypeOptions[0][0]
  );
  const [weatherInfo, setWeatherInfo] = useState({});
  const markerRef = useRef(null);
  const mapRef = useRef(null);

  React.useEffect(() => {
    if (!location.lat || !location.lng || !detailingType) {
      return;
    }
    const fetchData = async () => {
      const weatherData = await getWeatherForecast(
        location.lat,
        location.lng,
        detailingType
      );
      setWeatherInfo(weatherData);
      return weatherData;
    };
    fetchData().catch(console.error);
  }, [detailingType, location]);

  function onClick(...args) {
    console.log("onClick args: ", args);
  }

  function setNewLocation() {
    console.log(mapRef.current.getPlaces());
  }

  function onPlacesChanged(...args) {
    console.log("onPlacesChanged args: ", args);
    setNewLocation();
  }

  function onDragEnd(...args) {
    console.log("onDragEnd args: ", args);
    console.log(
      markerRef.current.position.lat(),
      markerRef.current.position.lng()
    );
    setLocation({
      lat: markerRef.current.position.lat(),
      lng: markerRef.current.position.lng(),
    });
    // setNewLocation();
  }

  const onLoad = useCallback(
    (map) => {
      mapRef.current = map;
    },
    [onPlacesChanged]
  );

  const onMarkerLoad = useCallback(
    (marker) => {
      markerRef.current = marker;
      // const path = marker.getPath();
      console.log(marker);
    },
    [onDragEnd]
  );
  const onDetailingChange = (event) => {
    setWeatherInfo({});
    setDetailingType(event.target.value);
  };
  const weatherData = weatherInfo?.data;
  const renderMap = (
    <>
      <GoogleMap
        mapContainerStyle={{
          height: "500px",
          width: "100%",
        }}
        zoom={15}
        center={center}
        onClick={onClick}
      >
        <StandaloneSearchBox onLoad={onLoad} onPlacesChanged={onPlacesChanged}>
          <select
            placeholder="Detailing type"
            style={{
              boxSizing: "border-box",
              border: "1px solid transparent",
              width: "240px",
              backgroundColor: "#fff",
              height: "32px",
              padding: "0 12px",
              borderRadius: "3px",
              boxShadow: "0 2px 6px rgba(0, 0, 0, 0.3)",
              fontSize: "14px",
              outline: "none",
              textOverflow: "ellipses",
              position: "absolute",
              left: 0,
              right: 0,
              margin: "0 auto",
            }}
            onChange={(e) => onDetailingChange(e)}
          >
            {DetailingTypeOptions?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </StandaloneSearchBox>
        <Marker
          position={location}
          draggable
          clickable
          onDragEnd={onDragEnd}
          onLoad={onMarkerLoad}
        />
      </GoogleMap>
      <WeatherWidget data={weatherData} detailing_type={detailingType} />
    </>
  );

  if (loadError) {
    return <div>Map cannot be loaded right now, sorry.</div>;
  }

  return isLoaded ? renderMap : Loading;
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
