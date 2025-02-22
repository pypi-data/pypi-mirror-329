import argparse
import sys
from .processor import SPDXProcessor


def main():
    parser = argparse.ArgumentParser(
        description='Process SPDX files with different output formats')

    parser.add_argument(
        '--archive', default='system_extra.spdx.tar.zst', help='Path to the SPDX archive. defaults to system_extra.spdx.tar.zst')
    # Allow multiple options
    parser.add_argument('-m', '--min', action='store_true',
                        help='Generate minimal output ex:1non_build_recipes_only.txt')
    parser.add_argument('-b', '--bin', action='store_true',
                        help='Generate binary-focused output ex:2non_build_binaries_only.txt')
    parser.add_argument('-f', '--full', action='store_true',
                        help='Generate full output ex:3with_build_deps_full.txt')

    args = parser.parse_args()

    try:
        processor = SPDXProcessor(args.archive)
        processor.load_data()

        # Handle combined options
        output = ""
        output_file = ''

        if args.full:
            output = processor.process_full()
            output_file = '3with_build_deps_full.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
        if args.bin:
            output = processor.process_binaries()
            output_file = '2non_build_binaries_only.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
        if args.min:
            output = processor.process_minimal()
            output_file = '1non_build_recipes_only.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))

        # Check if no options were selected
        if not output:
            print("Error: No valid output options selected.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
