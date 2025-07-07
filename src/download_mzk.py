import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL to the directory containing this file and linked .htm files
BASE_URL = "https://www.mzk.zamosc.pl/pliki/rozklad/"  # ← change if needed
INDEX_FILE = "0008/w.htm"  # ← your file listing stops for line 8
SAVE_DIR = "htm/linia_8"

def download_line_8_stops():
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Load main line page
    index_url = urljoin(BASE_URL, INDEX_FILE)
    print(f"📥 Downloading index: {index_url}")
    response = requests.get(index_url)
    response.encoding = 'iso-8859-2'

    if response.status_code != 200:
        print(f"❌ Failed to load index page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all linked .htm stop pages
    links = soup.find_all('a', href=True)
    stop_files = set()

    for link in links:
        href = link['href']
        if href.lower().endswith('.htm') and href.lower().startswith('0008t'):
            stop_files.add(href)

    print(f"🔗 Found {len(stop_files)} stop files.")

    for href in sorted(stop_files):
        full_url = urljoin(index_url, href)
        filename = os.path.basename(href)
        save_path = os.path.join(SAVE_DIR, filename)

        print(f"⬇️  Downloading {href} → {filename}")
        file_resp = requests.get(full_url)
        file_resp.encoding = 'iso-8859-2'

        if file_resp.status_code == 200:
            with open(save_path, 'w', encoding='iso-8859-2') as f:
                f.write(file_resp.text)
        else:
            print(f"⚠️  Failed to fetch {href}: {file_resp.status_code}")

    print("✅ All stops downloaded for Linia 8.")


BASE_URL = "https://www.mzk.zamosc.pl/pliki/rozklad/"
SAVE_BASE_DIR = "htm_all_linie"

def download_all_lines(from_line=0, to_line=56):
    for line_number in range(from_line, to_line + 1):
        line_id = f"{line_number:04d}"
        folder_path = f"{line_id}/"
        index_file = "w.htm"
        index_url = urljoin(BASE_URL, folder_path + index_file)
        save_dir = os.path.join(SAVE_BASE_DIR, f"linia_{line_id}")
        os.makedirs(save_dir, exist_ok=True)

        print(f"\n📥 Downloading index for linia {line_id}: {index_url}")
        try:
            response = requests.get(index_url)
            response.encoding = 'iso-8859-2'
            if response.status_code != 200:
                print(f"❌ Failed to load {index_url}: {response.status_code}")
                continue
        except Exception as e:
            print(f"⚠️  Error requesting {index_url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        stop_files = set()

        for link in links:
            href = link['href']
            if href.lower().endswith('.htm') and href.lower().startswith(f"{line_id}t"):
                stop_files.add(href)

        print(f"🔗 Found {len(stop_files)} stop files for line {line_id}")

        for href in sorted(stop_files):
            full_url = urljoin(index_url, href)
            filename = os.path.basename(href)
            save_path = os.path.join(save_dir, filename)

            try:
                file_resp = requests.get(full_url)
                file_resp.encoding = 'iso-8859-2'
                if file_resp.status_code == 200:
                    with open(save_path, 'w', encoding='iso-8859-2') as f:
                        f.write(file_resp.text)
                    print(f"✅ Saved {filename}")
                else:
                    print(f"❌ Failed to fetch {href}: {file_resp.status_code}")
            except Exception as e:
                print(f"⚠️  Error fetching {href}: {e}")

    print("\n🏁 Done downloading all available line schedules.")

download_all_lines(0, 56)
