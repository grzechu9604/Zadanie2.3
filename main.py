import datetime
import sqlite3


class PlayInserter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""create table plays (
                    id integer primary key,
                    date_id integer,
                    user_id integer,
                    song_id integer,
                    FOREIGN KEY (date_id) REFERENCES dates(id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (song_id) REFERENCES songs(id));
                  """)
        c.close()

    def insert_play_to_db(self, date_id: int, user_id: int, song_id: int):
        c = self.conn.cursor()
        c.execute("""insert into plays (date_id, user_id, song_id) values (?, ?, ?);""", [date_id, user_id, song_id])
        c.close()


class DateGetter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""create table dates (
                    id integer,
                    day integer,
                    month integer,
                    year integer);
                  """)
        c.close()

    def get_date_id(self, unix_timestamp: int):
        date = datetime.datetime.utcfromtimestamp(unix_timestamp)
        return self.insert_date_to_db(unix_timestamp, date.day, date.month, date.year)

    def insert_date_to_db(self, id: int, day: int, month: int, year: int):
        c = self.conn.cursor()
        c.execute("""insert into dates (id, day, month, year) values (?, ?, ?, ?);""", [id, day, month, year])
        c.close()
        return id


class UserGetter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""create table users (
                    id integer primary key,
                    user_id TEXT);
                  """)
        c.execute("""create unique index users_id_idx on users(user_id);""")
        c.close()

    def get_user_id(self, id: str):
        user_id = self.get_user_id_from_db(id)
        if not user_id:
            user_id = self.insert_user_to_db(id)

        return user_id

    def get_user_id_from_db(self, id: str):
        c = self.conn.cursor()
        c.execute("""select * from users where user_id = ?;""", [id])
        result = c.fetchall()
        c.close()
        if len(result) > 0:
            return result[0][0]

    def insert_user_to_db(self, id: str):
        c = self.conn.cursor()
        c.execute("""insert into users (user_id) values (?);""", [id])
        c.close()

        return c.lastrowid


class User:
    id: int
    name: str

    def __init__(self, id: int, name: str):
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
            artist_id = self.insert_artist_to_db(name)

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

        return c.lastrowid


class SongGetter:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection, create_table: bool):
        self.conn = conn

        if create_table:
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
        c.execute("""select id from songs where song_id = ?;""", [song_id])
        result = c.fetchall()
        c.close()
        if len(result) > 0:
            return result[0][0]

    def insert_song_to_db(self, track_id: str, song_id: str, artist_id: int, title: str):
        c = self.conn.cursor()
        c.execute("""insert into songs (track_id, song_id, artist_id, title) values (?, ?, ?, ?);""",
                  [track_id, song_id, artist_id, title])
        c.close()


class QueryExecutor:
    conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def execute_and_print(self, query: str):
        c = self.conn.cursor()
        c.execute(query)
        result = c.fetchall()
        c.close()
        for line in result:
            print(*line)


def process_unique_tracks(file_path: str, conn: sqlite3.Connection):
    artist_getter = ArtistGetter(conn)
    songs_getter = SongGetter(conn, True)

    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_line = line[0:-1].split("<SEP>")
            songs_getter.insert_song_to_db(split_line[0], split_line[1], artist_getter.get_artist_id(split_line[2]),
                                           split_line[3])
            line = myfile.readline()


def process_triplets(file_path: str, conn: sqlite3.Connection):
    user_getter = UserGetter(conn)
    dates_getter = DateGetter(conn)
    song_getter = SongGetter(conn, False)
    play_inserter = PlayInserter(conn)

    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_line = line[0:-1].split("<SEP>")
            user_id = user_getter.get_user_id(split_line[0])
            date_id = dates_getter.get_date_id(int(split_line[2]))
            song_id = song_getter.get_id(split_line[1])
            play_inserter.insert_play_to_db(date_id, user_id, song_id)
            line = myfile.readline()


def main():
    conn = sqlite3.connect(":memory:")

    unique_tracks_path = "unique_tracks.txt"
    triplets_sample_path = "triplets_sample_20p.txt"

    process_unique_tracks(unique_tracks_path, conn)

    process_triplets(triplets_sample_path, conn)

    queries = [  # zadanie 1:
        """select s.title, (select name from artists a where a.id = s.artist_id), amount from 
(select song_id, count(*) as amount from plays group by song_id order by count(*) desc limit 10) t
join songs s on s.id = t.song_id;"""
        ,
        # zadanie 2:
        """select (select u.user_id from users u where  u.id = t.user_id), t.amount from (select user_id, 
        count(distinct song_id) as amount from plays order by count(distinct song_id) desc limit 10) t; """
        ,
        # zadanie 3:
        """select (select name from artists a where a.id = t.artist_id), t.amount from 
(select artist_id, count(*) as amount from songs s join plays p on s.id = p.song_id group by artist_id order by count(*) desc limit 1) t;"""
        ,
        # zadanie 4:
        """select d.month, count(*) from dates d join plays p on p.date_id = d.id group by d.month order by d.month"""
        ,
        # zadanie 5:
        """select user_id from users where id in (
select user_id from plays where song_id in (
select song_id from plays where song_id in (
select id from songs where artist_id in (select id from artists where name = 'Queen')) group by song_id order by count(*) desc limit 3)) order by user_id limit 10"""]

    executor = QueryExecutor(conn)
    for query in queries:
        executor.execute_and_print(query)


main()
