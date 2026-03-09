# GlasgowSurvivalGuide

## Requirements

- **OS**: macOS (or Linux/Windows with equivalent steps)
- **Version control**: Git
- **Environment**: Conda (Anaconda or Miniconda)

## 1. Install Conda

If Conda is not installed:

1. Download from [Anaconda](https://www.anaconda.com/download/)
2. Restart the terminal; `conda` should be available

## 2. Create the environment

In a terminal, go to the project root and run:

```bash
cd path/to/GlasgowSurvivalGuide

conda env create -f environment.yml
conda activate GlasgowSurvivalGuide
```

To recreate the environment:

```bash
conda env remove -n GlasgowSurvivalGuide
conda env create -f environment.yml
conda activate GlasgowSurvivalGuide
```

## 3. Run the development server

With the environment activated:

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in a browser. Stop the server with `Ctrl+C`.

## 4. Project layout

```
GlasgowSurvivalGuide/
├── manage.py
├── environment.yml
├── .gitignore
├── README.md
├── templates/
│   └── guide/
├── static/
├── media/
├── GlasgowSurvivalGuide/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── guide/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── ...
```

## 5. Pinned versions

| Component | Version  |
|-----------|----------|
| Python    | 3.12.8   |
| Django    | 5.2.12   |
| Pillow    | 10.4.0   |
| pip       | 24.3.2   |

## 6. News feature: API key, Mock data, and news page

The project integrates the NewsData.io news API with **Mock mode** (offline, no API key) and **Real mode** (requires API key). This section explains how to set the API key, how to view the news page, and how to use Mock data.

### 6.1 Viewing the news page

- **URL**: With the server running, open **http://127.0.0.1:8000/news/** in your browser.
- The page shows the list of news stored in the database (title, time, summary, link). If you have not run a fetch yet, the list may be empty; follow the steps below to fetch news first.

### 6.2 Using Mock data (no API key, works offline)

Mock mode reads 5 fixed news items from **mock_data/news.json**. No API key or internet connection is required.

**Ensure Mock mode is active**

- Mock is the default; no setup needed.
- If you changed environment variables before, either leave `USE_MOCK_API` unset or set `USE_MOCK_API=true` (or `1`).

**Fetching news (write Mock data into the database)**

Use either method once; then open `/news/` to see the 5 items.

**Option A – Command line**

```bash
conda activate GlasgowSurvivalGuide
cd path/to/GlasgowSurvivalGuide
python manage.py fetch_news
```

**Option B – Django Admin**

1. Open **http://127.0.0.1:8000/admin/** and log in.
2. Go to **News**.
3. Select at least one news item (required by Django; the action ignores selection and replaces all news).
4. In the **Action** dropdown choose **Fetch news (Mock/Real per settings)**, then click **Go**.
5. You should see a success message such as "Fetched and saved 5 news item(s).".

Then open **http://127.0.0.1:8000/news/** to see the 5 items from **mock_data/news.json**.

### 6.3 Setting the API key (Real NewsData.io news)

To use the **real API** (latest Glasgow-related news from NewsData.io):

1. Get an API key from [NewsData.io](https://newsdata.io/) (sign up and create a key).
2. Set the key as an environment variable (see below). **Do not put the key in code or commit it to git.**

**Method 1 – Conda environment variables (recommended; set once)**

Run (replace `your_actual_key` with your real key):

```bash
conda activate GlasgowSurvivalGuide
conda env config vars set NEWSDATA_API_KEY=your_actual_key
conda env config vars set USE_MOCK_API=false
```

Reactivate the environment so the variables take effect:

```bash
conda deactivate
conda activate GlasgowSurvivalGuide
```

After that, `runserver` and `fetch_news` in this environment will use the real API without typing the key again.

**Viewing variables you set**

```bash
conda activate GlasgowSurvivalGuide
conda env config vars list
```

**Method 2 – Export in the current terminal (temporary)**

In the same terminal where you run the project:

```bash
export NEWSDATA_API_KEY=your_actual_key
export USE_MOCK_API=false
```

Then run `python manage.py runserver` or `python manage.py fetch_news`. You must export again after closing the terminal.

**Fetching with the real API**

- Command line: `python manage.py fetch_news`
- Admin: Same as Option B in 6.2; choose "Fetch news (Mock/Real per settings)" and click Go.

On success, the database is updated with 5 items from NewsData.io. On failure (e.g. invalid key, no network), existing news is kept and errors are logged.

### 6.4 Switching between Mock and Real

| Mode        | Setting                          | Data source          |
|-------------|----------------------------------|----------------------|
| **Mock** (default) | Unset or `USE_MOCK_API=true`     | mock_data/news.json |
| **Real**    | `USE_MOCK_API=false` and `NEWSDATA_API_KEY` set | NewsData.io API      |

After changing the setting, restart the Django process (e.g. restart `runserver`) for it to take effect.

### 6.5 Notes for shared projects

- **API key and env vars**: Do not put `NEWSDATA_API_KEY` in code or in version control. Use Conda or `export`; the key stays only in your local environment.
- **Collaboration**: Each team member sets their own API key locally (or uses Mock). Conda `env config vars` are per machine and are not shared via git.
