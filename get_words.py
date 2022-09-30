import requests
import bs4 as BeautifulSoup
import csv

kyus = ['kyu1', 'kyu100', 'kyu2', 'kyu200', 'kyu3', 'kyu4', 'kyu5', 'kyu6', 'kyu7', 'kyu8', 'kyu9', 'kyu10',]

for kyu in kyus:

    url = requests.get(f'https://kanjijoho.com/cat/{kyu}.html')
    output_file_name = f'practice_{kyu}.csv'

    with open(output_file_name, mode='w', encoding="utf-16") as kanjis:
        t = csv.writer(kanjis, delimiter='^', quotechar="", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator = '')
        t.writerow([f'漢字,部首,正解,音読み,正解,訓読み,正解,1,2,3 \n'])


        if url.status_code != 200:
            print('status not 200, check it')
        else:
            soup = BeautifulSoup.BeautifulSoup(url.content, 'html.parser')
            words = soup.find_all("table", {"class": "kyuichiran"})
            for word in words:
                word_list = word.find_all('a')
                word_list = [x.text.strip() for x in word_list]


        # print(word_list)
        for char in word_list:
                t.writerow([f'{char}\n'])