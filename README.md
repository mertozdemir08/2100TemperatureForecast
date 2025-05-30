# Temperature Forecasting and Climate Risk Classification (2100 Projection)

This project aims to predict average global temperature increases for the year 2100 using demographic and environmental attributes of countries. Based on Ridge regression modeling and IPCC climate risk thresholds, countries are classified into risk levels to assess their vulnerability to climate change.

## Objective

To estimate the average temperature increase for each country in the year 2100 using past data (1980–2013), and classify countries into four IPCC-based risk categories:  
- **Low Risk** (0–1°C)  
- **Medium Risk** (1–1.5°C)  
- **High Risk** (1.5–2°C)  
- **Very High Risk** (>2°C)

## Methods

- **Model**: Ridge regression with polynomial features (degree=1)
- **Features used**: Year, average temperature, population, population density, MtCO₂ emissions, nitrous oxide emissions, continent
- **Data range**: 1980–2013 (due to post-industrial warming trends and dataset intersection)
- Countries with sufficient historical data were modeled individually
- Forecasts are compared with 2013 temperatures to compute risk scores

## Risk Classification Logic

Thresholds are based on IPCC's 2018 & 2023 reports and supported by NASA and UNEP:
- 1.5°C marks the beginning of irreversible effects
- 2°C or more is considered extremely dangerous, especially for vulnerable regions

## Tools and Technologies

- Python (pandas, scikit-learn)
- Ridge regression modeling
- Data processing and transformation with pipelines
- Excel reporting of prediction and risk levels

## Output

An Excel file was generated that includes:
- Country-level temperature forecasts for 2100
- Risk level assigned to each country
- A summary sheet showing the number of countries per risk level

## Proposed Solutions (Based on Results)

Recommendations are provided by continent, focusing on:
- Water management and agricultural adaptation (Africa, Asia)
- Urban planning and emission reduction (Europe, South America)
- Renewable energy and early warning systems

## License

This project is licensed under the MIT License.

## References

Key data sources and reports include:
- [IPCC 2018 Special Report on Global Warming of 1.5°C](https://www.ipcc.ch/sr15/)
- [IPCC 2023 AR6 Synthesis Report](https://www.ipcc.ch/report/ar6/syr/)
- [NASA Climate Change Evidence](https://climate.nasa.gov/evidence/)
- [Global Carbon Atlas – Emissions](https://globalcarbonatlas.org/)
- [Gapminder Population Data](https://www.gapminder.org/data/documentation/gd003/)
- [UNEP Emissions Gap Report 2023](https://www.unep.org/resources/emissions-gap-report-2023)
- [Kaggle Datasets: Population, Emissions, Continents, Migration]
