import xmlController as xC
import xml.etree.ElementTree as ET
import os


def print_help():
    print('''
    welcome to java package managerment
    options:
    %-40s %-30s
    %-40s %-30s
    %-40s %-30s
    %-40s %-30s
    ''' % (
        'jpm help', 'print the document', 'jpm init',
        'construct a default pom.xml, after this, you can use maven to manager your jar',
        'jpm search name',
        'if you are not very sure for your jar\'s name or group, you can search it',
        'jpm install [jarGroup] (jarName)',
        'install the lastest released jar [groupId] (groupId is optional)'))


def remove_jar(name):
    xml_tree = xC.xml_to_tree('pom.xml')
    dependencies = xC.tree_to_list(xml_tree)
    if dependencies:
        for i in dependencies:
            if i['artifactId'] == name:
                print('remove the dependency from pom.xml: {0}'.format(name))
                version = i['version']
                dependencies.remove(i)
                if xml_tree:
                    xC.list_to_tree(dependencies, xml_tree)
                    xC.save_tree('pom.xml', xml_tree)
                    '''
                    xml_string = '<?xml version="1.0"?>' + ET.tostring(
                        xml_tree.getroot()).decode('utf-8')
                    open('pom.xml', 'wb+').write(xml_string.encode('utf-8'))
                    '''
                else:
                    print('suggest to init first')

                ###
                try:
                    os.path.os.remove('{0}-{1}.jar'.format(name, version))
                    print('delete jar named {0}-{1}.jar'.format(name, version))
                except:
                    print(
                        'cannot delete jar named {0}-{1}.jar, please delete it yourself'.
                        format(name, version))
                return
    print('there is not a jar named {0}'.format(name))


def print_list():
    xml_tree = xC.xml_to_tree('pom.xml')
    dependencies = xC.tree_to_list(xml_tree)
    if xml_tree or dependencies is None:
        print(dependencies)
    else:
        print('please init first')
