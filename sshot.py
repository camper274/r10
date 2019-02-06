from selenium import webdriver
import time
import base64
import datetime
from selenium.webdriver.firefox.options import Options
import img2pdf
import os
from PIL import Image
options = Options()
options.headless = True


url = "http://krea.digital/v5/"
sector = ".my-3 .container"
page_weight = 1920
page_height = 3000


def take_screenshot(url, selector):

    driver = webdriver.Firefox(options=options, executable_path="./geckodriver")
    driver.set_window_size(page_weight,page_height)
    driver.get(url)
    time.sleep(1)
    file_name = _unique_file_name()
    element = driver.find_element_by_css_selector(selector)
    image_64 = element.screenshot_as_base64
    with open("{}.png".format(file_name), "wb") as image_file:
        image_file.write(base64.decodebytes(image_64.encode()))
        image_file.close()
    driver.quit()
    convert_image_to_pdf(file_name)


def _unique_file_name():

    return str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

def convert_image_to_pdf(file_name):

    img_path = "{}.png".format(file_name)
    image = Image.open(img_path)
    image.load()
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    background.save(img_path, 'PNG', quality=100)
    pdf_bytes = img2pdf.convert(image.filename)
    pdf_path ='pdf/'+ file_name + ".pdf"
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    os.remove(img_path)
    image.close()
    file.close()
    print("Successfully made pdf file")

take_screenshot(url,sector)