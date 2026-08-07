from services.pinterest_api import search_fashion_images

images = search_fashion_images("Luxury African Fashion")

print(images[0])