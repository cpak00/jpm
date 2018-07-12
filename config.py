# repository = 'http://maven.aliyun.com/nexus/content/groups/public/'
repository = 'http://central.maven.org/maven2/'
db = 'repo.db'


def get_repo():
    global repository
    if (repository[-1] == '/'):
        repository = repository[:-1]
    return repository


def get_db():
    return db
