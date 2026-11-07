import sys
import pickle

def yaml_escape(value) -> str:
    s = str(value)
    result = ['"']

    for ch in s:
        if ch == "\\":
            result.append("\\\\")
        elif ch == '"':
            result.append('\\"')
        else:
            result.append(ch)

    result.append('"')
    return "".join(result)


def to_yaml(obj, indent: int = 0) -> list:
    pad = "  " * indent
    lines = []

    if isinstance(obj, dict):
        if not obj:
            return [pad + "{}"]

        for key, value in obj.items():
            yaml_key = yaml_escape(key)

            if isinstance(value, dict):
                lines.append(f"{pad}{yaml_key}:")
                lines.extend(to_yaml(value, indent + 1))

            elif isinstance(value, list):
                lines.append(f"{pad}{yaml_key}:")
                for item in value:
                    if isinstance(item, (dict, list)):
                        lines.append(f"{pad}  -")
                        lines.extend(to_yaml(item, indent + 2))
                    else:
                        lines.append(f"{pad}  - {yaml_escape(item)}")

            else:
                lines.append(f"{pad}{yaml_key}: {yaml_escape(value)}")

        return lines

    if isinstance(obj, list):
        if not obj:
            return [pad + "[]"]

        for item in obj:
            lines.append(f"{pad}- {yaml_escape(item)}")

        return lines

    return [pad + yaml_escape(obj)]

def main() -> int:
    if len(sys.argv) != 3:
        return 1
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "rb") as f:
        data = pickle.load(f)
        

    yaml_text = "\n".join(to_yaml(data))
    

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(yaml_text)

    return 0

if __name__ == __main__:
    main()