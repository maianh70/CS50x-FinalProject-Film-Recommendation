from flask import Flask, render_template, request, redirect, url_for
import requests
from chosen_plots import RecMa, GenreMatch
from data import Data
from update import Update
#API from tmdb in this file is invalid

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/feeling_tf.html')
def feeling_tf():
    action = request.args.get("action_feel")
    if action:
        message = request.args.get("message")
        if not message:
            return render_template('feeling_tf.html', error="Oh! You have not tell us how you feel")
        genre_matching = GenreMatch(message)
        genre = genre_matching.sim_rate()

        ds = Data("data/film_data_filtered_full(1).csv")
        Id_film = ds.id_return(genre)
        redirect_url = url_for("output", id_film=",".join(Id_film), message=message, genre=genre)


        return redirect(redirect_url)

    return render_template('feeling_tf.html')


@app.route('/film_tf.html')
def film_tf():
    Results = []
    film = request.args.get("film")
    action = request.args.get("action")
    if action == "true":
        if not film or film.strip() == "":
            return render_template("film_tf.html", error="Please enter a movie name!")
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=1c1e245a13390ef1e4f05fafd8d3508d&query={film}")
        movie_data = response.json()

        if movie_data.get("results"):
            for movie in movie_data.get("results"):
                Title = movie.get("title")
                Year = movie.get("release_date")
                Poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
                Check = movie.get("adult")
                Plot = movie.get("overview")

                film_if = {"title": Title, "year": Year, "poster": Poster, "plot": Plot, "check": Check}
                Results.append(film_if)

            return render_template("cf_film.html", results=Results, film=film)
        else:
            return render_template("cf_film.html", results=Results, film=film)

    else:
        return render_template("film_tf.html", error=None)


@app.route('/cf_film.html')
def cf_film():
    return render_template("cf_film.html")


@app.route('/loading.html')
def loading():
    plot = request.args.get("plot")
    return render_template("loading.html", plot=plot)


@app.route('/output')
def output():
    matching_id = []
    plot = request.args.get("plot")
    Message = request.args.get("message")
    id_film = request.args.get("id_film")
    genre = request.args.get("genre")
    Rating = ""

    error = "Sorry, we fail to connect with your Destination"

    if (not plot or "plot" == "N/A") and not id_film:
        return render_template('output.html', error=error)

    elif plot:
        ds = Data("data/mpst_full_data.csv")

        recomm_machine = RecMa(plot)
        s_plots = recomm_machine.satisfied_plot()  # plots in dataset that match
        if len(s_plots) == 0:
            return render_template('output.html', error=error)

        matching_id = ds.matching(s_plots)  # get back a list of id corresponds to the satisfied plots

    elif id_film:
        Rating = "How well did this match your mood?"
        matching_id = id_film.split(",")

    if not matching_id:
        return render_template('output.html', error=error)



    Outputs = []
    for id in matching_id:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}?api_key=1c1e245a13390ef1e4f05fafd8d3508d")
        movie_data = response.json()
        Title = movie_data.get("title")
        Year = movie_data.get("release_date")
        Poster = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
        Id = movie_data.get("imdb_id")
        Check = movie_data.get("adult")
        film_out = {"title": Title, "year": Year, "poster": Poster, "id": Id, "check": Check}
        Outputs.append(film_out)
    if len(Outputs) == 0:
        return render_template("output.html", error=error)
    if Rating and id_film:
        return render_template("output.html", outputs=Outputs, rating=Rating, message=Message, error=None, genre=genre)
    else:
        return render_template("output.html", outputs=Outputs, error=None)

@app.route("/submit_rating", methods=['POST'])
def submit_rating():

    data = request.get_json()


    rating = data.get("rating")
    val = data.get("message")
    if rating == "great":
        kee = data.get("genre")
    else:
        kee = data.get("new_genre")
    print(val)
    print(kee)
    if kee:
        Update(kee, val)

    return "", 204
