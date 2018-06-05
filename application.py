from cs50 import SQL, eprint
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import json
import certifi
import urllib3
http = urllib3.PoolManager(
cert_reqs='CERT_REQUIRED',
ca_certs=certifi.where())

# Repress scary error codes
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()

# Thing to use Harvard Art Museums API
https = urllib3.PoolManager()

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = SQL("sqlite:///project.db")

# Set up some necessary global variables
user_input = "hello"
titles = []
images = []
dateds = []
cultures = []
objectnumbers = []
counter = 1
counter2 = 1

@app.route("/about", methods=["GET", "POST"])
def about():
    """Returns about page"""
    return render_template("about.html")

@app.route("/curateexplore", methods=['GET', 'POST'])
def curateexplore():
    """Returns curate explore page"""
    return render_template("curateexplore.html")

@app.route("/deletetour", methods=["POST"])
def deletetour():
    """Deletes user's tour from database"""
    # Delete tour with the id from the given line in "saved tours"
    tour_id = request.form.get("tourid")
    db.execute("DELETE FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)
    return redirect("/savedtours")

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """Web page index"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", Error="must provide username", login = True)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", Error="must provide password", login = True)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", Error="invalid password", login = True)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/realcurate", methods=["GET","POST"])
def realcurate():
    global titles
    global images
    global dateds
    global cultures
    global objectnumbers
    global user_input
    global counter2

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Set sessiontrue variable to 1 if user is not logged in
        sessiontrue = 0
        if session.get("user_id") is None:
            sessiontrue = 1
        else:
            sessiontrue = 0

        # Create page if request sent from index (i.e. not from user clicking "See more")
        if not 'seeMore' in request.form.values():

        # Check for valid user input
            if not request.form.get("user_input"):
                return render_template("error.html", Error = "Please insert input.")

            createobjectlists(request.form.get("user_input"))

            # Check for valid user input
            if len(titles) < 4:
                return render_template("error.html", Error = "Not enough results returned. Please try new input.")

            user_input = request.form.get("user_input")

            return render_template("tour2.html",
                see_more = True,
                save_tour = True,
                session_true = sessiontrue,
                fourtitles = titles[:4],
                fourimages = images[:4],
                fourdateds = dateds[:4],
                fourcultures = cultures[:4],
                fourobjectnumbers = objectnumbers[:4],
                user_input = user_input)
        else:
            # Increase counter each time the "see more" button is clicked to cycle through images returned
            counter2 += 1
            for j in range(counter2):
                #
                fourtitles = titles[:4]
                fourimages = images[:4]
                fourdateds = dateds[:4]
                fourcultures = cultures[:4]
                fourobjectnumbers = objectnumbers[:4]

                titles = titles[4:] + titles[:4]
                images = images[4:] + images[:4]
                dateds = dateds[4:] + dateds[:4]
                cultures = cultures[4:] + cultures[:4]
                objectnumbers = objectnumbers[4:] + objectnumbers[:4]

            return render_template("tour2.html",
                see_more = True,
                save_tour = True,
                session_true = sessiontrue,
                fourtitles = fourtitles,
                fourimages = fourimages,
                fourdateds = fourdateds,
                fourcultures = fourcultures,
                fourobjectnumbers = fourobjectnumbers,
                user_input = user_input)

    # Redirect user back to index if they reached route via GET (as by clicking a link or refreshing the page)
    else:
        return redirect("/index")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", Error="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", Error="must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return render_template("error.html", Error="must provide password confirmation")

        # Ensure password and confirmation match
        elif (request.form.get("password") != request.form.get("confirmation")):
            return render_template("error.html", Error="password and confirmation do not match")

         # Check that username is unique
        result = db.execute("SELECT * FROM users WHERE username = :username",
                            username=request.form.get("username"))
        if result:
            return render_template("error.html", Error="duplicate username")

        # Store username in database, encrypt and store password, and set session equal to that user's ID
        session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                        username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # After successful registration, redirect to that user's index
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/realcustom", methods=['POST'])
def realcustom():
    global titles
    global images
    global dateds
    global cultures
    global objectnumbers
    global counter
    global user_input

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Store user_input in global variable
        user_input = request.form.get("input")

        # If route accessed via home page, set counter to 0 and set numberadj to "first" for first round of custom tour
        if 'first' in request.form.values():
            counter = 0
            numberadj = "first"
            return render_template("realcustom.html", numberadj = numberadj)

        # Error coding
        if not user_input:
            return render_template("error.html", Error="Please input search query")

        createobjectlists(user_input)

        # Check for valid user input
        if len(images) < 16:
                return render_template("error.html", Error = "Not enough results returned. Please try new input.")

        return render_template("chooseImage.html",
            images = images,
            objectnumbers = objectnumbers,
            user_input = user_input,
            counter = counter)

@app.route("/custom_round", methods=['POST'])
def custom_round():
    global counter

    # Save unique objectnumber of image picked
    objectnumber = request.form.get('objectnumber')

    # For each image picked, save to tempTour database and increase counter
    if counter == 0:
        db.execute("UPDATE tempTour SET tempObject1_number=:objectnumber", objectnumber=objectnumber)
        numberadj = "second"
        counter += 1
        return render_template("realcustom.html", counter = counter, objectnumber = objectnumber, numberadj = numberadj)
    elif counter == 1:
        db.execute("UPDATE tempTour SET tempObject2_number=:objectnumber", objectnumber=objectnumber)
        numberadj = "third"
        counter += 1
        return render_template("realcustom.html", counter=counter, objectnumber=objectnumber, numberadj = numberadj)
    elif counter == 2:
        db.execute("UPDATE tempTour SET tempObject3_number=:objectnumber", objectnumber=objectnumber)
        numberadj = "fourth"
        counter += 1
        return render_template("realcustom.html", counter=counter, objectnumber=objectnumber, numberadj = numberadj)
    else:
        db.execute("UPDATE tempTour SET tempObject4_number=:objectnumber", objectnumber=objectnumber)
        counter = 0
        # After 4 images chosen, redirect to custom_finish to save and display tour
        return custom_finish()

@app.route("/custom_finish", methods=['POST'])
def custom_finish():
    """Save and display custom tour"""

    # Save object numbers from images in custom tour
    customobject1number = db.execute("SELECT tempObject1_number FROM tempTour")[0]['tempObject1_number']
    customobject2number = db.execute("SELECT tempObject2_number FROM tempTour")[0]['tempObject2_number']
    customobject3number = db.execute("SELECT tempObject3_number FROM tempTour")[0]['tempObject3_number']
    customobject4number = db.execute("SELECT tempObject4_number FROM tempTour")[0]['tempObject4_number']

    # Retrieve information from object 1
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': customobject1number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title1 = my_dict['records'][0]['title']
    image1 = my_dict['records'][0]['primaryimageurl']
    dated1 = my_dict['records'][0]['dated']
    culture1 = my_dict['records'][0]['culture']
    #objectid1 = my_dict['records'][0]['objectid']
    objectnumber1 = my_dict['records'][0]['objectnumber']

    # Retrieve information from object 2
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': customobject2number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title2 = my_dict['records'][0]['title']
    image2 = my_dict['records'][0]['primaryimageurl']
    dated2 = my_dict['records'][0]['dated']
    culture2 = my_dict['records'][0]['culture']
    objectnumber2 = my_dict['records'][0]['objectnumber']

    # Retrieve information from object 3
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': customobject3number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title3 = my_dict['records'][0]['title']
    image3 = my_dict['records'][0]['primaryimageurl']
    dated3 = my_dict['records'][0]['dated']
    culture3 = my_dict['records'][0]['culture']
    objectnumber3 = my_dict['records'][0]['objectnumber']

    # Retrieve information from object 4
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': customobject4number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title4 = my_dict['records'][0]['title']
    image4 = my_dict['records'][0]['primaryimageurl']
    dated4 = my_dict['records'][0]['dated']
    culture4 = my_dict['records'][0]['culture']
    objectnumber4 = my_dict['records'][0]['objectnumber']

    # Create arrays with each of the custom objects' information
    customfourtitles = [title1, title2, title3, title4]
    customfourimages = [image1, image2, image3, image4]
    customfourdateds = [dated1, dated2, dated3, dated4]
    customfourcultures = [culture1, culture2, culture3, culture4]
    customfourobjectnumbers = [objectnumber1, objectnumber2, objectnumber3, objectnumber4]


    # Set sessiontrue to 1 if user is not logged in
    sessiontrue = 0
    if session.get("user_id") is None:
        sessiontrue = 1
    else:
        sessiontrue = 0

    return render_template("tour2.html",
            see_more = False,
            save_tour = True,
            session_true = sessiontrue,
            fourtitles = customfourtitles,
            fourimages = customfourimages,
            fourdateds = customfourdateds,
            fourcultures = customfourcultures,
            fourobjectnumbers = customfourobjectnumbers)

@app.route("/savedtours", methods = ['GET','POST'])
@login_required
def savedtours():
    """Display saved tours"""

    #Retrieve and display user's tours from database
    tours = db.execute("SELECT * FROM savedTours WHERE user_id=:user_id", user_id = session["user_id"])
    return render_template("savedtours.html", tours = tours)

@app.route("/savetour", methods=["POST"])
@login_required
def savetour():
    """Save tour"""

    # Remember userinput
    user_input = request.form.get('user_input')

    # Save each object number from tour
    object1_number = request.form.get('object1_number')
    object2_number = request.form.get('object2_number')
    object3_number = request.form.get('object3_number')
    object4_number = request.form.get('object4_number')

    # Retrieve user-inputted tour name
    tourname = request.form.get("tourname")

    # Save session id as variable
    userid = session["user_id"]

    # Store username in database, encrypt and store password, and set session equal to that user's ID
    db.execute("INSERT INTO savedTours (user_input, object1_number, object2_number, object3_number, object4_number, user_id, tour_name)\
                VALUES(:user_input, :object1_number, :object2_number, :object3_number, :object4_number, :user_id, :tourname)",
                user_input=user_input, object1_number=object1_number, object2_number=object2_number,
                object3_number=object3_number, object4_number=object4_number, user_id=userid,
                tourname = tourname)

    return redirect("/savedtours")

@app.route("/remembertour", methods=["POST"])
def remembertour():
    """Display saved tour"""

    # Remember tour_id
    tour_id = request.form.get("tourid")

    # Save object numbers
    rememberobject1number = db.execute("SELECT object1_number FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)[0]['object1_number']
    rememberobject2number = db.execute("SELECT object2_number FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)[0]['object2_number']
    rememberobject3number = db.execute("SELECT object3_number FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)[0]['object3_number']
    rememberobject4number = db.execute("SELECT object4_number FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)[0]['object4_number']
    remembertourname = db.execute("SELECT tour_name FROM savedTours WHERE tour_id = :tour_id", tour_id = tour_id)[0]['tour_name']

    # Retrieve data from first object in tour
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': rememberobject1number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title1 = my_dict['records'][0]['title']
    image1 = my_dict['records'][0]['primaryimageurl']
    dated1 = my_dict['records'][0]['dated']
    culture1 = my_dict['records'][0]['culture']
    objectnumber1 = my_dict['records'][0]['objectnumber']


    # Retrieve data from second object in tour
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': rememberobject2number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title2 = my_dict['records'][0]['title']
    image2 = my_dict['records'][0]['primaryimageurl']
    dated2 = my_dict['records'][0]['dated']
    culture2 = my_dict['records'][0]['culture']
    objectnumber2 = my_dict['records'][0]['objectnumber']

    # Retrieve data from third object in tour
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': rememberobject3number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title3 = my_dict['records'][0]['title']
    image3 = my_dict['records'][0]['primaryimageurl']
    dated3 = my_dict['records'][0]['dated']
    culture3 = my_dict['records'][0]['culture']
    objectnumber3 = my_dict['records'][0]['objectnumber']

    # Retrieve data from fourth object in tour
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'objectnumber': rememberobject4number,
        'fields': 'title,primaryimageurl,dated,culture,people,objectid,objectnumber',
    })

    # Turn JSON into dict
    my_dict = json.loads(r.data)

    title4 = my_dict['records'][0]['title']
    image4 = my_dict['records'][0]['primaryimageurl']
    dated4 = my_dict['records'][0]['dated']
    culture4 = my_dict['records'][0]['culture']
    objectnumber4 = my_dict['records'][0]['objectnumber']

    rememberfourtitles = [title1, title2, title3, title4]
    rememberfourimages = [image1, image2, image3, image4]
    rememberfourdateds = [dated1, dated2, dated3, dated4]
    rememberfourcultures = [culture1, culture2, culture3, culture4]
    rememberfourobjectnumbers = [objectnumber1, objectnumber2, objectnumber3, objectnumber4]

    return render_template("tour2.html",
            see_more = False,
            save_tour = False,
            rememberedtour = True,
            fourtitles = rememberfourtitles,
            fourimages = rememberfourimages,
            fourdateds = rememberfourdateds,
            fourcultures = rememberfourcultures,
            fourobjectnumbers = rememberfourobjectnumbers,
            tourname = remembertourname)

@app.route("/renametour", methods=['POST'])
@login_required
def renametour():
    """Rename Tour"""
    # Retrieve user's input for new name
    rename = request.form.get("rename")
    tour_id = request.form.get("tourid")

    # Update name in database for correct tour
    result = db.execute("UPDATE savedTours SET tour_name = :rename WHERE tour_id = :tour_id", rename=rename, tour_id = tour_id)
    return str(result)


def createobjectlists(user_input):
    """Algorithm for returning list of artwork based on user input"""
    global titles
    global images
    global dateds
    global cultures
    global objectnumbers

    # Create appropriately formatted lists of centuries

    # Get JSON from Harvard Art Museums API with centuries
    r = http.request('GET', 'http://api.harvardartmuseums.org/century',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'size': 100,
        'fields': 'name, temporalorder',
        'sort': 'temporalorder',
    })

    my_century_dict = json.loads(r.data)

    # Make string of centuries classified as Antiquity
    antiquity = []
    for i in range(2,31):
        century = my_century_dict['records'][i]['name']
        antiquity.append(century)

    antiquitystring = "|".join(antiquity)

    # Make string of centuries classified as Postclassical
    postclassical = []
    for i in range(32,42):
        century = my_century_dict['records'][i]['name']
        postclassical.append(century)

    postclassicalstring = "|".join(postclassical)

    # Make list of centuries classified as Modern
    modern = []
    for i in range(42,47):
        century = my_century_dict['records'][i]['name']
        modern.append(century)

    modernstring = "|".join(modern)

    # If user has Time Modifier, set century_api to "any"
    # If user inputs Time Modifier, set century_api according to button clicked

    clickedtime = request.form.get("hiddenTime")

    # Get century_apis

    if (clickedtime == "any"):
        century_api = "any"
    elif (clickedtime == "waywayback"):
        century_api = antiquitystring
    elif (clickedtime == "wayback"):
        century_api = postclassicalstring
    elif (clickedtime == "notsofarback"):
        century_api = modernstring
    else:
        century_api = "any"

    # If user has Color Modifier, set color_api to "any"
    # If user inputs Color Modifier, set color_api according to button clicked

    clickedcolor = request.form.get("hiddenColor")

    if (clickedcolor == "any"):
        color_api = "any"
    elif (clickedcolor == "red"):
        color_api = "Red"
    elif (clickedcolor == "green"):
        color_api = "Green"
    elif (clickedcolor == "yellow"):
        color_api = "Yellow"
    elif (clickedcolor == "black"):
        color_api = "Black"
    elif (clickedcolor == "white"):
        color_api = "White"
    elif (clickedcolor == "grey"):
        color_api = "Grey"
    else:
        color_api = "any"

    # Get JSON from Harvard Art Museums API
    r = http.request('GET', 'http://api.harvardartmuseums.org/object',
    fields = {
        'apikey': 'facf3f90-c430-11e7-bffe-71e657325c21',
        'title': user_input,
        'hasimage': 1,
        'size': 100,
        'fields': 'title,primaryimageurl,culture,objectnumber,dated,totaluniquepageviews,objectid,gallery,colors',
        'sort': 'totaluniquepageviews',
        'sortorder': 'desc',
        'century': century_api,
    })

    my_dict = json.loads(r.data)

    # Figure out Gallery Preference

    clickedgallerypreference = request.form.get("galleryPreference")

    # Separate list creation based on clickedgallerypreference

    titles = []
    images = []
    dateds = []
    cultures = []
    objectnumbers = []
    galleries = []

    # If user prefers objects in gallery, put in-gallery objects first
    if (clickedgallerypreference == "on"):
        # In Gallery
        for i in range(len(my_dict['records'])):
            if 'gallery' in my_dict['records'][i]:
                if 'colors' in my_dict['records'][i]:
                    if color_api == my_dict['records'][i]['colors'][0]['hue']:
                        title = my_dict['records'][i]['title']
                        image = my_dict['records'][i]['primaryimageurl']
                        dated = my_dict['records'][i]['dated']
                        culture = my_dict['records'][i]['culture']
                        objectnumber = my_dict['records'][i]['objectnumber']

                        titles.append(title)
                        images.append(image)
                        dateds.append(dated)
                        cultures.append(culture)
                        objectnumbers.append(objectnumber)

                    if color_api != my_dict['records'][i]['colors'][0]['hue']:
                        title = my_dict['records'][i]['title']
                        image = my_dict['records'][i]['primaryimageurl']
                        dated = my_dict['records'][i]['dated']
                        culture = my_dict['records'][i]['culture']
                        objectnumber = my_dict['records'][i]['objectnumber']

                        titles.append(title)
                        images.append(image)
                        dateds.append(dated)
                        cultures.append(culture)
                        objectnumbers.append(objectnumber)

                if 'colors' not in my_dict['records'][i]:
                    title = my_dict['records'][i]['title']
                    image = my_dict['records'][i]['primaryimageurl']
                    dated = my_dict['records'][i]['dated']
                    culture = my_dict['records'][i]['culture']
                    objectnumber = my_dict['records'][i]['objectnumber']

                    titles.append(title)
                    images.append(image)
                    dateds.append(dated)
                    cultures.append(culture)
                    objectnumbers.append(objectnumber)

        # Not in Gallery
        for i in range(len(my_dict['records'])):
            if 'gallery' not in my_dict['records'][i]:
                if 'colors' in my_dict['records'][i]:
                    if color_api == my_dict['records'][i]['colors'][0]['hue']:
                        title = my_dict['records'][i]['title']
                        image = my_dict['records'][i]['primaryimageurl']
                        dated = my_dict['records'][i]['dated']
                        culture = my_dict['records'][i]['culture']
                        objectnumber = my_dict['records'][i]['objectnumber']

                        titles.append(title)
                        images.append(image)
                        dateds.append(dated)
                        cultures.append(culture)
                        objectnumbers.append(objectnumber)

                    if color_api != my_dict['records'][i]['colors'][0]['hue']:
                        title = my_dict['records'][i]['title']
                        image = my_dict['records'][i]['primaryimageurl']
                        dated = my_dict['records'][i]['dated']
                        culture = my_dict['records'][i]['culture']
                        objectnumber = my_dict['records'][i]['objectnumber']

                        titles.append(title)
                        images.append(image)
                        dateds.append(dated)
                        cultures.append(culture)
                        objectnumbers.append(objectnumber)

                if 'colors' not in my_dict['records'][i]:
                    title = my_dict['records'][i]['title']
                    image = my_dict['records'][i]['primaryimageurl']
                    dated = my_dict['records'][i]['dated']
                    culture = my_dict['records'][i]['culture']
                    objectnumber = my_dict['records'][i]['objectnumber']

                    titles.append(title)
                    images.append(image)
                    dateds.append(dated)
                    cultures.append(culture)
                    objectnumbers.append(objectnumber)

    # If gallery not preferred, just do Gallery Irrelevant
    # Gallery Irrelevant
    else:
        for i in range(len(my_dict['records'])):
            # Preference images that have chosen color as their primary hue, if there is a chosen hue
            if 'colors' in my_dict['records'][i]:
                if color_api == my_dict['records'][i]['colors'][0]['hue']:
                    title = my_dict['records'][i]['title']
                    image = my_dict['records'][i]['primaryimageurl']
                    dated = my_dict['records'][i]['dated']
                    culture = my_dict['records'][i]['culture']
                    #objectid = my_dict['records'][i]['objectid']
                    objectnumber = my_dict['records'][i]['objectnumber']

                    titles.append(title)
                    images.append(image)
                    dateds.append(dated)
                    cultures.append(culture)
                    objectnumbers.append(objectnumber)

                if color_api != my_dict['records'][i]['colors'][0]['hue']:
                    title = my_dict['records'][i]['title']
                    image = my_dict['records'][i]['primaryimageurl']
                    dated = my_dict['records'][i]['dated']
                    culture = my_dict['records'][i]['culture']
                    objectnumber = my_dict['records'][i]['objectnumber']

                    titles.append(title)
                    images.append(image)
                    dateds.append(dated)
                    cultures.append(culture)
                    objectnumbers.append(objectnumber)

            if 'colors' not in my_dict['records'][i]:
                title = my_dict['records'][i]['title']
                image = my_dict['records'][i]['primaryimageurl']
                dated = my_dict['records'][i]['dated']
                culture = my_dict['records'][i]['culture']
                objectnumber = my_dict['records'][i]['objectnumber']

                titles.append(title)
                images.append(image)
                dateds.append(dated)
                cultures.append(culture)
                objectnumbers.append(objectnumber)
