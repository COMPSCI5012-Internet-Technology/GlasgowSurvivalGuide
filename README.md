# GlasgowSurvivalGuide

Django project: Glasgow University survival guide (posts, comments, collections, news, user profiles). Supports local development and deployment to PythonAnywhere.

---

## Requirements

- **OS**: macOS / Linux / Windows (steps may vary)
- **Version control**: Git
- **Environment** (choose one):
  - **Conda** (Anaconda or Miniconda), or
  - **Python 3.10+** with **venv** and **requirements.txt**

---

## 1. Local environment (choose one)

### Option A: Conda

If Conda is installed:

```bash
cd path/to/GlasgowSurvivalGuide
conda env create -f environment.yml
conda activate GlasgowSurvivalGuide
```

### Option B: venv + requirements.txt

```bash
cd path/to/GlasgowSurvivalGuide
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Environment variables (optional)

The project reads settings from environment variables (see `GlasgowSurvivalGuide/settings.py`). For local development you can leave them unset; defaults will be used.

- `DEBUG`: defaults to `True` if unset
- `DJANGO_SECRET_KEY`: defaults to a dev key if unset (development only)
- `USE_MOCK_API`: `true` (default) uses mock news; `false` uses the real API
- `NEWSDATA_API_KEY`: required when using the real news API

You can copy `.env.example` to `.env` and fill in values; with **python-dotenv**, loading is done in code (at deploy time via WSGI; see PythonAnywhere section below).

---

## 3. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in a browser. Stop with `Ctrl+C`.

---

## 4. Project layout

```
GlasgowSurvivalGuide/
├── manage.py
├── requirements.txt
├── .env.example
├── wsgi_pythonanywhere_example.py   # WSGI example for deployment
├── .gitignore
├── README.md
├── environment.yml                  # Optional, for Conda
├── templates/
│   ├── base.html
│   └── guide/
│       ├── index.html, login.html, register.html, profile.html
│       ├── post_list.html, post_detail.html, post_form.html
│       ├── news_list.html
│       ├── collection_list.html, collection_detail.html, collection_form.html
│       └── ...
├── static/
├── media/
├── mock_data/
│   └── news.json                   # Mock news data
├── GlasgowSurvivalGuide/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── guide/                          # Main app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── context_processors.py       # Global user_profile
    ├── utils.py
    ├── services/
    │   └── news_service.py         # News API (Mock/Real)
    ├── management/commands/
    │   └── fetch_news.py           # Command: python manage.py fetch_news
    └── migrations/
```

Main routes (see `guide/urls.py`): home `/`, `/about/`, `/news/`, `/accounts/register|login|logout|profile/`, `/posts/` (list, create, detail, like, delete), `/collections/` (list, create, detail, add/remove posts, delete, toggle visibility), `/users/<id>/collections/`.

---

## 5. Dependency versions (reference)

| Package       | Requirement                    |
|---------------|--------------------------------|
| Python        | 3.10+                          |
| Django        | 5.2.x (see requirements.txt)    |
| Pillow        | 10+                            |
| python-dotenv | 1.0+                           |

---

## 6. News feature: Mock / Real API and news page

The project integrates the NewsData.io news API with **Mock mode** (offline, no API key) and **Real mode** (requires API key).

### 6.1 Viewing the news page

- **URL**: **http://127.0.0.1:8000/news/**
- Displays news stored in the database; the list may be empty until you run a fetch.

### 6.2 Mock mode (default, no key)

- Reads 5 fixed items from `mock_data/news.json`.
- Default is Mock; you can set `USE_MOCK_API=true` or leave it unset.

**Writing to the database** (choose one):

- **Command**: `python manage.py fetch_news`
- **Admin**: Log in at `/admin/` → **News** → select any row → Action **Fetch news (Mock/Real per settings)** → **Go**

Then refresh `/news/` to see the 5 items.

### 6.3 Real API (NewsData.io)

1. Sign up at [NewsData.io](https://newsdata.io/) and get an API key.
2. Set environment variables (do not put the key in code or git):
   - `NEWSDATA_API_KEY=your_key`
   - `USE_MOCK_API=false`
3. Use `python manage.py fetch_news` or Admin **Fetch news** as above.

### 6.4 Switching Mock / Real

| Mode  | Setting                           | Data source            |
|-------|-----------------------------------|------------------------|
| Mock  | Unset or `USE_MOCK_API=true`      | mock_data/news.json    |
| Real  | `USE_MOCK_API=false` + API key    | NewsData.io API        |

Restart Django (e.g. restart `runserver`) after changing the setting.

---

## 7. Deploy to PythonAnywhere (step-by-step)

Below are the full steps to deploy this project on **PythonAnywhere free tier**. The steps use `WEITSUNGCHENG` as the PythonAnywhere username; replace it with yours if different.

### 7.1 Prerequisites: local check

- Run `python manage.py check` in the project directory; it should report no issues.
- Ensure `requirements.txt` includes Django, Pillow, and python-dotenv.

### 7.2 Get the code

On PythonAnywhere open **Consoles** → **Bash**:

```bash
cd ~
git clone https://github.com/COMPSCI5012-Internet-Technology/GlasgowSurvivalGuide.git
cd GlasgowSurvivalGuide
```


### 7.3 Virtual environment and dependencies

In Bash:

```bash
python3.10 -m venv ~/.virtualenvs/glasgow_venv
source ~/.virtualenvs/glasgow_venv/bin/activate
cd ~/GlasgowSurvivalGuide
pip install --upgrade pip
pip install -r requirements.txt
python manage.py check
```

If Python 3.10 is not available, use `python3.9` etc. (must match the Web app Python version later).

### 7.4 Database and admin user

```bash
python manage.py migrate
python manage.py createsuperuser
```

Follow the prompts to set the admin username and password.

### 7.5 Create the Web app

1. Go to **Web** → **Add a new web app** → confirm domain → **Next**.
2. Choose **Manual configuration** (do not use the Django quick start).
3. Choose **Python 3.10** (same as your virtualenv) → **Next**.

### 7.6 Set the Virtualenv

In the **Web** tab, **Virtualenv** section:

- Enter: `/home/WEITSUNGCHENG/.virtualenvs/glasgow_venv`
- Click the green check to save.

### 7.7 Configure WSGI (load .env)

1. On the **Web** page, open **WSGI configuration file**.
2. Replace its **entire contents** with the contents of `wsgi_pythonanywhere_example.py` from the project.
3. The path uses `WEITSUNGCHENG`; change it to your PythonAnywhere username if different:

```python
path = "/home/WEITSUNGCHENG/GlasgowSurvivalGuide"
```

4. Save. This will load `.env` from the project directory (created in the next step).

### 7.8 Create .env (environment variables)

Create a `.env` file in the project directory so WSGI can load it via python-dotenv.

**Files**: Go to `/home/WEITSUNGCHENG/GlasgowSurvivalGuide/` → **New file** → name it `.env`.

Or in **Bash**:

```bash
cd ~/GlasgowSurvivalGuide
nano .env
```

Example contents (for production set `DEBUG=False` and a random `DJANGO_SECRET_KEY`):

```
DEBUG=False
DJANGO_SECRET_KEY=your-random-secret-key
USE_MOCK_API=true
NEWSDATA_API_KEY=
```

Save (nano: Ctrl+O, Enter, Ctrl+X). Do not commit `.env` to version control.

### 7.9 Static and Media mapping

In the **Web** page **Static files** section, add two entries:

| URL         | Directory                                                                 |
|-------------|----------------------------------------------------------------------------|
| `/static/`  | `/home/WEITSUNGCHENG/GlasgowSurvivalGuide/staticfiles/`                    |
| `/media/`   | `/home/WEITSUNGCHENG/GlasgowSurvivalGuide/media/`                          |

Note: `/static/` must point to **staticfiles** (the output of collectstatic), not the `static` directory.

### 7.10 Run collectstatic

In Bash (with the virtualenv activated):

```bash
cd ~/GlasgowSurvivalGuide
source ~/.virtualenvs/glasgow_venv/bin/activate
python manage.py collectstatic --noinput
```

### 7.11 Fix existing users without profile (optional)

If you see "User has no profile", create UserProfile for existing users:

```bash
python manage.py shell
```

In the shell:

```python
from django.contrib.auth import get_user_model
from guide.models import UserProfile
User = get_user_model()
for u in User.objects.all():
    UserProfile.objects.get_or_create(user=u, defaults={"email": u.email or ""})
exit()
```

### 7.12 Reload and verify

1. On the **Web** page click the green **Reload** button.
2. Open **https://weitsungcheng.pythonanywhere.com/** in a browser.
3. Check home, login/register, post list, news page, etc.
4. To refresh news: log in at **/admin/** → **News** → Action **Fetch news (Mock/Real per settings)** → **Go**, then check `/news/`.

### 7.13 Updating the code later

If you deploy with Git, when updating:

```bash
cd ~/GlasgowSurvivalGuide
git pull
source ~/.virtualenvs/glasgow_venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** on the **Web** page.

---

## 8. Reference docs

- Project scope and acceptance criteria: `docs/`
- Data model: `docs/model_attribute_list.md`
- System architecture and service layer: `docs/system_architecture_diagram.md`
