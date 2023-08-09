import requests
from csv import DictWriter
from bs4 import BeautifulSoup
from datetime import datetime

global report_table, final_row

field_names = {
  "txtEntryDate": "Date",
  "txtNewlyEligible": "Newly eligible families",
  "txtDirect": "Directly placed families",
  "txtPresumptive": "Presumptively placed families",
  "txtMotelFamilies": "Families placed in motels"
}

HEADERS = {
  'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'),
  'accept-language': 'he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4',
  'cache-control': 'max-age=0'
}

def parse_date(date: str):
  """Parses a string date

    e.g. "Tuesday, August 8, 2023" --> "8/8/2023"

  Args:
      date (str): The date to parse
  Returns:
      str: The parsed date
  """
  parsed_date = datetime.strptime(date, "%A, %B %d, %Y")
  # Format the date in the desired output format
  return parsed_date.strftime("%-m/%-d/%Y")

request = requests.get('https://hed-dhsentry.azurewebsites.net/default.aspx', HEADERS)

page_content = BeautifulSoup(request.text, 'html.parser')

report = ''

report = page_content.find('div', {'id': 'DHS_Display'})
if report != None:
  report_table = report.find('table')
else:
  report_table = page_content.find('table')


report_rows = report_table.find_all('tr')

data = {}

for row in report_rows:
  cell = row.find('td')
  input = cell.find('input')

  if input != None:
    input_type = input.get('name')
    input_value = input.get('value')

    data[input_type] = input_value

with open('data/housing-stabilization.csv', 'r') as data_object:
  final_row = data_object.readlines()[-1]
  print(final_row)

data["txtEntryDate"] = parse_date(data["txtEntryDate"])  # Parse the date to the desired format
print(final_row[0], data['txtEntryDate'])
if data['txtEntryDate'] not in final_row:
  data = {field_names[key]: value for (key, value) in data.items()}  # Rename the keys to human-readable format
  with open('data/housing-stabilization.csv', 'a') as data_object:
    dictwriter_object = DictWriter(data_object, fieldnames=field_names.values())
    dictwriter_object.writerow(data)
  

