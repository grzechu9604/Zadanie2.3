docker build -t py_sqlite .
docker run --name py_sqlite_container py_sqlite
docker stop py_sqlite_container
docker rm py_sqlite_container

### wybrałem python i sqlite3, ponieważ są to lekkie i proste w obsłudze technologie

### tabela: Users(id, user_id) - id sztuczny klucz, user_id - id użytkownika z pliku triplets
### tabela: Songs(id, track_id, song_id, artist_id, title) - id klucz sztuczny, track_id, title oraz song_id pochodzą z pliku unique_tracks.txt, artist_id - klucz obcy do tabeli artists
### tabela: Play(date_id, user_id, song_id) - date_id klucz obcy z tabeli dates, user_id klucz obcy z tabeli users, song_id - klucz obcy z tabeli songs
### tabela: Artist(id, name) - id klucz sztuczny, name pochodzi z pliku unique_tracks.txt
### tabela: Dates(id, day, month, year) - id to unixtimestamp z pliku triplets_sample_20p.txt, pozostałe kolumny to odpowiednie właściwości tej daty