import time
import requests
import json
import os

def main():
    countries = ["DE", "US"]
    # only US for tv shows because the api doesn't seem to support region for tv shows
    download_show_data("US", "tv")

    time.sleep(5)

    for country in countries:
        download_show_data(country, "movie")
        # add 5 seconds delay to avoid rate limit
        time.sleep(5)
        

def download_show_data(region, type):
    read_key = os.getenv("READ_KEY")
    # TODO
    read_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZmYyMjQyYTJjNGRhNzJlNDkzY2M4ZjFjMWE2ZTQ3YyIsInN1YiI6IjY1OTZjYjE2ODY5ZTc1NmUzYTA2Y2UzZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._U3umEV14xRtn1ua5bkdoPaW1Z9dzZ97g9G9ZQCfEyo"

    all_movies = []
    for i in range(1, 2):
        url = f"https://api.themoviedb.org/3/discover/{type}?include_adult=false&include_video=false&page={i}&sort_by=popularity.desc&region={region}"

        headers = {"Authorization": f"Bearer {read_key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # keep only id, title and popularity
            movies = [{"i": movie["id"], "p": movie["popularity"]} for movie in response.json()["results"]]
            all_movies.extend(movies)
        except Exception as e:
            print(i)
            print(e)

    # write json objects to file
    with open(f"{region}-popular-{type}.json", 'w') as f:
        json.dump(all_movies, f)

if __name__ == "__main__":
    main()