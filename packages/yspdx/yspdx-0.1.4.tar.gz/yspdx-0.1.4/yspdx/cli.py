import argparse
import sys
from .processor import SPDXProcessor
import concurrent.futures


def generate_full_details(processor: SPDXProcessor, output_file: str):
    output = processor.process_full()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))


def generate_binary_details(processor, output_file):
    output = processor.process_binaries()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))


def generate_minmal_details(processor, output_file):
    output = processor.process_minimal()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))


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

    # If no optional argument is provided, enable all options
    if not (args.min or args.bin or args.full):
        args.min = True
        args.bin = True
        args.full = True

    try:
        processor = SPDXProcessor(args.archive)
        processor.load_data()

        # Handle combined options
        output = ""
        function_mapping = {  # (function, (arg1, arg2))
            "generate_minmal_details": (generate_minmal_details, (processor, '1non_build_recipes_only.txt')),
            "generate_binary_details": (generate_binary_details, (processor, '2non_build_binaries_only.txt')),
            "generate_full_details": (generate_full_details, (processor, '3with_build_deps_full.txt')),
        }

        # Get user choices
        selected_tasks = []
        if args.full:
            # generate_full_details(
            #     processor, output_file='3with_build_deps_full.txt')
            selected_tasks.append(function_mapping["generate_full_details"])
        if args.bin:
            # generate_binary_details(
            #     processor, output_file='2non_build_binaries_only.txt')
            selected_tasks.append(function_mapping["generate_binary_details"])
        if args.min:
            # generate_minmal_details(
            #     processor, output_file='1non_build_recipes_only.txt')
            selected_tasks.append(function_mapping["generate_minmal_details"])
        # Check if no options were selected
        # if not output:
        #     print("Error: No valid output options selected.", file=sys.stderr)
        #     sys.exit(1)

        # Execute selected functions in parallel (CPU bound)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(
                func, *args): func.__name__ for func, args in selected_tasks}

            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    # Only prints if result is none
                    print(f"{futures[future]} result: {future.result()}")
                else:
                    print(f"{futures[future]} done!")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
