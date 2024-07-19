from flask import Flask, request, render_template, redirect, url_for
from generateMap import generateMap

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    clients = [
        "Lorenzo Bianchi",
        "Giorgia Rinaldi",
        "Federico Colombo",
        "Anna Moretti",
        "Matilde Ferrara",
        "Sergio De Luca",
        "Giulia Neri",
        "Alessandro Fontana",
        "Martina Rossi",
        "Valentina Parisi",
        "Andrea Ricci",
        "Silvia Marino",
        "Alberto Greco",
        "Elisa Barone",
        "Michela De Santis",
        "Dario Marino",
        "Sara Fontana",
        "Riccardo Morelli",
        "Chiara Rizzi",
        "Luca Bianchi",
        "Maria Rossi",
        "Elena Verdi",
        "Paolo Giordano",
        "Sofia De Angelis",
        "Gianni Lombardi",
    ]
    if request.method == "POST":
        client1 = request.form.get("client1")
        client2 = request.form.get("client2")

        if client1 and client2 and client1 != client2:
            generateMap(client1, client2)
            return redirect(url_for("output"))
        else:
            return render_template(
                "index.html",
                clients=clients,
                error="Please select two different clients.",
            )

    return render_template("index.html", clients=clients, error=None)


@app.route("/output")
def output(): 
    return render_template("output.html")


if __name__ == "__main__":
    app.run(debug=True)
