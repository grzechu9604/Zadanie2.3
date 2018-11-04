from typing import List
import numpy as np
import threading


def create_artists_dict(split_lines: List[List[str]]):
    distinc_artists = enumerate(set([line[3] for line in split_lines]))
    return dict(distinc_artists)


def process_songs(file_path: str):
    print("start: unique_tracks.txt")
    split_lines = []
    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        line = myfile.readline()
        while line:
            split_lines.append(line[0:-1].split("<SEP>"))
            line = myfile.readline()

    artist_dict = create_artists_dict(split_lines)
    print("unique_tracks.txt")


def process_triplets(file_path: str):
    print("start: triplets_sample_20p.txt")
    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        data: List[str] = myfile.readlines()
        print(data[0])
    print("triplets_sample_20p.txt")


def main():
    # process_triplets("triplets_sample_20p.txt")
    process_songs("unique_tracks.txt")


main()
