# atai-web-tool

`atai-web-tool` is a command-line utility that extracts the main content from a webpage. It leverages [zendriver](https://pypi.org/project/zendriver/), [readability-lxml](https://pypi.org/project/readability-lxml/), and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to fetch pages, extract primary content, and display a clean, text-only version.

## Features

- **Headless Browsing:** Fetch webpages using zendriver.
- **Content Extraction:** Extract main content with readability-lxml.
- **Clean Output:** Remove unwanted HTML tags using BeautifulSoup.
- **Easy CLI:** Run from the terminal with a single command.

## Installation

You can install `atai-web-tool` via pip:

```bash
pip install atai-web-tool
```

If you prefer to install from source, clone the repository and run:

```bash
pip install .
```

## Usage

Extract the main content from a webpage by running:

```bash
atai-web-tool https://example.com
```

This command will open the specified URL, extract the primary content, and print it to the terminal.

## Requirements

- Python 3.6 or higher
- [zendriver](https://pypi.org/project/zendriver/)
- [readability-lxml](https://pypi.org/project/readability-lxml/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [lxml[html_clean]](https://pypi.org/project/lxml/)

## Development

For local development, install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements. For major changes, open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.