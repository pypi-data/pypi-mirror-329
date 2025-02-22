import locale

from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Invoice:
    invoice_number: int
    invoice_date: str
    customer_id: int
    customer_name: str
    customer_address: str
    customer_postal_code: str
    customer_city: str
    customer_country: str
    customer_vat_registered_number: str
    vat_percentage: int
    invoice_language: str
    articles: List[object]

    def __init__(self,
                 invoice_number,
                 invoice_date,
                 customer_id: int,
                 customer_name: str,
                 customer_address: str,
                 customer_postal_code: str,
                 customer_city: str,
                 customer_country: str,
                 customer_vat_registered_number: str,
                 vat_percentage: int,
                 config=None):
        if config == None:
            from .config import Config
            config = Config().load()
        self.config = config
        self.invoice_number = invoice_number
        self.invoice_id = config['payment_details']['invoice_prefix'] + '{:02d}'.format(self.invoice_number)
        self.customer_id = customer_id
        self.customer_name: str = customer_name
        self.customer_address: str = customer_address
        self.customer_postal_code: str = customer_postal_code
        self.customer_city: str = customer_city
        self.customer_country: str = customer_country
        self.customer_vat_number: str = customer_vat_registered_number
        self.vat_percentage: int = vat_percentage
        try:
            locale.setlocale(locale.LC_ALL, self.config['pdf']['locale'])
            self.set_invoice_date(invoice_date)
        except ValueError as e:
            print(f'ValueError: {e}')
            exit()

    def __repr__(self):
        return ('<Invoice details: id={0}, date={1}>\n'
                '<Invoice customer details: id={2}, name={3}, address={4}, postal_code={5}, city={6}, country={7}, vat_number={8}, vat_percentage={9}>').format(
            self.invoice_id, self.invoice_date, self.customer_id, self.customer_name, self.customer_address,
            self.customer_postal_code, self.customer_city, self.customer_country, self.customer_vat_number,
            self.vat_percentage)

    def set_invoice_date(self, invoice_date):
        self.invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d').strftime(self.config['date_format'])

    def set_articles(self, articles):
        self.articles = articles

    def get_articles(self):
        return ('<Invoice articles: {0}>').format(
            [[article['title'], article['price'], article['amount'], article['description']] for article in self.articles])
