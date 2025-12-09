import os
import time
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your host (Render/Railway)
OPENAI_BASE = os.getenv("OPENAI_BASE", "https://api.openai.com/v1")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json"
}

@app.route("/generate", methods=["POST"])
def generate():
    body = request.json or {}
    prompt = body.get("prompt", "").strip()
    if not prompt:
        return jsonify({"status":"error","error":"prompt required"}), 400

    payload = {
        "model": "sora-2",
        "input": {
            "text": prompt,
            "duration": body.get("duration", 5),
            "style": body.get("style", "cinematic")
        }
    }

    create_url = f"{OPENAI_BASE}/videos"

    r = requests.post(create_url, headers=HEADERS, json=payload)
    if r.status_code >= 400:
        return jsonify({"status":"error","error": r.text}), 500

    job = r.json()
    job_id = job.get("id") or job.get("job_id")
    if job.get("status") == "succeeded" and job.get("result"):
        return jsonify({"status":"success","video_url": job["result"].get("url")})

    poll_url = f"{create_url}/{job_id}" if job_id else None
    if not poll_url:
        return jsonify({"status":"error","error":"no job id returned","raw": job}), 500

    timeout = 60 * 3
    elapsed = 0
    interval = 3
    while elapsed < timeout:
        pr = requests.get(poll_url, headers=HEADERS)
        if pr.status_code >= 400:
            return jsonify({"status":"error","error": pr.text}), 500
        pdata = pr.json()
        if pdata.get("status") == "succeeded":
            video_url = pdata.get("result", {}).get("url")
            return jsonify({"status":"success","video_url": video_url})
        elif pdata.get("status") in ("failed","errored"):
            return jsonify({"status":"error","error": pdata.get("error","generation failed")}), 500

        time.sleep(interval)
        elapsed += interval

    return jsonify({"status":"pending","message":"generation taking longer than expected; implement webhooks for production","job": job}), 202

@app.route("/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
