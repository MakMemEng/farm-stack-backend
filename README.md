docker compose build

docker compose run --rm \--entrypoint "poetry init \
--name farm-app \
--dependency fastapi \
--dependency uvicorn[standard] \
--dependency fastapi_csrf_protect \
--dependency motor \
--dependency PyJWT \
--dependency passlib \
--dependency python-decouple \
--dependency dnspython \
--dependency gunicorn" \
backend

docker compose run --rm --entrypoint "poetry install --no-root" backend

docker compose build --no-cache
