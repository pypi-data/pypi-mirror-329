import unittest

from pathlib import Path

from src.pdf_invoice_util import InvoicePDF, Invoice, Config


class TestInvoicePDF(unittest.TestCase):
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
                                       'address': 'Your street address 1',
                                       'postal_code': 'PO0000',
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
                                  'date_format': '%B, %d %Y',
                                  'translations_path': '../../../translations/'}).load()
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
            self.invoice.set_articles([
                {'title': 'Article 1', 'price': 20, 'amount': 1},
                {'title': 'Article 2', 'price': 30, 'amount': 1},
                {'title': 'Article 3', 'price': 40, 'amount': 1},
            ])
        except Exception as e:
            self.fail(e)

    def tearDown(self):
        try:
            Path(('{0}/{1}.pdf').format(Path(__file__).parent.resolve().__str__(),
                                    self.invoice_pdf.output_filename)).unlink(missing_ok=True)
        except AttributeError as e:
            print(f'AttributeError: {e}')

    def test_create_invoice_pdf_nl_valid(self):
        self.create_invoice_pdf_valid('nl')

    @unittest.expectedFailure
    def test_create_invoice_pdf_nl_invalid(self):
        self.create_invoice_pdf_invalid('nl')

    def test_create_invoice_pdf_en_valid(self):
        self.create_invoice_pdf_valid('en')

    @unittest.expectedFailure
    def test_create_invoice_pdf_en_invalid(self):
        self.create_invoice_pdf_invalid('en')

    def create_invoice_pdf_valid(self, langcode):
        self.setUp()
        self.invoice.invoice_id = (self.config['payment_details']['invoice_prefix'] +
                                   ('{:02d}').format(0, langcode) + ('-{0}').format(langcode))
        self.invoice_pdf = InvoicePDF(self.invoice, langcode)
        self.invoice_pdf.generate_document()
        try:
            Path(('{0}/{1}.pdf').format(Path(__file__).parent.resolve().__str__(),
                                        self.invoice_pdf.output_filename)).resolve(strict=True)
        except FileNotFoundError:
            self.fail(f'Invoice {self.invoice_pdf.output_filename}.pdf does not exist')

    def create_invoice_pdf_invalid(self, langcode):
        self.setUp()
        self.invoice.invoice_id = (self.config['payment_details']['invoice_prefix'] +
                                   ('{:02d}').format(1, langcode) + ('-{0}').format(langcode))
        self.invoice_pdf = InvoicePDF(self.invoice, langcode, self.config)
        try:
            Path(('{0}/{1}.pdf').format(Path(__file__).parent.resolve().__str__(),
                                        self.invoice_pdf.output_filename)).resolve(strict=True)
        except FileNotFoundError:
            self.fail(f'Invoice {self.invoice_pdf.output_filename}.pdf does not exist')
