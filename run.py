from ocr import ocr_space_file, ocr_space_url
from screenshot import ScreenShot
from imageprocessor import ImageProcessor
from generate_report import Report
from PIL import Image
import pytesseract
import json

scrape = ScreenShot()
website = input("Website: ")
files = scrape.scrape_website(website)
for image in files:
    process = ImageProcessor(image)
    process.process()
    process.save(image)

pdf = Report()

for image in files:
    test_file = ocr_space_file(filename=image, overlay=False, api_key='426dfa6ce788957', language='eng')
    
    try:
        line = json.loads(test_file)["ParsedResults"][0]["ParsedText"]
    except:
        # Resize
        img = Image.open(image)
        img.save(image, optimize = True, quality = 10)
        test_file = ocr_space_file(filename=image, overlay=False, api_key='426dfa6ce788957', language='eng')
        line = json.loads(test_file)["ParsedResults"][0]["ParsedText"]

    pdf.add_string(line)
pdf.build()
