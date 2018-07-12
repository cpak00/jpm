import xml.etree.ElementTree as ET
import xml.dom.minidom as md
namespace = 'http://maven.apache.org/POM/4.0.0'
ET.register_namespace('', namespace)


def xml_to_tree(in_path):
    try:
        tree = ET.parse(in_path)
        return tree
    except Exception as e:
        return None


def tree_to_list(tree):
    if not tree or not tree.getroot():
        print('please init first')
        return None
    dependencies = tree.getroot().find('{{{0}}}dependencies'.format(namespace))
    if dependencies:
        dependency_list = dependencies.findall('{{{0}}}dependency'.format(namespace))
        result = []
        for item in dependency_list:
            groupId = item.find('{{{0}}}groupId'.format(namespace)).text
            artifactId = item.find('{{{0}}}artifactId'.format(namespace)).text
            version = item.find('{{{0}}}version'.format(namespace)).text
            result.append({'groupId': groupId, 'artifactId': artifactId, 'version': version})
        return result
    else:
        return []


def list_to_tree(_list, tree):
    dependencies = tree.getroot().find('{{{0}}}dependencies'.format(namespace))
    for i in dependencies.getchildren():
        dependencies.remove(i)
    for item in _list:
        dependency = ET.Element('dependency')
        for key, value in item.items():
            node = ET.SubElement(dependency, key)
            node.text = value
        dependencies.append(dependency)
    return tree


def init_pom():
    open('pom.xml', 'wb+').write('''<?xml version="1.0"?>
<project xmlns="{0}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>temp.download</groupId>
    <artifactId>temp-download</artifactId>
    <version>1.0-SNAPSHOT</version>
    <dependencies>
    <!-- 依赖-->
    </dependencies>
</project>
'''.format(namespace).encode('utf-8'))


def install(name, group, version):
    try:
        xml_tree = xml_to_tree('pom.xml')
        dependencies = tree_to_list(xml_tree)
        dependencies.append({'groupId': group, 'artifactId': name, 'version': version})
        list_to_tree(dependencies, xml_tree)
        xml_string = '<?xml version="1.0"?>'+ET.tostring(xml_tree.getroot()).decode('utf-8')
        open('pom.xml', 'wb+').write(xml_string.encode('utf-8'))
    except Exception as e:
        print(e)
        print('please type `jpm init`')


def save_tree(file_name, xml_tree):
    xml_string = '<?xml version="1.0"?>' + ET.tostring(
        xml_tree.getroot()).decode('utf-8')
    dom = md.parseString(xml_string)
    f = open(file_name, 'wb+')
    # f.write(xml_string)
    xml_bytes = dom.toprettyxml(indent='\t', encoding='utf-8').decode('utf-8')
    result = ''
    for tt in xml_bytes.splitlines():
        line_clean = tt.rstrip()
        if line_clean:
            line_crlf = line_clean+'\r\n'
            result += line_crlf
    f.write(result.encode('utf-8'))
    f.close()
