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
