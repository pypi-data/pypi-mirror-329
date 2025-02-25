# yspdx

A Python package for processing several SPDX (Software Package Data Exchange) files generated from create-spdx.bbclass with different output formats.

## Installation

```bash
pip install yspdx
```

## Usage

The package provides a command-line interface with three different output modes:

1. Full output (-f or --full):
```bash
yspdx -f
```

2. Binary-focused output (-b or --bin):
```bash
yspdx -b
```

3. Minimal output (-m or --min):
```bash
yspdx -m
```

By default, the tool looks for a file named `system_extra.spdx.tar.zst` in the current directory. You can specify a different archive path using the --archive option:

```bash
yspdx -f --archive /path/to/your/archive.spdx.tar.zst
```

## Output Files

The tool generates different output files based on the mode:
- Full mode: `full.txt`
- Binary mode: `binaries.txt`
- Minimal mode: `minimal.txt`

## Author

Dinesh Ravi

## License
Copyright (c) 2025 Dinesh Ravi
GPL-3.0+ License

