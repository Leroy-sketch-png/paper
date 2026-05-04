"""
Resumable download of falcon.zip from Zenodo.
Uses HTTP Range requests to resume interrupted downloads.
"""
import urllib.request
import os
import time
import sys

URL = "https://zenodo.org/records/18897073/files/falcon.zip?download=1"
DEST = r"c:\Users\YOGA\Downloads\research\falcon.zip"

def download_with_resume(url, dest, chunk_size=1024*1024, max_retries=20):
    existing = os.path.getsize(dest) if os.path.exists(dest) else 0
    print(f"Starting download. Existing: {existing/1024/1024:.2f} MB")

    for attempt in range(max_retries):
        try:
            current_size = os.path.getsize(dest) if os.path.exists(dest) else 0
            headers = {}
            if current_size > 0:
                headers["Range"] = f"bytes={current_size}-"
                print(f"[attempt {attempt+1}] Resuming from {current_size/1024/1024:.2f} MB")
            else:
                print(f"[attempt {attempt+1}] Starting fresh")

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                mode = "ab" if current_size > 0 else "wb"
                with open(dest, mode) as f:
                    downloaded = current_size
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        total_mb = downloaded / 1024 / 1024
                        sys.stdout.write(f"\r  {total_mb:.2f} MB downloaded")
                        sys.stdout.flush()
            print(f"\nDone! Total: {os.path.getsize(dest)/1024/1024:.2f} MB")
            return True

        except Exception as e:
            current = os.path.getsize(dest) if os.path.exists(dest) else 0
            print(f"\n  Error: {e} (at {current/1024/1024:.2f} MB)")
            if attempt < max_retries - 1:
                wait = min(30, (attempt + 1) * 3)
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("Max retries exceeded.")
                return False

download_with_resume(URL, DEST)
final = os.path.getsize(DEST) if os.path.exists(DEST) else 0
print(f"Final file size: {final/1024/1024:.2f} MB")
