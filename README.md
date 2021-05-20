# Amazon Listing Template Creator

This program takes a csv file with product data and creates two templates, an FBA upload template to create Amazon listings and an FBA-Shipment template to send product into Amazon. 

## Instructions
Fill out "newproductinput.csv"; ASIN, SKU, quantity, and price are the only fields that matter. Run "python create_amazon_listing_from_file.py" from the command line to create the templates. If you have an Amazon listing report, named 'test_amazon_listing_report.txt' in this example, run "python create_amazon_listing_from_file test_amazon_listing_report" instead and products that you already have listed on Amazon as FBA listings will be skipped for the FBA upload template


## Dependencies 
- Python 3
- Datetime python module
