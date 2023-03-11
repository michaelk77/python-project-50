import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', help='Path to the first file')
    parser.add_argument('second_file', help='Path to the second file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()

    print(args.first_file)
    print(args.second_file)
    print(args.format)

    # TODO: Implement file comparison logic here


if __name__ == '__main__':
    main()
