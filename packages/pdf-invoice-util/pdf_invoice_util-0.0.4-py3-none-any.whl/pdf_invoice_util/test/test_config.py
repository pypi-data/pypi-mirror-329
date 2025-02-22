import unittest

from src.pdf_invoice_util import Config

config = {
    'pdf': {
        'cell_width': 30,
        'cell_height': 4,
        'font': 'verdana',
        'language': 'nl',
        'locale': 'nl_NL'
    },
    'company': {
        'name': 'Your company',
        'address': 'Your street address 20',
        'postal_code': '1000',
        'city': 'Your city',
        'country': 'Your country',
        'vat_registered_number': 'Your registered vat number',
        'email': 'john@doe.com',
        'phone_1': '+01 234 567',
    },
    'payment_details': {
        'bank_name': 'Your bank',
        'bank_iban': 'XX00 0000 0000 0000',
        'bank_bic': 'AAAAAAAA',
        'invoice_due_date': 30,
        'invoice_prefix': 'PREF',
        'vat': 25
    },
    'date_format': '%B, %d %Y'
}


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config(config)

    def test_update_valid(self):
        update = {'pdf': {'cell_width': 50}, 'date_format': '%d %B %Y'}
        self.config.update(update)
        for key, value in update.items():
            if type(value) is dict:
                for value_key, value_value in value.items():
                    self.assertEqual(self.config.load()[key][value_key], value_value,
                                     'invalid config update')
            else:
                self.assertEqual(self.config.load()[key], value,
                                 'invalid config update')

    @unittest.expectedFailure
    def test_update_invalid(self):
        update = {'pdf': {'cell_width': 50}, 'date_format': '%d %B %Y'}
        previous_value_1 = self.config.load()['pdf']['cell_width']
        previous_value_2 = self.config.load()['date_format']
        self.config.update(update)
        for key, value in update.items():
            if type(value) is dict:
                for value_key, value_value in value.items():
                    self.assertEqual(self.config.load()[key][value_key], previous_value_1,
                                     'invalid config update')
            else:
                self.assertEqual(self.config.load()[key], previous_value_2,
                                 'invalid config update')
