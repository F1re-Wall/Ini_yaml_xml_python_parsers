import sys
import pickle
import yaml


def main() -> int:
    if len(sys.argv) != 3:
        return 1

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "rb") as f:
        data = pickle.load(f)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return 0


if __name__ == __main__:
    main()