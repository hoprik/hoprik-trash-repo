import io
from barcode import UPCA
from barcode.writer import ImageWriter
from PIL import Image
import random, img2pdf

count = int(input("Enter the number of barcodes you want to generate: "))
PIXELS_ON_CM = 37.938105*2

barcodes = []
total_width = 0
total_height = 0
for i in range(round(count/4)):
    row = []
    row_width = 0
    row_height = 0
    for j in range(4):
        code = UPCA(str(random.randint(10000000000, 99999999999)), writer=ImageWriter())
        img = code.render()
        img = img.resize((int(5*PIXELS_ON_CM), int(1.5*PIXELS_ON_CM)))
        row.append(img)
        row_width += img.width
        row_height = max(img.height, row_height)
    barcodes.append(row)
    total_width = max(total_width, row_width)
    total_height += row_height

combined_image = Image.new('RGB', (int(21*PIXELS_ON_CM), int(30*PIXELS_ON_CM)), color='white')

y_offset = 10
for barcode in barcodes:
    row_width = 15
    _y_offset = 0
    for barcode_img in barcode:
        combined_image.paste(barcode_img, (row_width, y_offset))
        row_width += barcode_img.width
        _y_offset = max(barcode_img.height, _y_offset)
    y_offset += _y_offset


with open("barcodes.pdf","wb") as f, io.BytesIO() as output:
    combined_image.save(output, format='jpeg')
    f.write(img2pdf.convert(output.getvalue()))