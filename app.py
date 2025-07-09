from flask import Flask, request, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_info = None
    formats = []
    download_url = ""
    error = ""

    if request.method == "POST":
        url = request.form["url"]
        selected_format = request.form.get("format_id")

        ydl_opts = {"quiet": True, "no_warnings": True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = [f for f in info["formats"] if f.get("url") and f.get("ext") in ["mp4", "webm", "m4a"]]

                if selected_format:
                    for f in formats:
                        if f["format_id"] == selected_format:
                            download_url = f["url"]
                            break

                video_info = {
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "thumbnail": info.get("thumbnail"),
                    "url": url,
                }
        except Exception as e:
            error = str(e)

    return render_template("index.html", info=video_info, formats=formats, download_url=download_url, error=error)


if __name__ == "__main__":
    app.run(debug=True)
