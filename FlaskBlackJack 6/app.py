from flask import Flask, request, render_template, url_for, redirect
import blackjack

app = Flask(__name__, static_url_path="")


@app.route("/")
def get_homepage():
    return app.send_static_file("index.html")


@app.route("/blackjack")
def get_blackjack():
    blackjack.start_hand()
    blackjack.is_winner = False

    return render_template("blackjack.html",
                           hand_results=blackjack.hand_results(),
                           dealer_cards=blackjack.dealer_cards().replace("10", "0").split(", "),
                           player_cards=blackjack.player_cards().replace("10", "0").split(", "),
                           player_balance=blackjack.player_balance,
                           is_winner=blackjack.is_winner
                           )


@app.route("/blackjack/youlost")
def get_refill_page():
    return render_template("youlost.html")


@app.post("/blackjack/youlost")
def post_refill_page():
    cc = request.form.get("creditcard")
    cc_is_valid = blackjack.is_valid_card(cc)
    refill_amount = (request.form.get("refillamount"))
    if not refill_amount.isdigit():
        return render_template("youlost.html",
                               badbalance=True)
    if cc_is_valid:
        blackjack.player_balance = int(refill_amount)
        return render_template("placebet.html",
                               player_balance=blackjack.player_balance)
    else:
        return render_template("youlost.html",
                               badcard=True)


@app.route("/blackjack/bet")
def get_bet_page():
    if blackjack.player_balance <= 0:
        return redirect(url_for('get_refill_page'))
    return render_template("placebet.html",
                           player_balance=blackjack.player_balance)


@app.post("/blackjack/bet")
def post_bet_page():
    bet_amount = request.form.get("placebet")
    if not bet_amount.isdigit():
        return render_template("placebet.html",
                               player_balance=blackjack.player_balance,
                               badbet=True)
    blackjack.bet_amount = int(bet_amount)
    if blackjack.is_valid_bet(blackjack.bet_amount):
        return redirect(url_for('get_blackjack'))
    else:
        return render_template("placebet.html",
                                   player_balance=blackjack.player_balance,
                                   badbet=True)


@app.post("/blackjack")
def post_blackjack():
    submit_button = request.form.get("submitButton")

    if blackjack.is_hand_active():
        if submit_button.upper() == "H":
            blackjack.hit_player()
        else:
            blackjack.play_dealer()

    return render_template("blackjack.html",
                           hand_results=blackjack.hand_results(),
                           dealer_cards=blackjack.dealer_cards().replace("10", "0").split(", "),
                           player_cards=blackjack.player_cards().replace("10", "0").split(", "),
                           player_balance=blackjack.player_balance,
                           is_winner=blackjack.is_winner
                           )


app.run(host="0.0.0.0", debug=True)
