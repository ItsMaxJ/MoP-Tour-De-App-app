**[Čeština](#čeština)** · **[English](#english)**

# Čeština

## Začínáme

Tato složka obsahuje tři části:

- `frontend/`: webová aplikace.
- `backend/`: API.
- `caddy/`: reverzní proxy pro produkci (Tour de Cloud). Lokální vývoj ji nepoužívá.

Spuštění všeho lokálně:

```bash
docker compose up
```

Frontend běží na `http://localhost:3000`, API na `http://localhost:3001/api`. Porty 3000, 3001 a 3306 (MySQL) musí být před spuštěním volné. V Docker Desktopu pro macOS nebo Windows nejdřív zapněte host networking (Settings → Resources → Network → "Enable host networking"); Linux a OrbStack to podporují bez nastavování.

## Nasazení

Push do větve `main` spustí `.github/workflows/deploy.yml`, který nahraje projekt na Tour de Cloud. Před prvním pushem:

1. Přidejte repository secret `TDC_TOKEN` (Settings → Secrets and variables → Actions) s vaším Tour de Cloud tokenem.
2. Otevřete `tourdeapp.yaml` a nahraďte `<slug>` slugem vašeho projektu, ve všech čtyřech řádcích `image:`.

Pak pushněte do `main`.

## Frontend: čistý JavaScript

Žádný framework, žádný build nástroj, žádné závislosti. `index.html` načítá `src/*.js` přímo jako moduly prohlížeče.

Kód je v `frontend/src/`:

- `api.js`: komunikace s backendem (`getProducts`, `createProduct`, `updateProduct`, `deleteProduct`).
- `App.js`: drží stav seznamu produktů a propojuje formulář s tabulkou.
- `ProductForm.js`: formulář pro přidání a úpravu.
- `ProductTable.js`: vykresluje seznam produktů.
- `index.css`: styly.

`docker compose up` soubory jen servíruje beze změny. Není tu žádný build krok ani live reload: po úpravě souboru je potřeba stránku v prohlížeči ručně obnovit.

Spuštění mimo Docker: otevřete `index.html` přímo v prohlížeči, nebo složku servírujte libovolným statickým serverem. V obou případech volá backend na `http://localhost:3001/api` (napevno v `api.js`).

## Backend: Python Flask

API ve Flasku s Flask-SQLAlchemy a MySQL (přes `pymysql`).

Kód je v `backend/app/`:

- `routes.py`: endpointy (registrované jako blueprint `product_bp`).
- `models.py`: SQLAlchemy model `Product`.
- `extensions.py`: sdílená instance `db` (`SQLAlchemy`).
- `config.py`: nastavení připojení k databázi, čtené z prostředí.
- `__init__.py`: tovární funkce `create_app`, kde se zapojí blueprint a CORS.

`docker compose up` spustí `flask run --debug`, který se restartuje po každé změně: úprava souboru v `app/` se projeví v dalším požadavku.

Spuštění mimo Docker: nejdřív spusťte MySQL příkazem `docker compose up -d mysql`, pak `pip install -r requirements.txt` a `flask --app run:app run --debug --port 3001`. API poslouchá na `http://localhost:3001/api/product`.

# English

## Getting started

This folder has three parts:

- `frontend/`: the web app.
- `backend/`: the API.
- `caddy/`: the reverse proxy used in production (Tour de Cloud). Local development skips it.

Run everything locally:

```bash
docker compose up
```

The frontend is at `http://localhost:3000`, the API at `http://localhost:3001/api`. Ports 3000, 3001 and 3306 (MySQL) must be free before you start. On Docker Desktop for macOS or Windows, turn on host networking first (Settings → Resources → Network → "Enable host networking"); Linux and OrbStack support it by default.

## Deploying

Pushing to `main` runs `.github/workflows/deploy.yml`, which uploads the project to Tour de Cloud. Before the first push:

1. Add a repository secret named `TDC_TOKEN` (Settings → Secrets and variables → Actions) with your Tour de Cloud token.
2. Open `tourdeapp.yaml` and replace `<slug>` with your project's slug in all four `image:` lines.

Then push to `main`.

## Frontend: pure JavaScript

No framework, no build tool, no dependencies. `index.html` loads `src/*.js` directly as browser modules.

Code lives in `frontend/src/`:

- `api.js`: talks to the backend (`getProducts`, `createProduct`, `updateProduct`, `deleteProduct`).
- `App.js`: holds the product list state and wires the form and table together.
- `ProductForm.js`: the add/edit form.
- `ProductTable.js`: renders the product list.
- `index.css`: styling.

`docker compose up` serves these files as-is. There is no build step and no live reload: after editing a file, reload the page in the browser to see the change.

To run it outside Docker, open `index.html` directly in a browser, or serve the folder with any static file server. Either way it calls the backend at `http://localhost:3001/api` (hardcoded in `api.js`).

## Backend: Python Flask

A Flask API with Flask-SQLAlchemy and MySQL (via `pymysql`).

Code lives in `backend/app/`:

- `routes.py`: the endpoints (registered as the `product_bp` blueprint).
- `models.py`: the SQLAlchemy `Product` model.
- `extensions.py`: the shared `db` (`SQLAlchemy`) instance.
- `config.py`: database connection settings, read from the environment.
- `__init__.py`: the app factory (`create_app`), where the blueprint and CORS are wired up.

`docker compose up` runs `flask run --debug`, which restarts on every change: edit any file under `app/` and the next request picks it up.

To run it outside Docker: start MySQL with `docker compose up -d mysql`, then `pip install -r requirements.txt` and `flask --app run:app run --debug --port 3001`. The API listens on `http://localhost:3001/api/product`.
