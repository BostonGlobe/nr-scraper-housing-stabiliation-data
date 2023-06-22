# What is this?

This is a scraper that captures entry data from the Division of Housing Stabalization. It runs daily via github actions, capturing the four values found on [this page](https://hed-dhsentry.azurewebsites.net/default.aspx). The result of each day's scrape is recorded in a csv file within the `data` directory of this repo.

### How is it used?

The csv file is imported via an importdata function in google sheets to [this sheet](https://docs.google.com/spreadsheets/d/1HtS1Q4BOwq-diY3H6qPHHu_jvo6hW2TXcW7xEcisud8/edit?usp=sharing). Mike Damiano uses this data in the course of his reporting. 
 