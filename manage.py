from parser_ydzen.parser.services.base import ManageParser
import sys


def main():
    options = sys.argv[1:]
    try:
        service = ManageParser.manage_service(options)
    except Exception as ex:
        raise ex

    service.execute()

if __name__ == '__main__':
    main()





