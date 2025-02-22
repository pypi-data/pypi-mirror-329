import sys

from commondata_countries import CountryData


def main():
    country_data = CountryData()
    print(country_data[" ".join(sys.argv[1:])])


if __name__ == "__main__":
    main()
