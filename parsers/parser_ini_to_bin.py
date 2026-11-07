import sys
import pickle

class IniError(Exception):
    pass


def remove_inline_comment(line: str) -> str:
    quote = None
    escaped = False

    for i, ch in enumerate(line):
        if escaped:
            escaped = False
            continue

        if ch == "\\":
            escaped = True
            continue

        if quote is not None:
            if ch == quote:
                quote = None
        else:
            if ch in ('"', "'"):
                quote = ch
            elif ch in (";", "#"):
                if i == 0 or line[i - 1].isspace():
                    return line[:i]

    return line


def parse_ini(text: str) -> dict:
    root = {}
    current = None

    for lineno, raw_line in enumerate(text.splitlines(), 1):
        line = remove_inline_comment(raw_line).strip()

        if not line:
            continue

        if line.startswith("["):
            if not line.endswith("]"):
                raise IniError(f"Строка {lineno}: ожидался закрывающий ']'")

            section_name = line[1:-1].strip()
            if not section_name:
                raise IniError(f"Строка {lineno}: пустое имя секции")

            if section_name in root:
                raise IniError(f"Строка {lineno}: повторная секция {section_name!r}")

            current = {}
            root[section_name] = current
            continue

        if "=" not in line:
            raise IniError(f"Строка {lineno}: ожидался символ '='")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise IniError(f"Строка {lineno}: пустой ключ")

        target = root if current is None else current

        if key in target:
            old = target[key]
            if isinstance(old, list):
                old.append(value)
            else:
                target[key] = [old, value]
        else:
            target[key] = value

    return root

def main() -> int:
    if len(sys.argv) != 3:
        return 1
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        ini_text = f.read()

    data = parse_ini(ini_text)

    with open(output_path, "wb") as f:
        pickle.dump(data, f)

    return 0

if __name__ == __main__:
    main()