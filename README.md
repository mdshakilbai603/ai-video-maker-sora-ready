# ai-video-maker-sora-ready

Text-to-Video web app (Frontend + Flask backend) configured for OpenAI Sora (sora-2).
**NOTE:** You must set your `OPENAI_API_KEY` in the host environment (Render/Railway/etc).

## Repo structure
- backend/ (Flask API)
  - app.py
  - requirements.txt
  - .env.example
- frontend/ (Static site for Netlify)
  - index.html, style.css, script.js
- Dockerfile
- .gitignore
- README.md

## Quick local run (dev)
1. Copy `.env.example` to `.env` and put your `OPENAI_API_KEY`.
2. Backend:
   ```
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
3. Frontend:
   Open `frontend/index.html` in your browser (or serve it with any static server).

## Deploy plan (recommended)
- Host backend on Render / Railway / Heroku / VPS using Docker or Python.
- Host frontend on Netlify (connect to GitHub repo, set build dir to `/frontend`).

## GitHub (Web UI) — What to enter when creating a repo
When you open https://github.com/new, use these exact values:

- **Repository name:** `ai-video-maker-sora-ready`
- **Description (optional):** `Text-to-Video web app using OpenAI Sora (frontend + Flask backend)`
- **Visibility:** `Public` (or Private if you prefer)
- **Add a README:** Optional (you can leave off, README.md already in repo)
- **Add .gitignore:** Choose `No .gitignore` in web UI (we include one) or select `Python`
- **Add a license:** Optional

After creating the empty repo, upload files:
- On the repo page click **"Add file" → "Upload files"**
- Drag & drop entire project folders (backend, frontend, Dockerfile, README.md, .gitignore)
- Commit changes (write a commit message like: `initial commit: add Sora-ready project`)
- OR clone locally and push via git:
  ```
  git clone https://github.com/<your-username>/ai-video-maker-sora-ready.git
  cp -r path/to/project/* ai-video-maker-sora-ready/
  cd ai-video-maker-sora-ready
  git add .
  git commit -m "initial commit: add project"
  git push origin main
  ```

## Netlify deploy (frontend)
1. Go to https://app.netlify.com/ and login.
2. Click **"New site from Git"** → Connect to GitHub → select repo `ai-video-maker-sora-ready`.
3. In **Deploy settings**:
   - **Branch to deploy:** `main`
   - **Build command:** *(leave empty for plain static)* 
   - **Publish directory:** `frontend`
4. Deploy site.
5. After deploy, set an environment variable if your backend is on a separate host:
   - In Netlify Site settings → Build & deploy → Environment → Add variable: `BACKEND_URL` = `https://your-backend-url`
   - Edit `frontend/script.js` to use `const API_BASE = BACKEND_URL` or set it via Netlify header injection.

## Render / Railway (backend)
- Use Dockerfile or direct Python deploy. Set `OPENAI_API_KEY` env var in the host dashboard.

## Support
If you want, I can provide the exact `render.yaml` / `railway` steps and help troubleshoot deployment logs.
