# Js-Scripts - Static HTML GitHub Pages

A static HTML GitHub Pages site for displaying scripts with embedded YouTube videos. No build tools required!

## Setup Instructions

1. **Update `scripts-config.json`**:
   - Add your scripts in the `fivem_scripts` array with:
     - `name`: Display name of the script
     - `repo`: GitHub repository in format "username/repo-name"
     - `youtube_id`: YouTube video ID (the part after v= in the URL)

2. **Test locally**:
   - Simply open `index.html` in your browser, or
   - Use a local server: `python -m http.server` or `npx serve`
   - Visit `http://localhost:8000` to preview

3. **Deploy to GitHub Pages**:
   - Push this repository to GitHub
   - Enable GitHub Pages in repository settings
   - Select "Deploy from a branch" as the source
   - Choose `main` branch and `/ (root)` folder
   - The site will automatically deploy

## Adding New Scripts

**Easy Method**: Run the Python script to manage scripts interactively:
```bash
.venv\Scripts\activate
python manage_scripts.py
```

The script provides options to:
- List all current scripts
- Add new scripts (manual entry or from URLs)
- Batch mode for adding multiple scripts quickly
- Remove scripts

**Manual Method**: Edit `scripts-config.json` and add entries to the `fivem_scripts` array:

```json
{
  "fivem_scripts": [
    {
      "name": "Your Script Name",
      "repo": "your-username/your-repo",
      "youtube_id": "youtube-video-id"
    }
  ]
}
```

## Features

- Dark mode UI
- Responsive design
- GitHub API integration for repository stats
- Embedded YouTube videos
- Auto-load videos (no auto-play with sound)
- Configurable script list

## YouTube Video IDs

To find a YouTube video ID:
1. Go to the video on YouTube
2. The URL will be like: `https://www.youtube.com/watch?v=VIDEO_ID`
3. Copy the `VIDEO_ID` portion
