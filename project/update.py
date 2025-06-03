import json

def Update(kee, val):
    with open("data/genre_emotion_map", "r+") as file:
        genre_data = json.load(file)
        if kee in genre_data:
            if not isinstance(genre_data[kee], list):
                genre_data[kee] = [genre_data[kee]]
                if not val in genre_data[kee]:
                    genre_data[kee].append(val)
                file.seek(0)
                json.dump(genre_data, file)
                file.truncate()

