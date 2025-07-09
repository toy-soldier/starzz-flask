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
