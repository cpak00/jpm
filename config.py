# repository = 'http://maven.aliyun.com/nexus/content/groups/public/'
repository = 'http://central.maven.org/maven2/'
download_repo = 'http://maven.aliyun.com/nexus/content/groups/public/'
db = 'repo.db'


def get_repo():
    global repository
    if (repository[-1] == '/'):
        repository = repository[:-1]
    return repository


def get_db():
    return db


def get_download():
    global download_repo
    if (download_repo[-1] == '/'):
        download_repo = download_repo[:-1]
    return download_repo
