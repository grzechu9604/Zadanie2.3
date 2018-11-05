docker build -t py_sqlite .
docker run --name py_sqlite_container py_sqlite
docker stop py_sqlite_container
docker rm py_sqlite_container

### wybrałęm python i sqlite3 ponieważ są to lekkie i proste w obsłudze technologie

### tabela: Users(id, user_id)
### tabela: Songs(id, track_id, artist_id, title)
### tabela: Play(date_id, user_id, song_id)
### tabela: Artist(id, name)
### tabela: Dates(id, day, month, year) 