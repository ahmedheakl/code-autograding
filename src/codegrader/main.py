"""Main library runner"""
import argparse

from transcoder.translate import translate


def parse_args():
    """Argument parser"""
    parser = argparse.ArgumentParser(description="CodeGrader")
    parser.add_argument(
        "-s", "--src_lang", type=str, default="cpp", help="Source Lanuage"
    )
    parser.add_argument(
        "-t", "--trg_lang", type=str, default="python", help="Target Language"
    )
    parser.add_argument("-f", "--file", help="Input file")
    return parser.parse_args()


def main():
    """Main library runner"""
    args = parse_args()
    with open(args.file, "r", encoding="utf-8") as file:
        code = file.read()
    output = translate(src_lang=args.src_lang, tgt_lang=args.trg_lang, input_code=code)
    for out in output:
        print(out)
