# commondata-countries

Work with [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1) [alpha2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2), [alpha3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) and [numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) standard country data.

List, lookup with fuzzy search, and synonyms.

## Installation

```bash
pip install commondata-countries
```

## Usage

**Iterate over all countries:**

```python
from commondata_countries import CountryData

countries = CountryData()

for country in countries:
    print(country.name)
```

**List all countries:**

```python
from commondata_countries import CountryData

countries = CountryData()

print(countries.all())
```

**Lookup a country**

```python
from commondata_countries import CountryData

countries = CountryData()

# Lookup by name (case insensitive, fuzzy search)
country = countries["Untied States of America"]

# Lookup by ISO Alpha-2
country = countries["US"]

# Lookup by ISO Alpha-3
country = countries["USA"]

# Lookup by ISO Numeric
country = countries[840]

# Lookup by synonym
country = countries["United States"]

# Look up with fuzzy search
country = countries["United Stat"]

print(country)
> Country(name='United States of America', iso_alpha2='US', iso_alpha3='USA', iso_numeric=840)
```

***Use CLI to lookup a country***

```bash
python -m commondata-countries United States
```

**Load countries data into pandas dataframe**

```python
import pandas as pd

from commondata_countries.data import countries

df = pd.DataFrame(countries)
```

## Other Formats and Datasets

Download CSV, XLSX, JSON and YAML files from [commondata.net/library](https://commondata.net/library/#countries).

[commondata.net](https://commondata.net) maintains a collection of essential datasets in a variety of formats, including
python bindings. Check out the full library here: [commondata.net/library](https://commondata.net/library).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request [here](https://github.com/commondata-net/commondata-countries-python).

## License

This project is licensed under GPLv3. See the [LICENSE](https://github.com/commondata-net/commondata-countries-python/blob/main/LICENSE) file for details.

## Support

For feedback, feature requests, or support, please email [support@commondata.net](mailto:support@commondata.net).
