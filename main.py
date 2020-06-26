from flask import Flask, render_template, redirect, url_for, request, session
from twitter_api import Extractor
from model_utility import load_model, load_tokenizer
from fplot import get_barplot, get_piechart, get_wordcloud
from datetime import date
import pickle
from covid_api import get_data


app = Flask(__name__)

app.secret_key = "hello"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        inp = request.form

        result, r_str = ext.get_data(
            date=inp["sdate"], keyword=inp["keyword"], limit=int(inp["max"])
        )
        print(result)

        bar_plot = get_barplot(result)
        pie_plot = get_piechart(result)
        wordcloud = get_wordcloud(r_str, int(inp["wc"]))

        bp = open("bar_plot", "wb")
        pp = open("pie_plot", "wb")
        wc = open("wordcloud", "wb")

        pickle.dump(bar_plot, bp)
        pickle.dump(pie_plot, pp)
        pickle.dump(wordcloud, wc)

        bp.close()
        pp.close()
        wc.close()

        l = [int(i) for i in inp["sdate"].split("-")]
        d = date.today() - date(*l)

        session["days"] = d.days

        return redirect(url_for("dshb"))


@app.route("/cov_ind")
def covind():

    bp = open("bar_plot", "rb")
    pp = open("pie_plot", "rb")
    wc = open("wordcloud", "rb")

    bar_plot = pickle.load(bp)
    pie_plot = pickle.load(pp)
    wordcloud = pickle.load(wc)

    days = session["days"]

    bp.close()
    pp.close()
    wc.close()

    d = get_data()
    d_con = d["NewConfirmed"]
    t_con = d["TotalConfirmed"]
    d_det = d["NewDeaths"]
    t_det = d["TotalDeaths"]
    d_rec = d["NewRecovered"]
    t_rec = d["TotalRecovered"]

    return render_template(
        "covid_india.html",
        days=days,
        wordcloud=wordcloud,
        pie_plot=pie_plot,
        bar_plot=bar_plot,
        d_con=d_con,
        t_con=t_con,
        d_rec=d_rec,
        t_rec=t_rec,
        d_det=d_det,
        t_det=t_det
    )


@app.route("/dshb")
def dshb():

    bp = open("bar_plot", "rb")
    pp = open("pie_plot", "rb")
    wc = open("wordcloud", "rb")

    bar_plot = pickle.load(bp)
    pie_plot = pickle.load(pp)
    wordcloud = pickle.load(wc)

    days = session["days"]

    bp.close()
    pp.close()
    wc.close()

    d = get_data()
    d_con = d["NewConfirmed"]
    t_con = d["TotalConfirmed"]
    d_det = d["NewDeaths"]
    t_det = d["TotalDeaths"]
    d_rec = d["NewRecovered"]
    t_rec = d["TotalRecovered"]

    return render_template(
        "dashboard.html",
        days=days,
        wordcloud=wordcloud,
        pie_plot=pie_plot,
        bar_plot=bar_plot,
        d_con=d_con,
        t_con=t_con,
        d_rec=d_rec,
        t_rec=t_rec,
        d_det=d_det,
        t_det=t_det
    )


@app.route("/twfeed")
def table_page():
    return render_template("feed.html")


@app.route("/maps")
def map_page():
    return render_template("maps.html")


if __name__ == "__main__":

    print("Loading Model..")

    tokenizer = load_tokenizer()
    model = load_model()

    print("Tokenizer and Model loaded.")

    ext = Extractor(model, tokenizer)

    app.run(debug=True)

