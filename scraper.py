from selenium import webdriver
from selenium.webdriver.common.by import By
import jinja2
import pdfkit
import os
import time

def scrape_song(song_url, song_name):
    if not os.path.exists("./images"):
        os.mkdir("./images")
    song_path = os.path.join("images", song_name)
    if not os.path.exists(song_path):
        os.mkdir(song_path)

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
        driver.execute_script(f"window.scrollTo({loc['x']}, {loc['y']});")
        elem.screenshot(f"{song_path}/img-{str(i).zfill(4)}.png")

    driver.quit()

def pairwise(t):
    it = iter(t)
    return zip(it,it)

def create_html_doc(images):
    image_pairs = pairwise(images)
    loader=jinja2.FileSystemLoader(".")
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template("out_template.j2")
    rendered = template.render(image_pairs=image_pairs)
    return rendered

def combine_images(song_name):
    if not os.path.exists("./songs"):
        os.mkdir("./songs")

    pdf_path = f"songs/{song_name}.pdf"
    images = [
        os.path.join("images", song_name, f) for f in os.listdir(os.path.join("images", song_name))
    ]

    os.remove(images[1])
    images.remove(images[1]) # two dots thingy

    html_path = pdf_path.replace(".pdf", ".html")
    try:
        content = create_html_doc(images)
        print("Content written to html file at: ", html_path)
        with open(html_path, "w") as f:
            f.write(content)
    except:
        pass

def main():
    global songs
    for song in songs:
        scrape_song(song[0], song[1])
        combine_images(song[1])

songs = [
    ("https://www.songsterr.com/a/wsa/black-keys-heavy-soul-drum-tab-s668136", "black_keys-heavy_soul"),
    ("https://www.songsterr.com/a/wsa/masayoshi-takanaka-oh-tengo-suerte-drum-tab-s580675", "takanaka-oh_tengo_suerte"),
    ("https://www.songsterr.com/a/wsa/nirvana-rape-me-drum-tab-s39", "nirvana-rape_me")
]

if __name__ == "__main__":
    main()