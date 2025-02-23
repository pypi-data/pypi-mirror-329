import argparse
import json
from parse import find_cell_references

def main():
    parser = argparse.ArgumentParser(description="Parse an XLSX file.")
    parser.add_argument("file", help="Path to the XLSX file")
    parser.add_argument("--sheet", default=None, help="Sheet name or index")
    args = parser.parse_args()

    df = find_cell_references(args.file, args.sheet)
    print(df)

if __name__ == "__main__":
    main()
