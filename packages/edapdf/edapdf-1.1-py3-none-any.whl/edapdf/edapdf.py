"""
Defines EDAPDF class.
"""

from tempfile import NamedTemporaryFile

from fpdf import FPDF, Align,XPos
from matplotlib.figure import Figure
import pandas as pd
import polars as pl
from great_tables import GT, style, loc 


class EDAPDF(FPDF):
    """
    PDF class that inherits from FPDF and automatically
    sets certain options.
    """

    _title: str
    _header_flag: bool

    def __init__(self, title: str = ""):
        self._title = title  # Initialize _title properly
        super().__init__(orientation="landscape", unit="mm", format="A4")
        self._header_flag = False
        self._add_title_page()
        self._header_flag = True

    def _add_title_page(self):
        # Calculate center position
        self.set_font(
            "helvetica", style="B", size=30
        )  # Calculate size of cell containing title
        text_width = self.get_string_width(self._title)
        x = (self.w - text_width) / 2  # Center horizontally
        y = self.h / 2  # Center vertically

        # Set position and add text
        self.add_page()
        self.set_xy(x, y)
        self.cell(text_width, 10, self._title, align="C")
        self._reset_font()

    def _reset_font(self):
        self.set_font("helvetica", size=15)

    def _set_header_footer_font(self):
        self.set_font("helvetica", size=8)

    def _add_slide_title(self, title: str, pos: str):
        self.set_font("helvetica", size=25, style="B")
        y = 20
        if pos == "C":
            text_width = self.get_string_width(title)
            x = (self.w - text_width) / 2  # Center horizontally
            self.set_xy(x, y)
            self.multi_cell(w=text_width + 4, h=10, text=title, align="C")
        elif pos == "L":
            text_width = self.get_string_width(title)
            self.set_y(y)
            self.multi_cell(w=text_width + 4, h=10, text=title, align="C")
        else: 
            raise ValueError("pos argument must be 'C' or 'L'")
        self.ln(25)

    def header(self):
        if self._header_flag:
            # Setting font: helvetica bold 15
            self._set_header_footer_font()
            # Printing title:
            self.cell(w=None, h=None, text=self._title, new_x=XPos.LMARGIN)
            # Performing a line break:
            self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font
        self._set_header_footer_font()
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_figure(self, figure: Figure, title: str = "Figure"):
        self.add_page()
        self._add_slide_title(title=title, pos="C") 
        with NamedTemporaryFile(suffix=".png") as tempfile:
            figure.set_size_inches(6, 3.75)
            figure.savefig(tempfile, dpi=300)
            self.image(tempfile.name, x=Align.C, h=125, keep_aspect_ratio=True)

    def add_table(self, table: pd.DataFrame | pl.DataFrame, title: str = "Table"):
        self.add_page()
        self._add_slide_title(title=title, pos="C") 
        with NamedTemporaryFile(suffix=".png") as tempfile:
            gt = GT(table)
            gt = (gt
                  .tab_style(style=style.text(color="black", font="Helvetica", size=15),
                         locations=[loc.body()])
                  .tab_style(style=style.text(color="black", font="Helvetica", size=15, weight="bold"),
                         locations=[loc.column_labels()])
                  .cols_align(align="center"))
            gt.save(tempfile.name, scale=10)
            self.image(tempfile.name, x=Align.C, h=140, keep_aspect_ratio=True)

    def add_text_slide(self, title: str, bullet_points: list[str]):
        self.add_page()
        self._add_slide_title(title=title, pos="L")
        self._reset_font()
        bullet = "-" 
        for bullet_point in bullet_points:
            self.cell(10)  # Small indent
            w = self.epw - (self.r_margin + self.l_margin + 10)
            self.multi_cell(w=w, 
                            text=f"{bullet} {bullet_point}", 
                            new_x=XPos.LMARGIN)
            self.ln(7.5)

    def _add_dummy_figure(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(layout='tight')
        ax.scatter([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        return fig

    
    def _add_dummy_table(self):
        import polars as pl 
        df = pl.DataFrame({
        "column1": [1, 2, 3, 4, 5],        # Integers
        "column2": [10, 20, 30, 40, 50],   # Integers
        "column3": [1.1, 2.2, 3.3, 4.4, 5.5]  # Floats
        }).describe()
        return df

    

"""
%load_ext autoreload
%autoreload 2
from edapdf import EDAPDF
pdf = EDAPDF(title="test")
pdf.add_table(table=pdf._add_dummy_table(), title="my table")
pdf.add_figure(figure=pdf._add_dummy_figure(), title="My Figure")
pdf.output("Path/test.pdf")
"""
