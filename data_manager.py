from models import db, User, Movie


class DataManager():
    def create_user(self, name):
        """
        Add a new user to your database.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_user(self, user_id):
        """
        Return the object user with user_id
        """
        return db.session.execute(
            db.select(User).where(User.id == user_id)
        ).scalar_one_or_none()

    def get_users(self):
        """
        Return a list of all users in your database
        """
        return db.session.execute(db.select(User).order_by(User.id)).scalars().all()

    def get_movies(self, user_id):
        """
        Return a list of all movies of a specific user.
        """
        return db.session.execute(db.select(Movie).where(Movie.user_id == user_id)).scalars().all()

    def add_movie(self, movie):
        """
        Add a new movie to a user’s favorites
        """
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """
        Update the details of a specific movie in the database.
        Returns True if the movie has been updated, returns False if the movie_id
        has not been found.
        """
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar_one_or_none()
        if not movie_to_update:
            return False
        movie_to_update.name = new_title
        db.session.commit()
        return True

    def delete_movie(self, movie_id):
        """
        Delete the movie from the user’s list of favorites.
        Returns True if the movie has been deleted, returns False if the movie_id
        has not been found.
        """
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar_one_or_none()
        if not movie_to_delete:
            return False
        db.session.delete(movie_to_delete)
        db.session.commit()
        return True
