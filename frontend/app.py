import requests
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


# The Username & Password of the currently logged-in User, this is used as a pseudo-cookie, as such this is not session-specific.
username = None
password = None

session_data = dict()


def save_to_session(key, value):
    session_data[key] = value


def load_from_session(key):
    return (
        session_data.pop(key) if key in session_data else None
    )  # Pop to ensure that it is only used once


def succesful_request(r):
    return r.status_code == 200


@app.route("/")
def home():
    global username

    if username is None:
        return render_template("login.html", username=username, password=password)
    else:
        # ================================
        # FEATURE (list of public events)
        #
        # Retrieve the list of all public events. The webpage expects a list of (title, date, organizer) tuples.
        # Try to keep in mind failure of the underlying microservice
        # =================================

        events = []
        response = requests.get("http://events:8000/events")
        if response.status_code == 200:
            public_events = response.json()
            for event in public_events["events"]:
                events.append((event["title"], event["date"], event["organizer"]))
        return render_template(
            "home.html", username=username, password=password, events=events
        )


@app.route("/event", methods=["POST"])
def create_event():
    title, description, date, publicprivate, invites = (
        request.form["title"],
        request.form["description"],
        request.form["date"],
        request.form["publicprivate"],
        request.form["invites"],
    )
    # ==========================
    # FEATURE (create an event)
    #
    # Given some data, create an event and send out the invites.
    # ==========================
    publicprivate = request.form["publicprivate"] == "public"

    response = requests.post(
        "http://events:8000/events/create",
        json={
            "title": title,
            "description": description,
            "date": date,
            "public": publicprivate,
            "organizer": username,
        },
    )
    if response.status_code == 200:
        event_response = response.json()
        event_id = event_response["Event"]["id"]
        requests.post(
            "http://engagement:8000/engagement",
            json={"user": username, "event_id": event_id, "invite_status": "pending"},
        )
        for invitee in invites.split(";"):
            user_response = requests.get("http://auth:8000/users/" + invitee)
            if user_response.status_code == 200:
                requests.post(
                    "http://engagement:8000/engagement",
                    json={
                        "user": invitee,
                        "event_id": event_id,
                        "invite_status": "pending",
                    },
                )
    return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    calendar_user = (
        request.form["calendar_user"] if "calendar_user" in request.form else username
    )

    # ================================
    # FEATURE (calendar based on username)
    #
    # Retrieve the calendar of a certain user. The webpage expects a list of (id, title, date, organizer, status, Public/Private) tuples.
    # Try to keep in mind failure of the underlying microservice
    # =================================

    success = (
        True  
    )
    calendar = []
    allowed = False
    calendar_response = requests.get(
        "http://calendar:8000/calendar/" + str(username)
    )
    if calendar_user == username:
        allowed = True
        success = True
    elif calendar_response.status_code == 200:
        calendar = calendar_response.json()
        # check if the calendar is shared with you
        for calendar_entry in calendar:
            if calendar_entry["user2"] == username:
                allowed = True
                
    engagements_response = requests.get(
        "http://engagement:8000/engagement/" + str(calendar_user)
    )
    if engagements_response.status_code == 200 and allowed:
        engagements = engagements_response.json()
        for engagement in engagements:
            event_response = requests.get(
                "http://events:8000/events/" + str(engagement["event_id"])
            )
            if event_response.status_code == 200:
                success = True
                event = event_response.json()
                calendar.append(
                    (
                        event["event"]["id"],
                        event["event"]["title"],
                        event["event"]["date"],
                        event["event"]["organizer"],
                        engagement["invite_status"],
                        "Public" if event["event"]["public"] else "Private",
                    )
                    if engagement["invite_status"] != "pending"
                    else None
                )

    return render_template(
        "calendar.html",
        username=username,
        password=password,
        calendar_user=calendar_user,
        calendar=calendar,
        success=success,
    )


@app.route("/share", methods=["GET"])
def share_page():
    return render_template(
        "share.html", username=username, password=password, success=None
    )


@app.route("/share", methods=["POST"])
def share():
    share_user = request.form["username"]

    # ========================================
    # FEATURE (share a calendar with a user)
    #
    # Share your calendar with a certain user. Return success = true / false depending on whether the sharing is succesful.
    # ========================================
    user_response = requests.get("http://auth:8000/users/" + share_user)
    if user_response.status_code == 200:
        response = requests.post(
            "http://calendar:8000/calendar",
            json={"owner": username, "receiver": share_user},
        )
        if response.status_code == 200:
            success = True
        else:
            success = False
    else:
        success = False
    success = True

    return render_template(
        "share.html", username=username, password=password, success=success
    )


@app.route("/event/<eventid>")
def view_event(eventid):

    # ================================
    # FEATURE (event details)
    #
    # Retrieve additional information for a certain event parameterized by an id. The webpage expects a (title, date, organizer, status, (invitee, participating)) tuples.
    # Try to keep in mind failure of the underlying microservice
    # =================================

    response = requests.get("http://events:8000/events/" + eventid)
    particpants = []
    if response.status_code == 200:
        event = response.json()
        # get all the engagements
        engagements_response = requests.get( "http://engagement:8000/engagement/")
        engagements = engagements_response.json()
        for engagement in engagements:
            if engagement["event_id"] == int(eventid):
                particpants.append((engagement["user"], engagement["invite_status"]))
        event = (
            event["event"]["title"],
            event["event"]["date"],
            event["event"]["organizer"],
            "Public" if event["event"]["public"] else "Private",
            particpants,
        )
        success = True
    else:
        event = None  
        success = False
    

    # success = True  # TODO: this might change depending on whether you can see the event (public, or private but invited)

    # if success:
    #     event = [
    #         "Test event",
    #         "Tomorrow",
    #         "Benjamin",
    #         "Public",
    #         [["Benjamin", "Participating"], ["Fabian", "Maybe Participating"]],
    #     ]  # TODO: populate this with details from the actual event
    # else:
    #     event = None  # No success, so don't fetch the data

    return render_template(
        "event.html", username=username, password=password, event=event, success=success
    )


@app.route("/login", methods=["POST"])
def login():
    req_username, req_password = request.form["username"], request.form["password"]

    # ================================
    # FEATURE (login)
    #
    # send the username and password to the microservice
    # microservice returns True if correct combination, False if otherwise.
    # Also pay attention to the status code returned by the microservice.
    # ================================
    success = False
    response = requests.post(
        "http://auth:8000/auth/login",
        json={"username": req_username, "password": req_password},
    )
    if response.status_code == 200:
        response_json = response.json()
        if response_json["message"] == "Login successful":
            success = True
    else:
        success = False

    save_to_session("success", success)
    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect("/")


@app.route("/register", methods=["POST"])
def register():

    req_username, req_password = request.form["username"], request.form["password"]

    # ================================
    # FEATURE (register)
    #
    # send the username and password to the microservice
    # microservice returns True if registration is succesful, False if otherwise.
    #
    # Registration is successful if a user with the same username doesn't exist yet.
    # ================================

    response = requests.post(
        "http://auth:8000/auth/register",
        json={"username": req_username, "password": req_password},
    )
    if response.status_code == 200:
        success = True
    else:
        success = False

    # success = True  # TODO: call
    save_to_session("success", success)

    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect("/")


@app.route("/invites", methods=["GET"])
def invites():
    # ==============================
    # FEATURE (list invites)
    #
    # retrieve a list with all events you are invited to and have not yet responded to
    # ==============================

    # my_invites = [(1, "Test event", "Tomorrow", "Benjamin", "Private")]  # TODO: process
    my_invites = []
    response = requests.get("http://engagement:8000/engagement/" + username)
    if response.status_code == 200:
        engagements = response.json()
        for engagement in engagements:
            event_response = requests.get(
                "http://events:8000/events/" + str(engagement["event_id"])
            )
            if event_response.status_code == 200:
                event = event_response.json()
                if engagement["invite_status"] == "pending":
                    my_invites.append(
                        (
                            event["event"]["id"],
                            event["event"]["title"],
                            event["event"]["date"],
                            event["event"]["organizer"],
                            "Private" if not event["event"]["public"] else "Public",
                        )
                    )
    
    return render_template(
        "invites.html", username=username, password=password, invites=my_invites
    )


@app.route("/invites", methods=["POST"])
def process_invite():
    eventId, status = request.json["event"], request.json["status"]

    # =======================
    # FEATURE (process invite)
    #
    # process an invite (accept, maybe, don't accept)
    # =======================
    real_status = 'pending'
    if status == "Participate":
        real_status = "accepted"
    elif status == "Maybe Participate":
        real_status = "maybe"
    elif status == "Don't Participate":
        real_status = "rejected"
    response = requests.put(
        "http://engagement:8000/engagement",
        json={"user": username, "event_id": eventId, "invite_status": real_status},
    )
    if response.status_code != 200:
        raise Exception("Could not process invite")

    return redirect("/invites")


@app.route("/logout")
def logout():
    global username, password

    username = None
    password = None
    return redirect("/")
