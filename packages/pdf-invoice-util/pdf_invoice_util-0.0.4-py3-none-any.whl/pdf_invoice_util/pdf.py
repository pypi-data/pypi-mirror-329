from pathlib import Path

import yaml

from fpdf import FPDF, XPos, YPos


class PDF(FPDF):
    def __init__(self, orientation, unit, format, output_filename, config, langcode=None):
        self.config = config
        super().__init__(orientation, unit, format)
        if langcode == None:
            langcode = self.config['pdf']['language']
        self.output_filename = output_filename
        translations_filename = f'language.{langcode}.yaml'
        try:
            translations_file_path = Path(f'{self.config['translations_path']}{translations_filename}').resolve(strict=True)
        except FileNotFoundError:
            translations_file_path = Path(('{0}/translations/{1}').format(
                Path(__file__).parent.resolve().__str__(),
                translations_filename)).resolve()
        with open(translations_file_path.__str__(), 'r') as translations_file:
            self.translations = yaml.safe_load(translations_file)

    def set_page_title(self, page_title):
        self.page_title = page_title

    def header(self):
        try:
            if 'logo' in self.config['pdf'] and Path(f'{self.config['pdf']['logo']}').resolve(strict=True):
                self.image(self.config['pdf']['logo'], 10, 10, 20)
        except FileNotFoundError as e:
            print(f'Logo not found: {e}')
        self.set_font(self.config['pdf']['font'], '', size=29)
        self.cell(0, self.config['pdf']['cell_height'] * 2, self.page_title, border=False, align='C',
                  new_x=XPos.LMARGIN)
        self.ln(25)

    def footer(self):
        self.set_y(-10)
        self.set_font(self.config['pdf']['font'], '', size=6)
        self.cell(0, self.config['pdf']['cell_height'], f'{self.translations['page']} {self.page_no()}/{{nb}}',
                  align='C')

    def render_line_space(self, cells=2):
        return self.cell(self.config['pdf']['cell_width'] * cells, self.config['pdf']['cell_height'], '',
                         new_x=XPos.LMARGIN,
                         new_y=YPos.NEXT)

    def render_cell_spacer(self, cells):
        return self.cell(self.config['pdf']['cell_width'] * cells, self.config['pdf']['cell_height'] * cells, '')

    def generate_document(self):
        self.output(f'{self.output_filename}.pdf')
