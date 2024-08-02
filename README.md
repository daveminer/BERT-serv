     _______  _______  ______    _______         _______  _______  ______    __   __
    |  _    ||       ||    _ |  |       |       |       ||       ||    _ |  |  | |  |
    | |_|   ||    ___||   | ||  |_     _| ____  |  _____||    ___||   | ||  |  |_|  |
    |       ||   |___ |   |_||_   |   |  |____| | |_____ |   |___ |   |_||_ |       |
    |  _   | |    ___||    __  |  |   |         |_____  ||    ___||    __  ||       |
    | |_|   ||   |___ |   |  | |  |   |          _____| ||   |___ |   |  | | |     |
    |_______||_______||___|  |_|  |___|         |_______||_______||___|  |_|  |___|

[![BERT-serv CI](https://github.com/daveminer/BERT-serv/actions/workflows/ci.yml/badge.svg)](https://github.com/daveminer/BERT-serv/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/daveminer/BERT-serv/branch/main/graph/badge.svg?token=jMMlzwBmhi)](https://codecov.io/gh/daveminer/BERT-serv)

**BERT-serv** provides [FinBERT](https://github.com/ProsusAI/finBERT) sentiment as a service. Send financial text via HTTP and get sentiment analysis back from [these pretrained models](https://github.com/yya518/FinBERT).

:exclamation: Only [this sentiment model](https://huggingface.co/yiyanghkust/finbert-tone) is implemented at this time.

## Why

- FinBERT analysis made available on-demand to HTTP clients (no Python required!)
- Avoid adding [PyTorch](https://pytorch.org/) dependencies to other parts of your system
- Results are saved and can be queried
- Analysis requests are handled asynchronously

## Run the Local Demo

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if needed.

```
git clone https://github.com/daveminer/BERT-serv.git
cd BERT-serv
cp .env.dist .env
docker-compose up
```

BERT-serv is now running on local port 8000!

## How to Use

### Request sentiment analysis on text

Send a POST request to the `/sentiment/new/` path. A `callback_url` may be specified in
the query parameters for asynchrous use cases and long-running sentiment analyses. This callback
will have a JSON object in the body with an array of the new sentiment record `id`s: `'{"ids": [95, 96]}'`

The body of the POST request must be a list; the strings inside will be processed synchronously.

```
curl --request POST \
  --url 'http://localhost:8000/sentiment/new/?callback_url=http%3A%2F%2Fweb%3A8000%2Fcallback%2Fsentiment%2Fnew%2F' \
  --header 'Content-Type: application/json' \
  --data '[
	"there is a shortage of capital, and we need extra financing",
	"year over year growth is increasing"
]'
```

### Look up sentiment results

Response defaults to HTML unless `application/json` is specified in the `Accept` header.

##### Get last 100 sentiments

Make a GET request to the `/sentiment/` path.

```
curl --request GET \
  --url http://localhost:8000/sentiment/ \
  --header 'Accept: application/json'
```

##### Get a specific sentiment by index

Add the index of the sentiment resource to the `sentiment` path:

```
curl --request GET \
  --url http://localhost:8000/sentiment/1/ \
  --header 'Accept: application/json'
```

### Filter sentiments

##### By Tag

A comma-separated list of tags may be specified in the `tags` query parameter.

##### By Age

The `period` query parameter accepts an integer that specifies how many days back to look for sentiments.

### Pagination

The sentiment index controller uses Django's built in [pagination](https://docs.djangoproject.com/en/5.0/topics/pagination/).
The `/sentiment/` path accepts `page_size` and a `page` query parameters.

## Development Environment Setup

The `make services` command will start all of the services besides the app. This allows for the app to be started and stopped (with `make app`) in the terminal for convenience during development.

### Setting up the environment

Local development requires that the local environment is set up alongside the
containerized services.

##### Create the virtualenv

```
python3 -m virtualenv env
```

##### Load

```
python3 -m venv .venv
```

##### Activate

```
source .venv/bin/activate
```

Notes:

- `make services` requires [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- `make deps` will install dependencies via pip3 and must be run before `make app`. This can take a few minutes as the PyTorch dependencies are sizable.
