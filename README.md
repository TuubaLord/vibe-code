# PDF Notes App

This simple Flask application lets you store links to PDF articles and leave comments about them.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Alternatively, run `./create_venv.sh` to set up the environment automatically.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   flask --app app run
   ```

The application uses a local SQLite database (`database.db`) created on first run.
