from PIL import Image, ImageEnhance, ImageFilter 


with Image.open("1.jpg") as pic:
    #pic.show()

    saturated = ImageEnhance.Color(pic)
    saturated = saturated.enhance(1.2)
    saturated.save("Saturated.jpg")

    bw = pic.convert("L")
    bw.save("Gray_image.jpg")

    mirror = pic.transpose(Image.FLIP_LEFT_RIGHT)
    mirror.save("Mirror_image.jpg")

    blur = pic.filter(ImageFilter.BLUR)
    blur.save("Blur_image.jpg")

    contrast = ImageEnhance.Contrast(pic)
    contrast = contrast.enhance(2.5)
    contrast.save("Contrast_image.jpg")
