# Python interface for invoice generation
Simple utility for PDF invoice generation in Python

## Setup
1. Install the module ```pip install pdf-invoice-util```
2. Copy ```config/config.example.yaml``` from the repository to ```config/config.yaml``` and update parameter values as desired
3. Optionally configure terms by creating a ```translations/terms.[language].yaml``` file, check out the example file ```config/terms.example.yaml```

## Usage
1. Import the module ```from pdf_invoice_util import Invoice, InvoicePDF```
2. Generate an invoice object eg. ```invoice = Invoice(invoice_id, invoice_date <YY-mm-dd>, customer_id, customer_name, customer_address, customer_postal_code, customer_city, customer_country, customer_vat_registered_number, vat_percentage)```
3. Set article lines by using the ```set_articles()``` method on the invoice object, eg. ```invoice.set_articles([{'name': 'Pizza margherita', 'price': 9.99, 'amount': 1}, {'name': 'Pizza fungi', 'price': 11.99, 'amount': 1}])```
4. Generate an InvoicePDF object eg. ```pdf = InvoicePDF(invoice <the invoice object>, invoice_language <the desired print language>)```
5. Generate the PDF by running the ```generate_document()``` method on the InvoicePDF object

## Translations
Translations can be overwritten by copying the translation file into /translations folder

## Contribution
Feel free or make proposals for code contributions and the addition of translation files for additional language support in this repository

## Credits
Big thanks to Pluralsight (https://www.pluralsight.com) and Chart Explorers (https://www.youtube.com/@ChartExplorers) for the detailed descriptions on working with the used techniques