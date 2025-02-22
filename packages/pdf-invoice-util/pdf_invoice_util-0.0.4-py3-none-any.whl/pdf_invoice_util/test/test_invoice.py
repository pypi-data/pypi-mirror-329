import unittest

from datetime import datetime

from src.pdf_invoice_util import Config, Invoice


class TestInvoice(unittest.TestCase):

    def setUp(self):
        try:
            self.config = Config({'pdf':
                                   {'cell_width': 30,
                                    'cell_height': 4,
                                    'font': 'courier',
                                    'language': 'nl',
                                    'locale': 'nl_NL'
                                    },
                               'company':
                                   {'name': 'Your company',
                                    'address': 'Your street address 20',
                                    'postal_code': '1000',
                                    'city': 'Your city',
                                    'country': 'Your country',
                                    'vat_registered_number': 'Your registered vat number',
                                    'email': 'john@doe.com',
                                    'phone_1': '+01 234 567',
                                    },
                               'payment_details':
                                   {'bank_name': 'Your bank',
                                    'bank_iban': 'XX00 0000 0000 0000',
                                    'bank_bic': 'AAAAAAAA',
                                    'invoice_due_date': 30,
                                    'invoice_prefix': 'PRE',
                                    'vat': 25},
                               'date_format': '%B, %d %Y'}).load()
            self.invoice = Invoice(
                invoice_number=0,
                invoice_date='1980-01-01',
                customer_id=0,
                customer_name='John Doe',
                customer_address='Address line 1',
                customer_postal_code='BE1234',
                customer_city='City',
                customer_country='Country',
                customer_vat_registered_number='XX0000.000.000',
                vat_percentage=25,
                config=self.config)
        except Exception as e:
            self.fail(e)

    def tearDown(self):
        print(f'Invoice {self.invoice.__repr__()}')

    def test_set_articles(self):
        self.setUp()
        articles = [
            {'title': 'Article 1', 'price': 104.99, 'amount': 20},
            {'title': 'Article 2', 'price': 24.99, 'amount': 100},
            {'title': 'Article 3', 'price': 29.99, 'amount': 23},
        ]
        self.invoice.set_articles(articles)
        print(f'{self.invoice.get_articles()}')

    def test_invoice_number_valid(self):
        self.setUp()
        try:
            self.invoice.invoice_number = 1
        except TypeError as e:
            self.fail(e)
        self.assertEqual(self.invoice.invoice_number, int(1),
                         'invalid invoice_number type')

    @unittest.expectedFailure
    def test_invoice_number_invalid(self):
        self.setUp()
        try:
            self.invoice.invoice_number = 'C'
        except TypeError as e:
            self.fail(e)
        self.assertEqual(self.invoice.invoice_number, int('C', 4),
                         'invalid invoice_number type')
        print(f'Invoice invoice_number: {self.invoice.invoice_number}')

    def test_date_format_valid(self):
        self.setUp()
        try:
            self.invoice.set_invoice_date('1980-01-02')
            self.assertEqual(self.invoice.invoice_date,
                             datetime.strptime('1980-01-02', '%Y-%m-%d').strftime(self.config['date_format']),
                             'invalid date format')
        except ValueError as e:
            self.fail(e)

    @unittest.expectedFailure
    def test_date_format_invalid(self):
        self.setUp()
        try:
            self.invoice.set_invoice_date('2 January 1980')
            self.assertEqual(self.invoice.invoice_date,
                             datetime.strptime('2 January 1980', '%Y-%m-%d').strftime(self.config['date_format']),
                             'invalid date format')
        except ValueError as e:
            self.fail(e)

    def test_name_valid(self):
        self.setUp()
        try:
            self.invoice.customer_name = 'Doe John'
            self.assertEqual(self.invoice.customer_name, str('Doe John'),
                             'invalid name format')
        except Exception as e:
            self.fail(e)

    def test_address_valid(self):
        self.setUp()
        try:
            self.invoice.customer_address = 'Address street 1'
            self.assertEqual(self.invoice.customer_address, str('Address street 1'),
                             'invalid address format')
        except Exception as e:
            self.fail(e)

    def test_city_valid(self):
        self.setUp()
        try:
            self.invoice.customer_city = 'City'
            self.assertEqual(self.invoice.customer_city, str('City'),
                             'invalid city format')
        except Exception as e:
            self.fail(e)

    def test_postal_code_valid(self):
        self.setUp()
        try:
            self.invoice.customer_postal_code = '1000'
            self.assertEqual(self.invoice.customer_postal_code, str('1000'),
                             'invalid postal code format')
        except Exception as e:
            self.fail(e)

    def test_country_valid(self):
        self.setUp()
        try:
            self.invoice.customer_country = 'Belgium'
            self.assertEqual(self.invoice.customer_country, str('Belgium'),
                             'invalid country format')
        except Exception as e:
            self.fail(e)

    def test_vat_registered_number_valid(self):
        self.setUp()
        try:
            self.invoice.customer_vat_registered_number = 'YY0000.000.000'
            self.assertEqual(self.invoice.customer_vat_registered_number, str('YY0000.000.000'),
                             'invalid vat_registered_number format')
        except Exception as e:
            self.fail(e)

    def test_vat_percentage_valid(self):
        self.setUp()
        try:
            self.invoice.vat_percentage = 25
            self.assertEqual(self.invoice.vat_percentage, int(25),
                             'invalid vat_percentage format')
        except Exception as e:
            self.fail(e)

    @unittest.expectedFailure
    def test_vat_percentage_invalid(self):
        self.setUp()
        try:
            self.invoice.vat_percentage = '25%'
            self.assertEqual(self.invoice.vat_percentage, int('25%', 4),
                             'invalid vat_percentage format')
        except Exception as e:
            self.fail(e)
