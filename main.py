import time
from typing import List
import numpy as np
import threading
import datetime


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
    artists: dict
    next_id: int

    def __init__(self):
        self.artists = dict()
        self.next_id = 0

    def get_artist(self, name: str):
        try:
            artist_to_return = self.artists[name]
        except KeyError:
            artist_to_return = None

        if not artist_to_return:
            artist_to_return = Artist(self.next_id, name)
            self.next_id += 1
            self.artists[name] = artist_to_return

        return artist_to_return


class Artist:
    artist_id: int
    name: str

    def __init__(self, artist_id: int, name: str):
        self.artist_id = artist_id
        self.name = name


class SongGetter:
    Songs: dict
    next_id: int

    def __init__(self):
        self.Songs = dict()
        self.next_id = 0

    def get(self, id: str):
        return self.Songs[id]

    def create_song(self, track_id: str, song_id: str, artist: Artist, title: str):
        self.Songs[song_id] = Song(track_id, song_id, artist, title)


class Song:
    track_id: str
    song_id: str
    artist: Artist
    title: str

    def __init__(self, track_id: str, song_id: str, artist: Artist, title: str):
        self.artist = artist
        self.track_id = track_id
        self.song_id = song_id
        self.title = title


class Listening:
    date: MyDate
    user: User
    song: Song

    def __init__(self, date: MyDate, user: User, song: Song):
        self.date = date
        self.user = user
        self.song = song


def process_unique_tracks(file_path: str):
    artist_getter = ArtistGetter()
    songs_getter = SongGetter()

    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_line = line[0:-1].split("<SEP>")
            songs_getter.create_song(split_line[0], split_line[1], artist_getter.get_artist(split_line[2]), split_line[3])
            line = myfile.readline()

    return artist_getter, songs_getter


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
    listenings = process_triplets(triplets_sample_path, songs_getter)
    elapsed_time = time.time() - start_time
    print(elapsed_time)




main()
