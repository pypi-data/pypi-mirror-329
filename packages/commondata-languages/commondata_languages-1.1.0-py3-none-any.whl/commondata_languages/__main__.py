import sys

from commondata_languages import LanguageData


def main():
    language_data = LanguageData()
    print(language_data[" ".join(sys.argv[1:])])


if __name__ == "__main__":
    main()
