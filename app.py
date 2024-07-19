from flask import Flask, request, render_template, redirect, url_for
from generateMap import generateMap
import json
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    with open("clients.json", "r") as f:
        clients = json.load(f)

    clients = list(clients.keys())
    default_avg_meeting_time = 60
    default_time_at_main_client = 120
    default_max_driving_time = 10 
    if request.method == "POST":
        client1 = request.form.get("client1")
        client2 = request.form.get("client2")
        avg_meeting_time = int(
            request.form.get("avgMeetingTime", default_avg_meeting_time)
        )
        time_at_main_client = int(
            request.form.get("timeAtMainClient", default_time_at_main_client)
        )
        max_driving_time = int(
            request.form.get("maxDrivingTime", default_max_driving_time)
        )

        if client1 and client2 and client1 != client2:
            generateMap(client1, client2, avg_meeting_time, time_at_main_client, max_driving_time)
            return redirect(url_for("output"))
        else:
            return render_template(
                "index.html",
                clients=clients,
                error="Please select two different clients.",
                avgMeetingTime=default_avg_meeting_time,
                timeAtMainClient=default_time_at_main_client,
                maxDrivingTime=default_max_driving_time,
            )

    return render_template(
        "index.html",
        clients=clients,
        error=None,
        avgMeetingTime=default_avg_meeting_time,
        timeAtMainClient=default_time_at_main_client,
        maxDrivingTime=default_max_driving_time,
    )


@app.route("/output")
def output():
    return render_template("output.html")


if __name__ == "__main__":
    app.run(debug=True)
