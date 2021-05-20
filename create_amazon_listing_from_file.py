import csv
import sys
from datetime import datetime
# fba_listing_and_shipment.py - Take a template file and fill out an FBA Uploader and an FBA-shipment template based on it
# takes in an All Listings report as the first argument

today = datetime.today().strftime("%m-%d-%Y")
def main():
    in_file_name = "newproductinput.csv"
    with open(in_file_name, newline = '') as infile:
        make_uploaders(infile)


def make_uploaders(infile):
    """Takes a new listing file and creates a filled out template to create both an Amazon
    Listing and shipments for it"""
    global today
    listing_out_file_name = "FBA-upload_template-"+today+".txt"
    shipment_out_file_name = "FBA-Shipment-Template-"+today+".txt"
    make_fba_uploader(infile,listing_out_file_name)
    make_shipment_uploader(infile,shipment_out_file_name)


def make_fba_uploader(infile,outfile_name):
    """With an open file, go to the top of the file and create an Amazon Listing template out of it"""
    PRICE_STR = "price"
    SKU_STR = "SKU"
    infile.seek(0)
    # These are fields that are either always going to be the same or
    # have default values
    LISTING_STATIC_FIELDS = {
    "product-id-type":"1",
    "item-condition":"11",
    "add-delete":"a",
    "batteries_required":"no",
    "supplier_declared_dg_hz_regulation1":"not_applicable",
    "fulfillment_center_id":"AMAZON_NA",
    # price is set to a very high $1,921 by default as a placeholder so that it won't sell before someone
    # has a chance to manually set it
    "price":"1921"
    }

    with open(outfile_name,'w',newline ='') as outfile:
        if len(sys.argv)>1:
            listing_report = sys.argv[1]
            # Current skus are pulled to prevent skus that already exist being relisted
            created_skus = pull_current_skus(listing_report)
        else:
            created_skus = []
        reader = csv.DictReader(infile, delimiter = ',')
        listing_writer = csv.DictWriter(outfile,delimiter ='\t',fieldnames = list(LISTING_STATIC_FIELDS.keys())+["product-id","sku"])
        listing_writer.writeheader()
        for row in reader:
            sku = row[SKU_STR]
            if sku in created_skus:
                continue
            outrow = LISTING_STATIC_FIELDS
            outrow["product-id"] = row["ASIN"]
            outrow["sku"] = sku
            # Sometimes we want to set a price manually instead of using the default price
            if row[PRICE_STR]:
                outrow[PRICE_STR] = row[PRICE_STR]
            listing_writer.writerow(outrow)

def make_shipment_uploader(infile,outfile_name):
    """Fills out an amazon shipping plan template file with an open file"""
    infile.seek(0)
    with open (outfile_name, 'w', newline='') as outfile:
        writer = csv.writer(outfile,delimiter = '\t')
        write_shipping_header(writer)
        reader = csv.DictReader(infile,delimiter = ',')
        for row in reader:
            quantity = row["Quantity"]
            sku  = row["SKU"]
            if quantity == "":
                quantity = "1"
            writer.writerow([sku,quantity])

def write_shipping_header(writer):
    """ Writes the header rows for a shipping plan file with an open writer. These rows are formatted entirely differently than the rest of the file"""
    global today
    TEMPLATE_FIELDS = ["PlanName","ShipToCountry","AddressName","AddressFieldOne","AddressFieldTwo","AddressCity","AddressCountryCode","AddressStateOrRegion","AddressPostalCode","AddressDistrict"]
    planName ="Test-Shipment-"+today
    template_values = [planName,"US","Michael Gallo","Fake-Street-Address","","Faker-City","US","NB","05555",""]
    out_file_name = "shipment_creator "+today+'.txt'
    for field,value in zip(TEMPLATE_FIELDS,template_values):
        writer.writerow([field,value])
    writer.writerow("")
    writer.writerow(["MerchantSKU","Quantity"])

def pull_current_skus(tab_file):
    """takes in a listing report from amazon and appends the Amazon fulfilled skus to a list"""
    sku_list = []
    with open(tab_file,newline = '',encoding = "utf-8-sig",errors = 'ignore') as f:
        for row in csv.DictReader (f, delimiter = '\t'):
            if row['fulfillment-channel'] == "AMAZON_NA":
                sku_list.append(row['seller-sku'])     
    return(sku_list)

if __name__ == '__main__':
    main()

