from typing import List

def process_songs(file_path: str):
    print("start: unique_tracks.txt")
    with open(file_path, "r", encoding='utf-8', errors='ignore') as myfile:
        data: List[str] = myfile.readlines()
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
