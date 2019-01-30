# kotone

## API

### `GET /auth` 
(For admin) save OAuth2 access token to Cloud Datastore

### `GET /api/songs`
List all songs as JSON

### `GET /api/stream/<song_id>`
Get stream URL

### `GET /api/download/<song_id>`
Download song as file

## Deploy

```sh
cd view/
yarn build
cd ../
cp .env.yaml.example .env.yaml
vi .env.yaml  # Put your device id!
gcloud app deploy 
```

## Development (Backend)

```sh
pip install -r requirements.txt
python main.py
```

## Development (Frontend)

```sh
cd view/
yarn start
```
