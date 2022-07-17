# Canvas-Scraper

Canvas Scraper is a Selenium-driven tool for students that will automatically go through each of the your courses and download all attached files.  

## Setup

Must have Python version 3 installed, and the correct version of [chromedriver](https://chromedriver.chromium.org/downloads) downloaded.

## Installation

First, clone the repository.

```bash
git clone
```

Create a new [venv](https://docs.python.org/3/library/venv.html) to run the script in, and activate it.

```bash
python3 -m venv canvas-scraper
cd canvas-scraper
source bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```
## Configuration

Edit the file *settings.conf* to include your canvas login information, the path to *chromedriver*, as well as the desired output location for the course data.

```yaml
login:
    username: eid1234
    passwd: pw123

save_location: /path/to/output/folder/

chromedriver_location: /path/to/chromedriver
```

## Usage
Now you are ready to run the scraper.
```bash
python scraper.py
```
*When the script is finished beginning the downloads, it will prompt you to wait until the downloads are finished to close out the script. Be patient.*

#### After Downloads Complete:
You can now run the separate script *rename_folders.py* in order to automatically rename the downloaded zip files to accurately represent the course they contain the files for.

```bash
python rename-folders.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
