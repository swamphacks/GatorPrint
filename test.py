from escpos.printer import Usb
from PIL import Image

p = Usb(0x04b8, 0x0202, 0, profile="TM-T88IV")

image = Image.open("../../Pictures/mikupony.jpeg")

width, height = image.size

new_width = 512
new_height = int((new_width / width) * height)

resized = image.resize((new_width, new_height))

p.image(resized, center=True)

p.cut()
