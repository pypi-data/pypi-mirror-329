import argparse
import sys
from .processor import SPDXProcessor

def main():
    parser = argparse.ArgumentParser(description='Process SPDX files with different output formats')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--full', action='store_true', help='Generate full output')
    group.add_argument('-b', '--bin', action='store_true', help='Generate binary-focused output')
    group.add_argument('-m', '--min', action='store_true', help='Generate minimal output')
    parser.add_argument('--archive', default='system_extra.spdx.tar.zst', help='Path to the SPDX archive')
    
    args = parser.parse_args()
    
    try:
        processor = SPDXProcessor(args.archive)
        processor.load_data()
        
        if args.full:
            output = processor.process_full()
            output_file = 'full.txt'
        elif args.bin:
            output = processor.process_binaries()
            output_file = 'binaries.txt'
        else:  # args.min
            output = processor.process_minimal()
            output_file = 'minimal.txt'
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()