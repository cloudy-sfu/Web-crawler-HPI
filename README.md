# Web crawler HPI

 Web crawler for house price index and relevant economic indices

![](https://shields.io/badge/dependencies-Python_3.12-blue.svg)

## Introduction

There are two files related to each chart (denoted as `{index}`):

- `get_{index}.py` is the Python script to request data from the Internet.
- `results/{index}.csv` is the processed data.

The meaning of each chart is shown as follows.

| Name              | Reference                                                               | Description                                                                                                                                                                          |
| ----------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| nz_median_price   | https://www.interest.co.nz/charts/real-estate/median-price-reinz        | Monthly median house price in New Zealand                                                                                                                                            |
| nz_mortgage_rates | https://www.interest.co.nz/charts/interest-rates/mortgage-rates         | Simple average of all retail loan rates of each bank brand in New Zealand                                                                                                            |
| nz_cpi            | https://www.interest.co.nz/charts/prices/consumer-prices-index          | CPI: the rate of price change of goods and services purchased by households in New Zealand <br/>*Tradables and non-tradables are categorized by whether facing foreign competition.* |
| nz_anz_cpi        | https://www.interest.co.nz/charts/commodities/anz-commodity-price-index | CPI in New Zealand measured by ANZ Bank                                                                                                                                              |