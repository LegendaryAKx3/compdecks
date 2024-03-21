# compdecks

compdecks is a competitive quiz platform. It is written in python using flask, htmx, and tailwindcss.

## Install

**Be sure to use the same version of the code as the version of the docs you're reading.** You probably want the latest tagged version, but the default Git version is the main branch.

```
# clone the repository
$ git clone https://github.com/LegendaryAKx3/compdecks
$ cd compdecks
```

Create a virtualenv and activate it:

```
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Or on Windows cmd:

```
$ py -3 -m venv .venv
$ .venv\Scripts\activate.bat
```

Install compdecks and required packages:

```
$ pip install -e .
```

## Run

```
$ flask --app compdecks init-db
$ flask --app compdecks run --debug
```

Open http://127.0.0.1:5000 in a browser.

## Test

```
$ pip install '.[test]'
$ pytest
```

Run with coverage report:

```
$ coverage run -m pytest
$ coverage report
$ coverage html  # open htmlcov/index.html in a browser
```
