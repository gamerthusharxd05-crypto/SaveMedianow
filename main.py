from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Save Media API Running"}

@app.get("/fetch")
def fetch_video(url: str = Query(...)):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get("formats", []):
            if f.get("ext") == "mp4" and f.get("height"):
                formats.append({
                    "quality": f"{f.get('height')}p",
                    "url": f.get("url"),
                    "filesize": f.get("filesize", "N/A")
                })

        return {
            "title": info.get("title"),
            "formats": sorted(formats, key=lambda x: x["quality"], reverse=True)[:6]
        }

    except Exception as e:
        return {"error": str(e)}