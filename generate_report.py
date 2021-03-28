from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class Report:

    def __init__(self):
        self.report = SimpleDocTemplate("TextFound.pdf", pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.flowables = [Paragraph('Phrases Found: ', style=self.styles["Normal"])]

    def add_string(self, line : str):
        lines = line.splitlines()
        for line in lines:
            
            words = line.split(' ')
            new_words = []

            for word in words:
                new_words.append(word)

            self.flowables.append(Paragraph(' '.join(new_words), style=self.styles["Normal"]))

    def build(self):
        self.report.build(self.flowables)
