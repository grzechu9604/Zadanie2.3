import time
from typing import List
import numpy as np
import threading
import datetime
import sqlite3


class MyDate:
    id: int
    year: int
    month: int
    day: int

    def __init__(self, id: int):
        date = datetime.datetime.utcfromtimestamp(id)
        self.year = date.year
        self.month = date.month
        self.day = date.day


class UserGetter:
    users: dict
    next_id: int

    def __init__(self):
        self.users = dict()
        self.next_id = 0

    def get_user(self, name: str):
        try:
            user_to_return = self.users[name]
        except KeyError:
            user_to_return = None

        if not user_to_return:
            user_to_return = User(self.next_id, name)
            self.next_id += 1
            self.users[name] = user_to_return

        return user_to_return


class User:
    id: int
    name: str

    def __init__(self, id: int, name:str):
        self.id = id
        self.name = name


class ArtistGetter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""create table artists (
                    id integer primary key,
                    name TEXT);
                  """)
        c.execute("""create unique index artist_name_idx on artists(name);""")
        c.close()

    def get_artist_id(self, name: str):
        artist_id = self.get_artist_id_from_db(name)
        if not artist_id:
            self.insert_artist_to_db(name)
            artist_id = self.get_artist_id_from_db(name)

        return artist_id

    def get_artist_id_from_db(self, name: str):
        c = self.conn.cursor()
        c.execute("""select * from artists where name = ?;""", [name])
        result = c.fetchall()
        c.close()
        if len(result) > 0:
            return result[0][0]

    def insert_artist_to_db(self, name: str):
        c = self.conn.cursor()
        c.execute("""insert into artists (name) values (?);""", [name])
        c.close()


class SongGetter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""create table songs (
                    id integer primary key,
                    track_id text,
                    song_id text,
                    artist_id int,
                    title text,
                    FOREIGN KEY (artist_id) REFERENCES artists(id));
                  """)
        c.execute("""create index song_id_idx on songs(song_id);""")
        c.close()

    def get_id(self, song_id: str):
        c = self.conn.cursor()
        c.execute("""select (id, track_id, song_id, artist_id, title) from songs where song_id = ?;""", [song_id])
        result = c.fetchall()
        c.close()
        if len(result) > 0:
            return result[0][0]

    def insert_song_to_db(self, track_id: str, song_id: str, artist_id: int, title: str):
        c = self.conn.cursor()
        c.execute("""insert into songs (track_id, song_id, artist_id, title) values (?, ?, ?, ?);""",
                  [track_id, song_id, artist_id, title])
        c.close()


def process_unique_tracks(file_path: str):
    conn = sqlite3.connect(":memory:")
    artist_getter = ArtistGetter(conn)
    songs_getter = SongGetter(conn)

    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_line = line[0:-1].split("<SEP>")
            songs_getter.insert_song_to_db(split_line[0], split_line[1], artist_getter.get_artist_id(split_line[2]), split_line[3])
            line = myfile.readline()

    return artist_getter, songs_getter

'''
def process_triplets(file_path: str, song_getter: SongGetter):
    listenings: List[Listening] = []
    user_getter = UserGetter()

    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_line = line[0:-1].split("<SEP>")
            listenings.append(Listening(MyDate(int(split_line[2])), user_getter.get_user(split_line[0]),
                              song_getter.get(split_line[1])))
            line = myfile.readline()

    return listenings
'''

def main():
    conn = sqlite3.connect(":memory:")

    unique_tracks_path = "unique_tracks.txt"
    triplets_sample_path = "triplets_sample_20p.txt"

    start_time = time.time()
    print("start: process_unique_tracks")
    artist_getter, songs_getter = process_unique_tracks(unique_tracks_path)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("start: process_triplets")
    #listenings = process_triplets(triplets_sample_path, songs_getter)
    elapsed_time = time.time() - start_time
    print(elapsed_time)




main()
