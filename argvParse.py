import xmlController as xC
import urlQuery as uQ
import jpmContext as jC
import spider as sp
import dao


def parse(argv):
    # print(argv)
    length = len(argv)
    if length == 2:
        if argv[1] == 'init':
            xC.init_pom()
        if argv[1] == 'help':
            jC.print_help()
        if argv[1] == 'list':
            jC.print_list()
        if argv[1] == 'update':
            sp.update_repo()
    elif length == 3:
        if argv[1] == 'install':
            print('prepare to install')
            search_result = dao.search(argv[2])
            uQ.only_name_download(argv[2], search_result)
        elif argv[1] == 'search':
            # search_result = uQ.get_search(argv[2])
            search_result = dao.search(argv[2])
            print('%30s %30s %30s' % ('jarName', 'jarGroup', 'lastest version'))
            for result in search_result:
                name = result['artifactId']
                group = result['groupId']
                latest_version = result['versions'][-1]
                print('%30s %30s %30s' % (name, group, latest_version))
            print(r'type `jpm install %jarGroup% %jarName%` to install')
        elif argv[1] == 'remove':
            jC.remove_jar(argv[2])
            print('done')
    elif length == 4:
        if argv[1] == 'install':
            result = dao.get_latest_version(argv[3], argv[2])
            uQ.latest_search_download(result)
    else:
        print('please print jpm help to get help')