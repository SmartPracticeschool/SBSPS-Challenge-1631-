from flask import Flask, render_template, redirect, url_for, request, session
from twitter_api import Extractor
from model_utility import load_model, load_tokenizer
from fplot import get_barplot, get_piechart, get_wordcloud
from datetime import date
import pickle
from covid_api_v2 import get_data
from state_info import get_state_data
from bisect import bisect


app = Flask(__name__)

app.secret_key = "hello"


@app.route("/")
def main():
    return redirect(url_for("index"))

@app.route("/index")
def index():
    session['stage'] = 0
    session['pass'] = 1
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    if 'pass' in session:
        if  session['pass'] == 1 or session['pass'] == 2:
            session['pass'] = 2
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

    if request.method == "POST":
        inp = request.form

        kw = inp['keyword']

        if inp['keyword'] == '':
            kw = "covid AND india" + ' -filter:retweets'

        session['stage'] = 1

        print('Keyword :',kw, 'Max no. of Tweets :', inp['max'])

        result, r_str, tw_list = ext.get_data(
            date=inp["sdate"], keyword=kw, limit=int(inp["max"])
        )
        print(result)

        session['stage'] = 2

        bar_plot = get_barplot(result)
        pie_plot = get_piechart(result)
        wordcloud = get_wordcloud(r_str, int(inp["wc"]))

        bp = open("tmp/bar_plot", "wb")
        pp = open("tmp/pie_plot", "wb")
        wc = open("tmp/wordcloud", "wb")
        tl = open("tmp/tweet_list", "wb")

        pickle.dump(bar_plot, bp)
        pickle.dump(pie_plot, pp)
        pickle.dump(wordcloud, wc)
        pickle.dump(tw_list, tl)

        bp.close()
        pp.close()
        wc.close()
        tl.close()

        l = [int(i) for i in inp["sdate"].split("-")]
        d = date.today() - date(*l)

        session["days"] = d.days

        return redirect(url_for("dshb"))



@app.route("/dshb")
def dshb():
    if 'pass' in session:
        if  session['pass'] == 2 or session['pass'] == 3:
            session['pass'] = 3
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

    
    bp = open("tmp/bar_plot", "rb")
    pp = open("tmp/pie_plot", "rb")
    wc = open("tmp/wordcloud", "rb")
    

    bar_plot = pickle.load(bp)
    pie_plot = pickle.load(pp)
    wordcloud = pickle.load(wc)
    

    days = session["days"]

    bp.close()
    pp.close()
    wc.close()


    d = get_data()
    d_con = d["NewConfirmed"]
    t_con = d["Confirmed"]
    d_det = d["NewDeaths"]
    t_det = d["Deaths"]
    d_rec = d["NewRecovered"]
    t_rec = d["Recovered"]
    
    actv = d['Active']
    upd = d['Last_Update']


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
        t_det=t_det,
        actv=actv,
        upd=upd
    )


@app.route("/twfeed")
def table_page():

    return render_template("feed.html")


@app.route("/tweets")
def tweets():
    tl = open("tmp/tweet_list", "rb")

    tw_list = pickle.load(tl)

    tl.close()

    return render_template("tweets.html", tw_list=tw_list)



@app.route("/maps")
def map_page():
    pos = open('state_loc', 'rb')
    loc = pickle.load(pos)
    data = get_state_data()
    rmap = [0, 6.5, 12, 18, 23, 28, 34, 40, 45.5, 60, 70]
    ranges = [5, 501, 1001, 3001, 5001, 10001, 25001, 50001, 100001, 250001]

    pos.close()
    return render_template("maps.html", loc=loc, data=data, rmap=rmap, ranges=ranges, bisect=bisect)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":

    print("Loading Model..")

    tokenizer = load_tokenizer()
    model = load_model()

    print("Tokenizer and Model loaded.")

    ext = Extractor(model, tokenizer)

    app.run(debug=False)

