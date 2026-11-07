import sys
import pickle
import xml.etree.ElementTree as ET


def dict_to_xml(parent, obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = ET.SubElement(parent, "item", {"key": key})
            dict_to_xml(child, value)

    elif isinstance(obj, list):
        for item in obj:
            child = ET.SubElement(parent, "item")
            dict_to_xml(child, item)

    else:
        parent.text = str(obj)


def main() -> int:
    if len(sys.argv) != 3:
        return 1

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "rb") as f:
        data = pickle.load(f)

    root = ET.Element("root")
    print(root)
    dict_to_xml(root, data)

    ET.indent(root, space="  ")

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    return 0

if __name__ == __main__:
    main()