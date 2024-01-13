import React, { useState, useRef, useCallback } from "react";
import getHumanDate from "./helper";

const DailyWeather = (props) => {
  const weather = props.weather;
  return (
    <div>
      <h1>Daily Weather</h1>
      <table>
        <thead>
          <tr>
            <th>Datetime</th>
            <th>Temperature</th>
            <th>Description</th>
            <th>Feels like</th>
            <th>Humidity</th>
            <th>Pressure</th>
            <th>Wind Speed</th>
          </tr>
        </thead>
        <tbody>
          {weather
            ? weather.map((el, index) => (
                <tr key={index}>
                  <td>{getHumanDate(el.dt)}</td>
                  <td>{el.temp.day}°C</td>
                  <td>{el.weather[0].description}</td>
                  <td>{el.feels_like.day}°C</td>
                  <td>{el.humidity}%</td>
                  <td>{el.pressure}</td>
                  <td>{el.wind_speed}m/s</td>
                </tr>
              ))
            : null}
        </tbody>
      </table>
    </div>
  );
};

const HourlyWeather = (props) => {
  const weather = props.weather;
  return (
    <div>
      <h1>Hourly Weather</h1>
      <table>
        <thead>
          <tr>
            <th>Datetime</th>
            <th>Temperature</th>
            <th>Description</th>
            <th>Feels like</th>
            <th>Humidity</th>
            <th>Pressure</th>
            <th>Wind Speed</th>
          </tr>
        </thead>
        <tbody>
          {weather
            ? weather.map((el, index) => (
                <tr key={index}>
                  <td>{getHumanDate(el.dt)}</td>
                  <td>{el.temp}°C</td>
                  <td>{el.weather[0].description}</td>
                  <td>{el.feels_like}°C</td>
                  <td>{el.humidity}%</td>
                  <td>{el.pressure}</td>
                  <td>{el.speed}m/s</td>
                </tr>
              ))
            : null}
        </tbody>
      </table>
    </div>
  );
};

const MinutelyWeather = (props) => {
  const weather = props.weather;
  return (
    <div>
      <h1>Weekly Weather</h1>
      <table>
        <thead>
          <tr>
            <th>Datetime</th>
            <th>Precipitation</th>
          </tr>
        </thead>
        <tbody>
          {weather
            ? weather.map((el, index) => (
                <tr key={index}>
                  <td>{getHumanDate(el.dt)}</td>
                  <td>{el.precipitation}°C</td>
                </tr>
              ))
            : null}
        </tbody>
      </table>
    </div>
  );
};

const CurrentWeather = (props) => {
  const weather = props.weather;
  return (
    <div>
      <h1>Current Weather</h1>
      <table>
        <thead>
          <tr>
            <th>Summary</th>
            <th>Datetime</th>
            <th>Temperature</th>
            <th>Description</th>
            <th>Feels like</th>
            <th>Humidity</th>
            <th>Pressure</th>
            <th>Wind Speed</th>
          </tr>
        </thead>
        <tbody>
          {weather ? (
            <tr>
              <td>{weather.name}</td>
              <td>{weather.dt}</td>
              <td>{weather.temp}°C</td>
              <td>{weather.weather[0].description}</td>
              <td>{weather.feels_like}°C</td>
              <td>{weather.humidity}%</td>
              <td>{weather.pressure}</td>
              <td>{weather.speed}m/s</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
};

const WeatherWidget = (props) => {
  const { data, detailing_type } = props;
  if (data === null) {
    return null;
  }
  if (detailing_type == "hourly") {
    return <HourlyWeather weather={data} />;
  }
  if (detailing_type == "daily") {
    return <DailyWeather weather={data} />;
  }
  if (detailing_type == "minutely") {
    return <MinutelyWeather weather={data} />;
  }
  if (detailing_type == "current") {
    return <CurrentWeather weather={data} />;
  }
  return null;
};

export default WeatherWidget;
