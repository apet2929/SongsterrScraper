from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
import os
import time

def scrape_song(song_url):
    driver = webdriver.Chrome()
    driver.get(song_url)
    driver.implicitly_wait(2)
    
    tabs = driver.find_element(By.ID, "tablature")
    # wait until elements loaded
    driver.find_element(By.ID, "showroom")
    

    driver.execute_script("document.getElementById('showroom').style.display = 'none';")
    if driver.find_element(By.ID, "tablist"):
        driver.execute_script("document.getElementById('tablist').style.display = 'none';")

    for i, elem in enumerate(tabs.find_elements(By.TAG_NAME, "svg")):
        loc = elem.location
        driver.execute_script(f"window.scrollTo({loc["x"]}, {loc["y"]});")
        elem.screenshot(f"./images/foo-{str(i).zfill(4)}.png")
    
    driver.quit()

def combine_images(song_name):
    image_paths = [
        os.path.join("images", f) for f in os.listdir("images")
    ]
    images = [
        Image.open(f) for f in image_paths
    ]

    pdf_path = f"songs/{song_name}.pdf"
        
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

    for img in image_paths:
        os.remove(img)

def main():
    global songs
    for song_url in songs:
        scrape_song(song_url[0])
        combine_images(song_url[1])

songs = [
    # ("https://www.songsterr.com/a/wsa/nirvana-blew-drum-tab-s10772", "nirvana-blew")
    ("https://www.songsterr.com/a/wsa/nirvana-about-a-girl-drum-tab-s29", "nirvana-about_a_girl"),
    ("https://www.songsterr.com/a/wsa/nirvana-smells-like-teen-spirit-drum-tab-s269", "nirvana-smells_like_teen_spirit"),
    ("https://www.songsterr.com/a/wsa/nirvana-in-bloom-drum-tab-s295", "nirvana-in_bloom"),
    ("https://www.songsterr.com/a/wsa/radiohead-creep-drum-tab-s97", "radiohead-creep"),
    ("https://www.songsterr.com/a/wsa/deftones-my-own-summer-shove-it-drum-tab-s595","deftones-my_own_summer")
]

if __name__ == "__main__":
    main()