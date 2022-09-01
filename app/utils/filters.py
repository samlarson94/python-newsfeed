# Create Custom Filters for Dates, URL Structure, and Plural Words

# Date Formatting
def format_date(date):
  return date.strftime('%m/%d/%y')

# URL Formatting
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# Plural Words Filter Function
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word

# Testing in Command Line
# from datetime import datetime
# print(format_date(datetime.now()))

# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))

# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))