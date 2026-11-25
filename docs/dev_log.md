# Development Log

## 2026-11-24 · Day 1

- Created the GitHub repo and wrote the README
- Learned what .gitignore does (don't upload secrets, rebuildable files, or big data)
- Set up the folder structure
- Installed uv and set up the Python environment (Python 3.12)
- Added libraries: requests, pandas, python-dotenv
- Learned: VS Code greys out files ignored by .gitignore (.venv is ignored, the lockfiles are committed)
- Explored the API response and wrote the data dictionary

## 2026-11-25 · Day 2

- Fixed repo: renamed data_dictionary.md, matched the API key name in .env, .env.example and the script
- Debugged the 502 errors: browser worked, script failed
- Tested one difference at a time: key, offset, page size, User-Agent
- Root cause: the server rejects requests with the default python-requests User-Agent (it returns 502)
- Fix: send a browser-like User-Agent header. First successful fetch: 644 tomato rows for 24-10-2026
