from PIL import Image

filename = 'test.png'
im = Image.open(filename)
im.load()
print(im.info)