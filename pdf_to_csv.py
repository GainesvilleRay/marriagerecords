

import pdftables_api
import creds

# convert pdf downloaded from county clerk site into csv
infile = 'Real Estate Search Results.pdf'
outfile = 'output.csv'

c = pdftables_api.Client(api_key)
c.csv(infile, outfile)
#replace c.csv with c.xlsx to convert to XLS
#replace c.xlsx with c.xml to convert to XML
#replace c.xlsx with c.html to convert to HTML
