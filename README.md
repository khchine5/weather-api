# WEATHER APP

## Install:

```
make all
```

## Tests:

```
make sanity-check
make test
```

# Project:

- [x] Write the press release

# Settings:

Settings are shared between FE and BE.

- `WEATHER_API_KEY` : the weather API key
- `GOOGLE_MAP_API_KEY` : Google map API key to display the map.

# Notes:

- In order to use the Weather MAP API wisely , we the user requests for specific detailing type , the application will request all detailing types so if within the 10 minutes the user make a request for the same coordinates but with a different detailing type we can find it the data on our database.
- I am using [parcel](https://parceljs.org/) to build the js bundles which will be served by Django server. You can use the command `make build` and `make watch` to generate FE application bundles.
