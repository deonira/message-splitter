import argparse
from msg_split import FragmentTooLargeError, split_html_structure



def main():
    parser = argparse.ArgumentParser(description="HTML Splitter Script")
    parser.add_argument("--max-len", type=int, required=True)
    parser.add_argument("file", type=str)
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {args.file} не найден.")
        return

    try:
        fragments = split_html_structure(html_content, max_len=args.max_len)

        for i, fragment in enumerate(fragments, 1):
            print(f"fragment #{i}: {len(fragment)} chars")
            print(fragment)
            print("-" * 40)

    except FragmentTooLargeError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()