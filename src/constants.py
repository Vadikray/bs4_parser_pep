from pathlib import Path

# urls
MAIN_DOC_URL = "https://docs.python.org/3/"
MAIN_PEP_URL = "https://peps.python.org/"
# dirs & files
BASE_DIR = Path(__file__).parent
# format
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = "%d.%m.%Y %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
# literals
DOWNLOAD = 'downloads'
DOWNLOAD_HTML = "download.html"
WHATSNEW = 'whatsnew/'
RESULTS = 'results'
PRETTY = 'pretty'
FILE = 'file'
# data
EXPECTED_STATUS = {
    "A": ["Active", "Accepted"],
    "D": ["Deferred"],
    "F": ["Final"],
    "P": ["Provisional"],
    "R": ["Rejected"],
    "S": ["Superseded"],
    "W": ["Withdrawn"],
    "": ["Draft", "Active"],
}
