# code-zipper

**code-zipper** is a command-line tool designed to copy multiple files and
directories directly to your clipboard.
Perfect for efficiently pasting code or text into ChatGPT!

---

## Features

- **Multiple Input Support:** Accepts files, directories, or glob patterns.
- **Structured Output:** Adds line numbers, file names, and sizes.
- **Clipboard Integration:** Aggregates content for instant pasting.
- **Minimal Dependencies:** Only uses two external libraries.

---

## Installation

Install via pip:

```bash
pip install code-zipper
```

Ensure Python and pip are installed on your system.
The tool is tested and supported for Python `3.10` and above.

---

## Usage

Once installed, run `code-zipper` from the command line
with desired paths or patterns:

```bash
code-zipper <file1> <folder2> <glob-pattern3>
```

Note that if you are passing just a folder, the tool with recursively
copy all `*.py` files within that directory.
This is handy if you want to copy all Python files in a project
like `code-zipper src`.

**Example:**

```bash
code-zipper src *.md tests/util/*.py
```

**Explanation:**
- `src` Copies every `*.py` file from the “src” folder (and any subfolders).
- `*.md` Matches all files ending with `.md` in the current directory.
- `tests/util/*.py` Matches only the `.py` files immediately  within the `tests/util` directory (subdirectories are not included).

For copying files from nested folders, use the folder name without a glob pattern.

**How It Works:**

1. **Input:** Provide a list of file paths, directories, or glob patterns.
2. **Processing:** Reads each file, concatenating contents while maintaining structure.
3. **Output:** Copies the combined result to your clipboard, ready for pasting.

Copied clipboard text will look like the following,
which can be reproduced using
`code-zipper src/cli.py` after having cloned the repo:

```
File: src/cli.py (84 lines and 2,015 chars)
   1 | """
   2 | A CLI tool that reads folders of code and copies it to the clipboard.
   3 | """
   4 | 
   5 | import argparse
   6 | import logging
   < ... more code >
  82 | 
  83 | if __name__ == "__main__":
  84 |     main()
```

Line numbers, file paths and sizes will help chatGPT better
navigate your code base and provide more accurate responses.

---

## FAQ

### How do I install code-zipper?
Install using pip as shown above.
Ensure you have a working Python `3.10` (or higher) environment.

### Are there any file type restrictions?
code-zipper works best with text-based files.
Binary files might not display correctly when pasted.

### Where can I report issues, suggest new features or contribute?
Issues, feature suggestions or improvements are very welcome!
For any of those, open a new
[GitHub issue](https://github.com/data-stepper/code-zipper/issues),
describe the problem or feature request, and we'll take it from there.

---

## License

Distributed under the MIT License. See the 
[LICENSE](https://github.com/data-stepper/code-zipper/blob/main/LICENSE)
file for more details.

---

Happy coding!
