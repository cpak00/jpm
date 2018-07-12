import requests
from lxml import etree
import sqlite3
import config
repository = config.get_repo()
db = config.get_db()
con = ''


def sqlite3_connect():
    global con
    con = sqlite3.connect(db)
    con.execute('''
    create table if not exists "versions" (
        ID INTEGER PRIMARY KEY AUTOINCREMENT ,
        artifactId TEXT,
        groupId TEXT,
        version TEXT,
        orderId INT
    )
    ''')


def get_all_title(url):
    r = requests.get(url)
    tree = etree.HTML(r.text)
    
    meta = tree.xpath('//a[@title="maven-metadata.xml"]/@href')
    if len(meta) == 1:
        parse_meta(url + '/' + meta[0])
    else:
        groups = tree.xpath('//a[contains(@title, "/")]/@title')
        for i in range(len(groups)):
            get_all_title(url + '/' + groups[i].split('/')[0])


def parse_meta(url):
    print(url)
    global con
    r = requests.get(url)
    tree = etree.XML(r.text.encode('utf-8'))
    artifactId = ''.join(tree.xpath('//artifactId/text()'))
    groupId = ''.join(tree.xpath('//groupId/text()'))
    versions = tree.xpath('//versions/version/text()')
    if artifactId and groupId:     
        if con:
            try:
                sql = '''
                insert into versions values(null, ?, ?, ?, ?)
                '''
                params = []
                i = 0
                for version in versions:
                    param = [artifactId, groupId, version, i]
                    i += 1
                    params.append(param)
                # print(params)
                con.cursor().executemany(sql, params)
                con.commit()
            except Exception as e:
                print(e)


def update_repo():
    print('prepare to update repo.db')
    get_all_title(repository)
    print('update done')


sqlite3_connect()
