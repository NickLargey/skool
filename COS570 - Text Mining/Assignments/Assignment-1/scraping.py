import requests
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


godFather_link = "https://www.dailyscript.com/scripts/The_Godfather.html"
godFather2_link = "https://www.dailyscript.com/scripts/godfather2.html"

html_gf1 = requests.get(godFather_link)
html_gf2 = requests.get(godFather2_link)

bs_gf1 = BeautifulSoup(
    html_gf1.text, features="html.parser")
bs_gf2 = BeautifulSoup(
    html_gf2.text, features="html.parser")


def scrape_and_clean(script, ouput_file):
    script.find("pre")
    lines = re.compile(
        r"\t{4}(MICHAEL|MICHAEL \(O.S.\)|MICHAEL \(CONT'D.\))\r\n\t{2}(.+?)(?:\r\n\r\n)", re.DOTALL)
    line = re.findall(lines, str(script))
    with open(f"{ouput_file}.txt", "w") as f:
        for dialog in line:
            d_out = re.sub(r'\s+', ' ', dialog[1])
            d_out = re.sub(r'\(.+\)', '', d_out)
            f.write(str(d_out).strip() + '\n')


def create_wordcloud(in_file):
    stopwords = set(STOPWORDS)
    stopwords.update(["will", "know", "want", "going", "thing", "things"])

    with open(in_file, "r+") as f:
        text = f.read()
        wordcloud = WordCloud(stopwords=stopwords,
                              height=400, width=600).generate(text)
        f_name = in_file.split(".")
        wordcloud.to_file(f"{f_name[0]}.png")


scrape_and_clean(bs_gf1, "GodFather1")
scrape_and_clean(bs_gf2, "GodFather2")


create_wordcloud("GodFather1.txt")
create_wordcloud("GodFather2.txt")
