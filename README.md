# starzz-flask

This is a REST API backend created using Python's Flask framework.

### The Dataset

This project uses a database of fictional galaxies, constellations and stars.  

Here is a diagram to describe the tables and their relationships:

<img src="assets/schema.png" width="500" height="200"/>

Stars are located in constellations, which are in turn located in galaxies.

The `galaxies`, `constellations` and `stars` tables contain the additional
fields `added_by` and `verified_by` to indicate the id of the users who made
the finding and verified it, respectively.

The database was created using SQLite.  The scripts to create the tables and
load the dummy data are included in `assets` for reference.  Note that the primary
keys of each table should actually increment automatically but are simply defined
as `INTEGER` and `PRIMARY KEY`, like so:

    CREATE TABLE users (
        user_id INTEGER,
        ...
        PRIMARY KEY (user_id)
    );
    
    CREATE TABLE galaxies (
        galaxy_id INTEGER,
        ...
        PRIMARY KEY (galaxy_id),
        ...
    );
    
    CREATE TABLE constellations (
        constellation_id INTEGER,
        ...
        PRIMARY KEY (constellation_id),
        ...
    );
    
    CREATE TABLE stars (
        star_id INTEGER,
        ...
        PRIMARY KEY (star_id),
        ...
    );

because in SQLite, if a column is defined as `INTEGER` 
and `PRIMARY KEY`, there is no need to 
define it as `AUTO_INCREMENT`.

### The Application

All code committed at each chapter is available with the commit message of the chapter name.

#### Chapter 1: Setting up the routes

Python libraries added:

    flask
    flask-restful

We set up the project structure as follows:

    app.py           -> the main module for the application
    requirements.txt -> a list of required libraries
    README.md        -> project's README
    |_ assets        -> directory containing the project's assets
    |_ controllers   -> modules to handle application logic
    |_ resources     -> modules to handle application requests

The module `app.py` contains code to dispatch the requests to the application, to the classes 
in `resources`:

    ...
    from resources import constellations, galaxies, stars, users
    
    
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(constellations.ConstellationRegisterOrList, "/constellations")
    api.add_resource(constellations.Constellation, "/constellations/<int:constellation_id>")
    api.add_resource(galaxies.GalaxyRegisterOrList, "/galaxies")
    api.add_resource(galaxies.Galaxy, "/galaxies/<int:galaxy_id>")
    api.add_resource(stars.StarRegisterOrList, "/stars")
    api.add_resource(stars.Star, "/stars/<int:star_id>")
    api.add_resource(users.UserRegisterOrList, "/users")
    api.add_resource(users.User, "/users/<int:user_id>")
    ...

A sample module in the `resources` package is `users.py`.  It contains the classes to 
handle the requests to the `/users` endpoints:

    ...
    from controllers import users
    
    
    class UserRegisterOrList(Resource):
        """Resource to handle requests to register new, or list existing, users."""
    
        def post(self) -> tuple[dict[str, str], int]:
            """Handle POST method."""
            return users.handle_post(request.json)
    
        def get(self) -> tuple[dict[str, str], int]:
            """Handle GET method."""
            return users.handle_list()
    
    
    class User(Resource):
        """Resource to handle requests to view, update and delete existing users."""
    
        def get(self, user_id: int) -> tuple[dict[str, str], int]:
            """Handle GET method."""
            return users.handle_get(user_id)
    ...

The different requests are then forwarded to different functions in `users.py` in the `controllers` package.

    ...
    def handle_post(r_json: dict[str, str]) -> tuple[dict[str, str], int]:
        """Handle the POST request."""
        return {
            "input": r_json,
            "message": "User successfully registered."
        }, HTTPStatus.CREATED
    
    
    def handle_get(user_id: int) -> tuple[dict[str, str], int]:
        """Handle the GET request."""
        return {
            "input": user_id,
            "message": "User successfully retrieved."
        }, HTTPStatus.OK
    
    ...

The other modules in the `resources` package follow a similar logic.

#### Chapter 2: Setting up the database

Python libraries added:

    flask-sqlalchemy

We include the package `models` to our project.  We also refactor `app.py` by introducing 
a new module `config.py` and moving the application's configuration to it:

    app.py            
    config.py        -> module containing application configuation 
    requirements.txt
    README.md        
    |_ assets
    |- deps          -> package to contain application dependencies
    |_ controllers   
    |_ resources     
    |_ models        -> modules for classes to be used for interacting with the database

`config.py` now has application configuration previously written to `app.py`.  It also
contains database configuration information.

    ...
    basedir = pathlib.Path(__file__).parent.resolve()
    app = Flask(__name__)
    
    # specify the location of the database file
    app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLITE_URI.format(basedir)
    # turns the SQLAlchemy event system off
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db = SQLAlchemy(app)

The database is saved as `deps/db.sqlite3`.

The modules in the `models` package define ORM classes that map to database tables.  
An example module is `constellations.py`.  The module defines the `Constellation` class
to directly map to the `constellations` table, and the class' attributes corresponds to
the table's columns (the appropriate attributes are also set as primary/foreign keys):

    ...
    class Constellation(db.Model):
        """Model for Constellation objects."""
        __tablename__ = "constellations"
    
        constellation_id = db.Column(db.Integer, primary_key=True)
        constellation_name = db.Column(db.String)
        galaxy_id = db.Column(db.Integer, db.ForeignKey("galaxies.galaxy_id"))
        added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
        verified_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    ...

The class also defines relationships with other classes:

    ...
        galaxy_info = relationship("Galaxy")
        added_info = relationship("User", foreign_keys=[added_by])
        verified_info = relationship("User", foreign_keys=[verified_by])
    ...

Since the last two relationships refer to `User`, we need to explicitly indicate, which relationship
uses which foreign key, to remove any ambiguity.

We then define the methods.  Since our APIs cannot directly respond with Python objects, we need
to serialize them; only then can they be used as API responses.  To serialize `Constellation`
objects, we define methods to return the JSON representation of the object:

    ...
        def to_partial_json(self) -> dict[str, str | int]:
            """Return a partial JSON representation of this object."""
            return {
                "constellation_id": self.constellation_id,
                "constellation_name": self.constellation_name
            }
    
        def to_full_json(self) -> dict[str, str | int | dict[str, str | int]]:
            """Return a full JSON representation of this object."""
            obj = self.galaxy_info
            galaxy = obj.to_partial_json() if obj else {}
            obj = self.constellation_added_info
            added_by = obj.to_partial_json() if obj else {}
            obj = self.constellation_verified_info
            verified_by = obj.to_partial_json() if obj else {}
    
            return {
                **self.to_partial_json(),
                "galaxy": galaxy,
                "added_by": added_by,
                "verified_by": verified_by
            }
    ...

In the `to_full_json()` method, since the 3 relationships that were previously defined return
objects of other classes, we also need to serialize each of those objects.

The CRUD and list methods are defined as `@classmethod` so they can be directly called on the
`Constellation` class (i.e. class instantiation is not necessary).

    ...
        @classmethod
        def create(cls, data: dict[str, str | int]) -> None:
            """Insert a new object into the database."""
            ...
        @classmethod
        def retrieve(cls, constellation_id: int) -> dict[str, str | int] | None:
            """Return a JSON representation of the object if found, otherwise return None."""
            ...
        @classmethod
        def update(cls, constellation_id: int, data: dict[str, str | int]) -> bool:
            """Update the object in the database."""
            ...
        @classmethod
        def delete(cls, constellation_id: int) -> bool:
            """Delete the object from the database."""
            ...
        @classmethod
        def list(cls) -> list[dict[str, str | int]]:
            """Return a list of objects present in the database."""
            ...
    ...

The other modules in the `models` package are similar.

The functions in `constellations.py` in the `controllers` package had minor changes.  Previously, 
when these functions were called, they simply returned a generic response. The functions now call 
the corresponding methods of `constellations.py` in the `models` package.  For example:
    
    def handle_get(constellation_id: int) -> tuple[dict[str, str | int |
                                                             dict[str, str | int]], int]:
        """Handle the GET request."""
        obj = constellations.Constellation.retrieve(constellation_id)
        if not obj:
            return {
                "message": "Constellation not found."
            }, HTTPStatus.NOT_FOUND
    
        return {
            "result": obj,
            "message": "Constellation successfully retrieved."
        }, HTTPStatus.OK

The `handle_get()` function first calls the `retrieve()` method and then returns an 
appropriate response depending on the method's return value.

The other modules in the `controllers` package are similar.

In the `constellations.py` module in the `resources` package, we added a parser for user requests:

    def parse_request() -> reqparse.Namespace:
        """Parse the user's request."""
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("constellation_id",
                            type=int
                            )
        parser.add_argument("constellation_name",
                            type=str,
                            required=True,
                            help=constants.VALIDATE_NOT_NULL
                            )
        ...
        return parser.parse_args()

This is basically a helper function for POST and PUT requests.  Previously, the methods receiving 
these types of requests blindly forwarded the JSON in the request to the corresponding function of 
`constellation.py` in the `controllers` package.  Using the helper function, the method can perform 
some checks first and forwards the JSON only if the validation is successful.  For example:

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        data = parse_request()
        return constellations.handle_post(data)

The other modules in the `resources` package are similar.

Note the statement `from __future__ import annotations`.  Since this project was developed using 
Python 3.9, this import is necessary for Python to properly interpret the type hints.  This 
import is not needed for later Python versions.

#### Chapter 3: Setting up password hashing

Python libraries added:

    bcrypt
    passlib

For security, we need to save the hash of the users' passwords, not the actual passwords.  We
use the `passlib` library for this.  We add a new module `hashing.py` to the `controllers` package:

    ...
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    def bcrypt(password: str) -> str:
        """Return a hash of the password."""
        return pwd_ctx.hash(password)
    
    
    def verify(hashed_string: str, plaintext_password: str) -> bool:
        """Check whether the given plaintext password equals the hashed string."""
        return pwd_ctx.verify(plaintext_password, hashed_string)

This module is a helper module for password hashing and verification.

In `users.py` of `controllers` module, we modify the functions that register new users and 
update existing users.  We first hash the password in the data received (if the password exists),
before forwarding the data.  For example:

    ...
    def handle_post(data: Namespace) -> tuple[dict[str, str], int]:
        """Handle the POST request."""
        plaintext_password = data.get("password")
        if plaintext_password:
            data["password"] = hashing.bcrypt(plaintext_password)
    ...

### References

Please refer to the documentations for more information.

- Flask documentation at https://flask.palletsprojects.com/en/stable/
- Flask-RESTful documentation at https://flask-restful.readthedocs.io/en/latest/index.html
- Flask-SQLAlchemy documentation at https://flask-sqlalchemy.readthedocs.io/en/stable/
- Flask-JWT-Extended documentation at https://flask-jwt-extended.readthedocs.io/en/stable/index.html
