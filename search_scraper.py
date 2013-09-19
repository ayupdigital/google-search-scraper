import twill, sys, os
from urlparse import urlparse
from StringIO import StringIO
from time import sleep

#
# CONFIGURATION
#
start_page      = 1
end_page        = 5
sleep_time      = 5
query           = "site:www.example.com"
query_url       = "http://www.example.com"


#
# START of script
#
screen_output   = sys.stdout
data_output     = StringIO()
page_links      = []
base_url        = "https://www.google.co.uk/search?q=" + query + "&start="
start_count     = (start_page - 1) * 10
end_count       = (end_page - 1) * 10

def scrape(url):

  global start_count, end_count, data_output, screen_output, query_url, page_links, sleep_time

  # Start configuring twill
  twill.commands.clear_cookies()
  twill.commands.agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36')
  twill.commands.go(url)

  # Ensure we get a 200 http status code back
  try:
    code_response = twill.commands.code(200)
  except:
    code_response = ""

  # Step into the html and extract the links
  if code_response is None:

    # Change sys output to capture output in a variable
    sys.stdout = data_output
    twill.set_output(data_output)

    # Grab the HTML data which will be stored in data_reponse
    twill.commands.showlinks()

    # Change the sys output back to the screen, now we have captured the data
    sys.stdout = screen_output
    twill.set_output(screen_output)

    # Split data up using new line char
    page_links_raw = data_output.getvalue().split("\n")

    # Loop through each row and look for a hyperlink
    for item in page_links_raw:

      # Find http in string
      httpString = item.find(query_url)

      # Add url to the array if not already
      if httpString is not -1:
        page_links.append(item[httpString:])

    # Goto the next page url
    start_count = start_count + 10;

    if start_count <= end_count:

      # Wait 5 seconds before visiting the next page
      sleep(sleep_time)

      # Recursive call, visit the next page
      init(base_url + str(start_count))



# Lets kick this shit off
scrape(base_url + str(start_count))

# Remove any duplicates
page_links = list(set(page_links))

# open for 'w'riting
f = open('data.txt', 'w')

# write text to file
for entry in page_links:
  print>>f, entry

# close the file
f.close()

# Print the final list of extracted url
print page_links

#
# END of script
#