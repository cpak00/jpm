import spider


class By:
    GROUPID = 0
    ARTIFACTID = 1
    VERSIONS = 2
    ORDER = 3

    def toString(self, id):
        if id == 0:
            return 'groupId'
        if id == 1:
            return 'artifactId'
        if id == 2:
            return 'version'
        if id == 3:
            return 'order'
        return ''


def search(content):
    print('prepare to search {0}'.format(content))
    sql = "select * from versions where artifactId like ? order by artifactId, orderId"
    resultSet = spider.con.cursor().execute(sql, ["%"+content+"%"])
    search_result = []
    for result in resultSet:
        flag = True
        for i in search_result:
            if (i['artifactId'] == result[0] and i['groupId'] == result[1]):
                i['versions'].append(result[2])
                flag = False
                break
        if flag:
            search_result.append({
                'groupId': result[1],
                'artifactId': result[0],
                'versions': [result[2]],
                'link': result[4]
            })
            # earch_result.append((result[2], result[1], [result[3]]))
    print("total {0} results".format(len(search_result)))
    return search_result


def get_latest_version(name, group):
    print('prepare to get the latest version of {0}/{1}'.format(group, name))
    sql = "select * from versions where artifactId=? and groupId=? order by orderId"
    resultSet = spider.con.cursor().execute(sql, [name, group])
    search_result = []
    for result in resultSet:
        flag = True
        for i in search_result:
            if (i['artifactId'] == result[0] and i['groupId'] == result[1]):
                i['versions'].append(result[2])
                flag = False
                break
        if flag:
            search_result.append({
                'groupId': result[1],
                'artifactId': result[0],
                'versions': [result[2]],
                'link': result[4]
            })
            # earch_result.append((result[2], result[1], [result[3]]))
    print("total {0} results".format(len(search_result)))
    return search_result

