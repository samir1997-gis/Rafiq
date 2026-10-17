"""Upload finished videos to the owner's Google Drive, into a "Rafiq videos" folder (made on first use), at full quality.
Needs GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET and GDRIVE_REFRESH_TOKEN in the session's environment (owner, 13 Oct 2026);
the token's scope is drive.file, so it only sees files it made itself.
  python3 tools/drive-upload.py <file.mp4> [more files...]      → prints each file's Drive link"""
import json, mimetypes, os, sys, urllib.parse, urllib.request

FOLDER = "Rafiq videos"
def call(url, data=None, headers={}, method=None):
    r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers, method=method))
    return r.headers, r.read()

tok = json.loads(call("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
    "client_id": os.environ["GDRIVE_CLIENT_ID"], "client_secret": os.environ["GDRIVE_CLIENT_SECRET"],
    "refresh_token": os.environ["GDRIVE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode())[1])["access_token"]
auth = {"Authorization": "Bearer " + tok}

q = urllib.parse.quote(f"name='{FOLDER}' and mimeType='application/vnd.google-apps.folder' and trashed=false")
found = json.loads(call(f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id)", headers=auth)[1])["files"]
folder = found[0]["id"] if found else json.loads(call("https://www.googleapis.com/drive/v3/files", json.dumps(
    {"name": FOLDER, "mimeType": "application/vnd.google-apps.folder"}).encode(), {**auth, "Content-Type": "application/json"})[1])["id"]

for path in sys.argv[1:]:                                 # resumable upload: one session URL, then the whole file in one PUT
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    h, _ = call("https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,webViewLink",
                json.dumps({"name": os.path.basename(path), "parents": [folder]}).encode(),
                {**auth, "Content-Type": "application/json", "X-Upload-Content-Type": mime})
    with open(path, "rb") as f:
        meta = json.loads(call(h["Location"], f.read(), {"Content-Type": mime}, "PUT")[1])
    print(os.path.basename(path), meta["webViewLink"])
