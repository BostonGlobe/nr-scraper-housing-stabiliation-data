import requests
from csv import DictWriter
from bs4 import BeautifulSoup

global report_table, final_row

field_names = ['txtEntryDate', 'txtNewlyEligible', 'txtDirect', 'txtPresumptive', 'txtMotelFamilies']

HEADERS = {
  'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'),
  'accept-language': 'he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4',
  'cache-control': 'max-age=0'
}

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

print(final_row[0], data['txtEntryDate'])
if data['txtEntryDate'] not in final_row:
  with open('data/housing-stabilization.csv', 'a') as data_object:
    dictwriter_object = DictWriter(data_object, fieldnames=field_names)
    dictwriter_object.writerow(data)
  

