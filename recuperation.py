
# res = requests.get("https://lol.fandom.com/wiki/LEC/2024_Season/Summer_Season/Player_Statistics")


from selenium import webdriver


driver = webdriver.Chrome()

driver.get(
    "https://lol.fandom.com/wiki/LEC/2024_Season/Summer_Season/Player_Statistics"
)

with open("demofile.html", "a") as f:
    f.write(driver.page_source)
