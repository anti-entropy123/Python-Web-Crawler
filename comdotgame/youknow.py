import requests
from lxml import etree
from typing import Tuple, List
import json
from time import sleep
import pymysql

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

names = set()

db = pymysql.connect(
    'localhost', 
    'root', 
    'root', 
    'comdotgame', 
    charset='utf8', 
    port=3306
)
cursor = db.cursor()

def get_one_game_id(url:str) -> str:
    response = requests.get(
        url=url,
        headers=header
    )
    html = etree.fromstring(response.text, etree.HTMLParser())
    result = html.xpath('//a[@rel="nofollow"]/span')[0]
    return result.xpath('text()')[0]

def get_one_game_like_and_unlike(id:int)-> Tuple[int, int]:
    response = requests.get(
        url = 'https://www.comdotgame.com/ajax/game-data?id=' + str(id),
        headers = header
    )
    data = json.loads(response.text)
    return int(data['rate_up']), int(data['rate_down']) 

def get_all_game_in_one_page(url: str) -> List[Tuple[str, str]]:
    response = requests.get(
        url=url, 
        headers=header
    )
    
    html = etree.fromstring(response.text, etree.HTMLParser())
    results = html.xpath('/html/body/main/div[@class="body"]/ul/li[@class="game left"]/a')
    return [(result.xpath('@title')[0], result.xpath('@href')[0]) for result in results[2:]]
    
if __name__ == "__main__":
    sql = '''
        select name from like_and_unlike;
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        names.add(row[0])

    cnt = 1816
    for page in range(140, 185): #185
        games = get_all_game_in_one_page("https://www.comdotgame.com/adult/" + str(page))
        sleep(0.1)
        for name, url in games:
            while "'" in name:
                name = name.replace("'", "")
            if name in names:
                continue
            sleep(0.1)
            game_id = get_one_game_id(url=url)
            sleep(0.1)
            like, unlike = get_one_game_like_and_unlike(game_id)
            while "'" in url:
                url = url.replace("'", "")
            print(f'[{cnt}]', name, url, like, unlike)
            sql = f"insert into like_and_unlike values('{name}','{url}', {like}, {unlike});"
            try:
                cursor.execute(sql)
                db.commit()
                names.add(name)
                cnt += 1
            except pymysql.err.IntegrityError:
                pass