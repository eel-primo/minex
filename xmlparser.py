
import xmltodict

def open_news():
    with open('data/news.xml') as fd: 
        return xmltodict.parse(fd.read())["news"]
