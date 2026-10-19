# Country Information Finder

## Overview

Country Information Finder is a Python application that integrates with the **World Bank Public API** to retrieve and display useful information about a country. It accepts a country name from the user, fetches external data, processes the JSON response, and displays selected information in a readable format.

This project demonstrates REST API integration, HTTP requests, JSON processing, input validation, and exception handling.

## Features

- Search for a country by name.
- Retrieve country information from the World Bank API.
- Display the country name, capital, population, region, and currency.
- Show the year associated with the latest available population value.
- Handle empty or invalid input.
- Handle API errors, network failures, timeouts, and unexpected responses.
- Allow repeated searches until the user chooses to exit.

## Used

- Python
- Requests library
- REST API
- JSON
- World Bank Open Data API

## API Used

**World Bank API:** https://api.worldbank.org/v2

The application uses the following endpoints:

- Country information: `/country?format=json&per_page=400`
- Population data: `/country/{country_code}/indicator/SP.POP.TOTL`

No API key is required.


