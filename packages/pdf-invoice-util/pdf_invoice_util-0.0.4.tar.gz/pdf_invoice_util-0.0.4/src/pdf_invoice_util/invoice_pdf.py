import locale
from dataclasses import dataclass

import yaml

from . import Invoice
from .pdf import PDF, XPos, YPos


@dataclass
class InvoicePDF(PDF):
    config: object
    invoice: Invoice

    def __init__(self, invoice, langcode, orientation='P', unit='mm', format='Letter'):
        self.config = invoice.config
        locale.setlocale(locale.LC_ALL, self.config['pdf']['locale'])
        self.invoice = invoice
        super().__init__(orientation, unit, format, self.invoice.invoice_id, self.config, langcode)
        self.set_page_title(self.translations['invoice'])
        try:
            with open(self.config['translations_path'] + 'terms.' + langcode + '.yaml', 'r') as terms_file:
                self.terms = yaml.safe_load(terms_file)
        except FileNotFoundError:
            self.terms = None

    def render_currency(self, amount):
        return locale.currency(amount, grouping=True, international=True, symbol=True)

    def generate_document(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font(self.config['pdf']['font'], '', size=9)

        # Supplier & client subheader
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['name'])
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'], self.invoice.customer_name,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['address'])
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.invoice.customer_address,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['postal_code'] + ' ' + self.config['company']['city'])
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  str(self.invoice.customer_postal_code) + ' ' + self.invoice.customer_city, new_x=XPos.LMARGIN,
                  new_y=YPos.NEXT)
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['country'])
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.invoice.customer_country,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['vat_registered_number'],
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                  self.config['company']['phone_1'],
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if 'phone_2' in self.config['company']:
            self.cell(self.config['pdf']['cell_width'] * 2, self.config['pdf']['cell_height'],
                      self.config['company']['phone_2'],
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.render_line_space()

        # Invoice details
        self.set_font(self.config['pdf']['font'], 'b', size=9)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                  self.translations['invoice_date'])
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                  self.translations['invoice_number'])
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                  self.translations['customer_vat_registered_number'])
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['customer_id'],
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font(self.config['pdf']['font'], '', size=9)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.invoice.invoice_date)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.invoice.invoice_id)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.invoice.customer_vat_number)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], str(self.invoice.customer_id),
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.render_line_space()

        # Invoice lines
        self.set_font(self.config['pdf']['font'], 'b', size=9)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['description'])
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['amount'])
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['price'],
                  align='R')
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['total_price'],
                  align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font(self.config['pdf']['font'], '', size=9)
        for article in self.invoice.articles:
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], article['title'])
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], str(article['amount']))
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      self.render_currency(article['price']),
                      align='R')
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      self.render_currency(article['amount'] * article['price']),
                      align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if article['description']:
                self.set_font(self.config['pdf']['font'], 'i', size=9)
                self.multi_cell(0, self.config['pdf']['cell_height'], article['description'],
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.set_font(self.config['pdf']['font'], '', size=9)

        # Totals
        subtotal = sum([article['amount'] * article['price'] for article in self.invoice.articles])
        vat_amount = subtotal * self.invoice.vat_percentage / 100

        self.render_line_space(1)

        if self.invoice.vat_percentage > 0:
            self.render_cell_spacer(2)
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      self.translations['subtotal'],
                      align='R')
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      str(self.render_currency(subtotal)),
                      align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            self.render_cell_spacer(2)
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      self.translations['vat_label'].format(str(self.invoice.vat_percentage)), align='R')
            self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                      str(self.render_currency(vat_amount)),
                      align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.render_cell_spacer(2)
        self.set_font(self.config['pdf']['font'], 'b', size=9)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'], self.translations['total'],
                  align='R')
        self.set_font(self.config['pdf']['font'], '', size=9)
        self.cell(self.config['pdf']['cell_width'], self.config['pdf']['cell_height'],
                  str(self.render_currency(subtotal + vat_amount)),
                  align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Payment info
        self.render_line_space(1)
        payment_info = self.translations['payment_info'].format(
            str(self.render_currency(subtotal + vat_amount)),
            self.config['payment_details']['bank_iban'],
            self.config['payment_details']['bank_bic'],
            self.invoice.invoice_id,
            self.config['payment_details']['invoice_due_date'])
        self.multi_cell(0, self.config['pdf']['cell_height'], payment_info + ' ' + self.translations[
            'terms_info'] if self.terms is not None else payment_info)

        if self.terms is not None:
            self.add_page()
            for term in self.terms:
                self.multi_cell(0, self.config['pdf']['cell_height'], term, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.render_line_space(1)

        super().generate_document()
