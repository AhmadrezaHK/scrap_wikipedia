import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import uuid
import re


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


page = requests.get(
    'https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%A9%DB%8C%E2%80%8C%D9%BE%D8%AF%DB%8C%D8%A7:%D9%81%D9%87%D8%B1%D8%B3%D8%AA_%D8%B3%D8%B1%DB%8C%D8%B9')

soup = BeautifulSoup(page.content, 'html.parser')

categories_link = ['https://fa.wikipedia.org/wiki/ویژه:تمام_صفحه‌ها' +
                   a.get('href') for a in soup.select('table.plainlinks a')]

count = 0
for cat_link in categories_link:
    cat_page = requests.get(cat_link)
    cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
    page_link_list = []
    for page_link in cat_soup.select('a.mw-redirect'):
        try:
            found = 'https://fa.wikipedia.org/wiki/' + \
                re.search(r'_\((.+?)\)', page_link.get('href')).group(1)
        except AttributeError:
            found = 'https://fa.wikipedia.org'+page_link.get('href')
        page_link_list.append(found)

    s = {}
    for pageee_link in page_link_list:
        pageee = requests.get(pageee_link)
        s[pageee_link] = text_from_html(pageee.content)
        print(pageee_link)
        count += 1  
        if (len(s) == 2):
            f = open('file/'+str(uuid.uuid4()) + '.txt', 'w')
            for ele in s:
                f.write('######-PAGE_LINK-######\n')
                f.write(str(ele) + '\n')
                f.write('######-PAGE_CONTENT-######\n')
                f.write(str(s[ele]) + '\n')
            f.close()
            print(str(count) + ' writed')
            s={}

