import os
from dark_web_scraper import find_images_from_onion_link

os.system('clear')

str = input("Enter .onion link to scrape images :")
find_images_from_onion_link(str)
print ("Pictures are saved in inspy/static/images/*.jpg")
