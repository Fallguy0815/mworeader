from PIL import ImageFont, ImageDraw, Image
import PIL

def get_concat_v_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

comp = Image.open('ocr_c_2_G 4 R R E T.png')
img = Image.new('RGB', (292,21))
draw = ImageDraw.Draw(img)

# use a truetype font
font = ImageFont.truetype("Helvetica-Neue-LT-Std-65-Medium_22532.ttf", 17)
draw.text((6, 1), "G 4 R R E T", font=font)

ni = img.resize((int(img.width*0.83),img.height), resample=PIL.Image.LANCZOS)


get_concat_v_blank(ni, comp).save('output.png')


#img.save('output.png')

