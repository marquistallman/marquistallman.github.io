# Portfolio — David Núñez

React + Vite. Datos en `src/data/portfolio.json`. Manager en `portfolio_manager.py`.

## Correr en desarrollo (Docker)

```bash
# primera vez (o al cambiar dependencias)
docker compose up --build

# después
docker compose up
```

Abre http://localhost:5173

## Editar contenido

```bash
python portfolio_manager.py
```

> Las imágenes se guardan automáticamente en `public/img/`. Mueve las imágenes existentes de `img/` a `public/img/` la primera vez.

## GitHub Pages

1. Ve a **Settings → Pages → Source** y elige **GitHub Actions**.
2. Haz push a `main` — el workflow `.github/workflows/deploy.yml` construye y publica solo.

## Build manual

```bash
docker compose run --rm portfolio npm run build
```

El output queda en `dist/`.
