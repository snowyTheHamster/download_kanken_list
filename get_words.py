import requests
import bs4 as BeautifulSoup
import csv
import re

kyus = ['kyu10', 'kyu9', 'kyu8', 'kyu7', 'kyu6', 'kyu5', 'kyu4', 'kyu3', 'kyu200', 'kyu2', 'kyu100', 'kyu1',]

for kyu in kyus:

    url = requests.get(f'https://kanjijoho.com/cat/{kyu}.html')
    output_file_name = f'practice_{kyu}.csv'

    with open(output_file_name, mode='w', encoding="utf-16") as kanjis:
        t = csv.writer(kanjis, delimiter='^', quotechar="", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator = '')
        t.writerow([f'漢字,部首,正解,音読み,正解,訓読み,正解,url \n'])


        if url.status_code != 200:
            print(f'{kyu}: status not 200, check it')
            continue
        else:
            soup = BeautifulSoup.BeautifulSoup(url.content, 'html.parser')
            # words = soup.find_all("table", {"class": "kyuichiran"}).find('a')
            table = soup.find("table", {"class": "kyuichiran"})
            for a in table.find_all("a", href=True):
                each_link = a['href']
                url = requests.get(each_link)
                if url.status_code != 200:
                    print(f'{each_link}: status not 200, check it')
                    continue
                else:
                    soup = BeautifulSoup.BeautifulSoup(url.content, 'html.parser')
                    kanji = soup.find("div", {"id": "kanjimainleft"}).text
                    bushu = soup.find('th', text = re.compile('部首'))
                    bushu_data = bushu.find_next_sibling("td").text
                    bushu_data = bushu_data.strip()
                    bushu_data = bushu_data.replace("<br>","")
                    bushu_data = bushu_data.replace("\n"," ")
                    try:
                        onyomi = soup.find('th', text = re.compile('音読み'))
                        onyomi_data = onyomi.find_next_sibling("td").find("ul").text
                        onyomi_data = onyomi_data.strip()
                        onyomi_data = onyomi_data.replace("<br>","")
                        onyomi_data = onyomi_data.replace("\n"," ")
                    except:
                        onyomi_data = "x"
                    try:
                        kunyomi = soup.find('th', text = re.compile('訓読み'))
                        kunyomi_data = kunyomi.find_next_sibling("td").find("ul").text
                        kunyomi_data = kunyomi_data.strip()
                        kunyomi_data = kunyomi_data.replace("<br>","")
                        kunyomi_data = kunyomi_data.replace("\n"," ")
                    except:
                        kunyomi_data = "x"

                    print(f'kyu:{kyu}, {kanji}:{each_link}, {url.status_code}')
                    t.writerow([f'"{kanji}","","{bushu_data}","","{onyomi_data}","","{kunyomi_data}","{each_link}"\n'])