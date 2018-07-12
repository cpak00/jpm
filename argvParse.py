import xmlController as xC
import urlQuery as uQ
import jpmContext as jC
import spider as sp


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
            uQ.only_name_download(argv[2])
        elif argv[1] == 'search':
            search_result = uQ.get_search(argv[2])
            print('%30s %30s' % ('jarName', 'jarGroup'))
            for result in search_result:
                name = result['artifactId']
                group = result['groupId']
                print('%30s %30s' % (name, group))
            print(r'type `jpm install %jarGroup% %jarName%` to install')
        elif argv[1] == 'remove':
            jC.remove_jar(argv[2])
            print('done')
    elif length == 4:
        if argv[1] == 'install':
            uQ.lastest_version_download(argv[3], argv[2])
    else:
        print('please print jpm help to get help')