

import requests

BASE_URL = "https://api.worldbank.org/v2"


def get_country_info(country_name):
    if not country_name or not country_name.strip():
        print("Error: Country name cannot be empty.")
        return

    try:
        # Fetch the country list and find a matching country.
        response = requests.get(
            f"{BASE_URL}/country",
            params={"format": "json", "per_page": 400},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            print("Error: Unexpected response from the country API.")
            return

        countries = data[1]
        if not isinstance(countries, list):
            print("Error: Country data is unavailable.")
            return

        search_name = country_name.strip().casefold()

        matches = [
            country for country in countries
            if isinstance(country, dict)
            and country.get("name", "").casefold() == search_name
        ]

        if not matches:
            print("No matching country found. Check the country name.")
            return

        country = matches[0]
        country_code = country.get("id")

        if not country_code:
            print("Error: Country code is missing.")
            return

        # Fetch the latest available population value.
        pop_response = requests.get(
            f"{BASE_URL}/country/{country_code}/indicator/SP.POP.TOTL",
            params={"format": "json", "per_page": 100},
            timeout=15
        )
        pop_response.raise_for_status()
        pop_data = pop_response.json()

        if not isinstance(pop_data, list) or len(pop_data) < 2:
            print("Error: Unexpected population API response.")
            return

        population = None
        population_year = None

        if isinstance(pop_data[1], list):
            for item in pop_data[1]:
                if isinstance(item, dict) and item.get("value") is not None:
                    population = item["value"]
                    population_year = item.get("date")
                    break

        if population is None:
            population_text = "Unavailable"
        else:
            population_text = f"{population:,.0f}"

        capital = country.get("capitalCity") or "N/A"
        region_data = country.get("region", {})
        region = (
            region_data.get("value", "N/A")
            if isinstance(region_data, dict)
            else "N/A"
        )
        currency = country.get("currencyUnit") or "N/A"

        print("\n========== Country Information ==========")
        print(f"Name       : {country.get('name', 'N/A')}")
        print(f"Capital    : {capital}")
        print(f"Population : {population_text}")

        if population_year:
            print(f"Population year: {population_year}")

        print(f"Region     : {region}")
        print(f"Currency   : {currency}")
        print("==========================================")

    except requests.exceptions.Timeout:
        print("Network error: The API request timed out.")

    except requests.exceptions.ConnectionError:
        print("Network error: Could not connect to the API.")

    except requests.exceptions.HTTPError as error:
        print(f"API error: HTTP request failed ({error}).")

    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")

    except (ValueError, TypeError, KeyError, AttributeError):
        print("Error: The API returned invalid or unexpected data.")


def main():
    print("Welcome to Country Information Finder")

    while True:
        country_name = input(
            "\nEnter a country name (or type 'exit' to quit): "
        )

        if country_name.strip().lower() == "exit":
            print("Thank you for using Country Information Finder!")
            break

        get_country_info(country_name)


if __name__ == "__main__":
    main()
