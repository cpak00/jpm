import requests
from lxml import etree
import xmlController as xC
import xml.etree.ElementTree as ET
import operator
import config
repository = config.get_repo()
download_repository = config.get_download()


'''
def get_versions_info(name, group):
    try:
        url = 'http://mvnrepository.com/artifact/{0}/{1}'.format(group, name)
        print('calling {0}'.format(url))
        r = requests.get(url)
        tree = etree.HTML(r.text)
        tags = tree.xpath('//*[@class="vbtn release"]')
        result = []
        for tag in tags:
            href = ''.join(tag.xpath('./@href'))
            version = ''.join(tag.xpath('./text()'))
            result.append({'version': version, 'href': href})
        print('get {0} versions'.format(len(result)))
        return result
    except Exception as e:
        print('Timeout, please check the net')


def get_detail_info(name, group, version):
    try:
        url = 'http://mvnrepository.com/artifact/{0}/{1}/{2}'.format(
            group, name, version)
        print('detail info url {0}'.format(url))
        r = requests.get(url)
        tree = etree.HTML(r.text)
        download_link = tree.xpath('//a[contains(text(),"jar")]/@href')[0]
        return download_link, ''
    except Exception as e:
        print('Timeout, please check the net')
'''


def only_name_download(name, search_result):
    result = search_result
    if result and len(result) > 0:
        if result[0]['artifactId'] == name:
            groupId = result[0]['groupId']
            print('prepare to install {0} from group {1}'.format(name, groupId))
            # lastest_version_download(name, groupId)
            latest_search_download(search_result)
        else:
            print('there is not {0}, maybe you want to install {1}'.format(name, result[0]['artifactId']))
    else:
        print('there is not any result like {0}'.format(name))


def latest_search_download(result):
    if not result:
        print('cannot get the lastest search')
        return
    name = result[0]['artifactId']
    group = result[0]['groupId']
    versions = result[0]['versions']
    link = result[0]['link']
    if versions and len(versions) > 0:
        last_version = versions[-1]
        print('prepare to download the lastest version {0}'.format(last_version))
        download(name, group, last_version, link)
    else:
        print('cannot get the lastest version')


'''
def lastest_version_download(name, group):
    versions = get_versions_info(name, group)
    if versions and len(versions) > 0:
        last_version = versions[0]
        print('prepare to download the lastest version {0}'.format(last_version['version']))
        download(name, group, last_version['version'])
    else:
        print('cannot get the lastest version')
'''


def construct_download(name, version, link):
    print('constuct from download link for {0}'.format(name))
    url = link + '/' + version + '/' + name + '-' + version + '.jar'
    url = url.replace('http://central.maven.org/maven2', download_repository)
    return url


def download(name, group, version, link):
    xml_tree = xC.xml_to_tree('pom.xml')
    dependencies = xC.tree_to_list(xml_tree)
    de = {
        'groupId': group,
        'artifactId': name,
        'version': version
    }
    if not dependencies:
        dependencies = []
    for i in dependencies:
        if operator.eq(de, i):
            print('has dependence {0}'.format(name))
            return
    dependencies.append(de)
    
    try:
        ###
        download_link = construct_download(name, version, link)
        print('prepare to download from link {0}'.format(download_link))
        r = requests.get(download_link)
        with open(download_link.split('/')[-1], "wb") as code:
            code.write(r.content)
        print('done, {0} has been downloaded'.format(link.split('/')[-1]))
        ###

        if xml_tree:
            # print(dependencies)
            xC.list_to_tree(dependencies, xml_tree)
            xC.save_tree('pom.xml', xml_tree)
            '''
            xml_string = '<?xml version="1.0"?>' + ET.tostring(
                xml_tree.getroot()).decode('utf-8')
            open('pom.xml', 'wb+').write(xml_string.encode('utf-8'))
            '''
        else:
            print('suggest to init first')
    except Exception as e:
        print(e)
        print('Timeout, please check the net')


'''
def get_search(content):
    try:
        r = requests.get('http://mvnrepository.com/search?q={0}'.format(content))
        tree = etree.HTML(r.text)
        results = tree.xpath('//p[@class="im-subtitle"]')
        result = []
        for item in results:
            group = ''.join(item.xpath("./a[1]/text()"))
            name = ''.join(item.xpath("./a[2]/text()"))
            result.append({'groupId': group, 'artifactId': name})
        return result
    except Exception as e:
        print('Timeout, please check the net')
'''
