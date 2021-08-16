# Groover Technical Backend Challenge

## Table of contents

- [Groover Technical Backend Challenge](#groover-technical-backend-challenge)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Development guide](#development-guide)
    - [Configuration](#configuration)
    - [Dependances installation](#dependances-installation)
      - [With Poetry](#with-poetry)
      - [With Pip](#with-pip)
    - [Tests](#tests)
      - [With Poetry](#with-poetry-1)
      - [With Pip](#with-pip-1)
    - [Run server](#run-server)
      - [With Poetry](#with-poetry-2)
      - [With Pip](#with-pip-2)
    - [Test the app](#test-the-app)
  - [Routing](#routing)

## Requirements

- **Python** >= 3.9.*
- **Poetry** >= 1.1.* or **Pip**

## Development guide

### Configuration

Copy the `.env-example` file:

    cp .env-example .env

Then, open the newest `.env` file and modify the keys with your own credentials:
- `SPOTIFY_API_CLIENT_ID`;
- `SPOTIFY_API_CLIENT_SECRET`.

:warning: The `POSTGRES_*` keys doesn't needs to be valued for the development environment.

### Dependances installation

You could use Poetry or Pip depending of your setup.

#### With Poetry

Just run the following command (at the root of the project):

    poetry install

#### With Pip

Run the following command (please replace `python` by the correct alias for the Python 3.9 executable):

    python -m pip install -r requirements.txt -r requirements-dev.txt

Create the virtual environment (same rule for the `python` command):

    python -m venv venv

Activate the virtual environment.

**Powershell**
    
    .\venv\Scripts\Activate.ps1

**Bash**

    source venv/bin/activate

### Tests

#### With Poetry

    poetry run pytest

#### With Pip

Ensure to have the venv activated, then run the following command:

    pytest

### Run server

Run the followind command:

#### With Poetry

    poetry run python manage.py runserver 8000

#### With Pip

Ensure to have the virtual environment activated first.

    python manage.py runserver 8000

### Test the app

Open a lambda browser (except IE, we're not animals) and then enter the following URL: `localhost:8000/api/artists/`.

## Routing

| Method | Resource            | Params     | Role                                                                              |
| ------ | ------------------- | ---------- | --------------------------------------------------------------------------------- |
| GET    | /api/artists/       | None       | Returns all newest artists who recently released albums.                          |
| GET    | /auth/              | None       | Redirect or login to the Spotify Authentication Server..                          |
| GET    | /auth/callback      | code (str) | Get the authentication code for retrieve the token informations and log the user. |
| GET    | /auth/refresh-token | None       | Refresh the `access_token` of the logged user.                                    |