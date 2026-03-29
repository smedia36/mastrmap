# stdlib
import os
import zipfile
from urllib.parse import urlparse

# third party
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def _session_with_retries():
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=(502, 503, 504))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s


def download(url: str, dest_path: str, chunk_size: int = 8192) -> str:
    """Download a URL to a local file with retries."""
    sess = _session_with_retries()
    r = sess.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(dest_path, "wb") as fh:
        for chunk in r.iter_content(chunk_size):
            if chunk:
                fh.write(chunk)
    return dest_path


def fetch_from_url(url: str, out_dir: str = "data") -> str:
    """Download a file from `url` into `out_dir`. If the download is a zip containing a CSV,
    the first CSV is extracted and its path is returned. Otherwise the downloaded path is returned.
    """
    os.makedirs(out_dir, exist_ok=True)
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "msdr_download"
    dest = os.path.join(out_dir, filename)
    download(url, dest)

    # If it's a zip file, extract the first CSV
    if zipfile.is_zipfile(dest):
        with zipfile.ZipFile(dest, "r") as z:
            for name in z.namelist():
                if name.lower().endswith(".csv"):
                    target = os.path.join(out_dir, os.path.basename(name))
                    with z.open(name) as src, open(target, "wb") as dst:
                        dst.write(src.read())
                    return target
    return dest
