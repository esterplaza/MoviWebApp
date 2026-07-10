from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
   A class used to represent a user

   Attributes
   ----------
   id : int
       Primary key, auto-incrementing
   name : str
       the name of the author
   """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        """
        Return a user-friendly string that represents the user
        """
        return f"User's name: {self.name} (User ID: {self.id}"

    def __repr__(self):
        """
        Return a readable string that represents the user
        """
        return (f"<User {self.id}: {self.name}>")


class Movie(db.Model):
    """
   A class used to represent a Movie

   Attributes
   ----------
   id : int
       Primary key, auto-incrementing
   name : str
       the name of the movie
   director : str
       the name of the movie's director
   year : int
       the year when the movie was released
   poster_url : str
       the url of the movie's poster
   user_id : str
       Foreign key referencing the user
   """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)