import axios from "axios";
const APP_CONFIG = Window.APP_CONFIG;

const getWeatherForecast = async (lat, lon, detailing_type) => {
  const data = await axios
    .get(APP_CONFIG.WEATHER_API_URL, {
      params: {
        lat,
        lon,
        detailing_type,
      },
    })
    .then((response) => response.data)
    .catch((error) => {
      console.log(error);
    });
  return data;
};

export default getWeatherForecast;
