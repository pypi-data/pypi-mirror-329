"""Fizzy - Fizz and Defizz your text, by Kreusada."""

CHARS = [
    "𖫩", "᧐", "O", "꯰", "°", "О", "о", "ₒ", "Ⓞ", "𐓂",  
    "𐓪", "𐔖", "𐖮", "𐤬", "𛱄", "ⓞ", "Ⲟ", "ⲟ", "ꓳ", "ꝏ",  
    "Ꝏ", "Ｏ", "ｏ", "𐊫", "𐌏", "᳃", "߀", "०", "০", "*",  
    "੦", "૦", "🇴", "𑵐", "᛫", "୦", "௦", "౦", "೦", "൦",  
    "๐", "໐", "၀", "᥆", "᠐", "0", "᪀", "᪐", "᭐", "᮰",  
    "᱀", "᱐", "⁰", "₀", "〇", "꣐", "꤀", "꧐", "꩐", ".",  
    "𐒠", "𐴰", "０", "𑃰"
]


class Error(Exception):
    pass


def fizz(text: str):
    """Make your text fizzy."""
    ret = []
    for char in text:
        code = ord(char)

        if code in range(32):
            raise Error("Control characters are forbidden")

        current = ""

        while code != 0:
            code, rem = divmod(code, 64)
            current += CHARS[rem]

        ret.append(current)
    return "o".join(ret)


def defizz(text: str) -> str:
    """Defizz your text. Valid fizzy characters are expected."""
    if not isfizzy(text):
        raise Error("Given text isn't fizzy.")

    ret = []
    for chars in text.split("o"):
        rems = [CHARS.index(char) for char in chars]

        n = 0
        for rem in reversed(rems):
            n = (n * 64) + rem

        if n in range(32):
            raise Error("Forbidden control character detected during defizzing")

        ret.append(chr(n))

    return "".join(ret)


def isfizzy(text: str) -> bool:
    """Check whether the text is fizzy."""
    return (
        not text.startswith("o")
        and not text.endswith("o")
        and all(c in CHARS for c in text.replace("o", ""))
    )

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    fizz_parser = subparsers.add_parser("fizz", help=fizz.__doc__)
    fizz_parser.add_argument("text", type=str, help="Text to fizz", nargs="+")

    defizz_parser = subparsers.add_parser("defizz", help=defizz.__doc__)
    defizz_parser.add_argument("text", type=str, help="Text to defizz")

    args = parser.parse_args()

    if not args.command:
        return parser.print_help()

    arg = " ".join(args.text) if args.command == "fizz" else args.text

    try:
        print(globals()[args.command](arg))
    except Error as e:
        print("Error:", e)
        sys.exit(2)


if __name__ == "__main__":
    main()
