from PIL import Image
print(Image.open('test.png').load().info)
