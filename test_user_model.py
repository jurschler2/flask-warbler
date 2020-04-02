"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


USER_DATA = {
    "username":  "test1",
    "email": "test1@test.com",
    "password": "password"
}

USER_DATA_2 = {
    "username":  "test2",
    "email": "test2@test.com",
    "password": "password"
}

USER_DATA_3 = {
    "username":  "test3",
    "email": "test3@test.com",
    "password": "password"
}

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        testUser1 = User(**USER_DATA)
        db.session.add(testUser1)
        db.session.commit()

        self.testUser1 = testUser1
        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        """"Test User repr."""

        self.assertEqual(self.testUser1.__repr__(),
                         f"<User #{self.testUser1.id}: test1, test1@test.com>")

    def test_user_following(self):
        """Test User and Followers relationship."""

        testUser2 = User(**USER_DATA_2)
        db.session.add(testUser2)

        testUser3 = User(**USER_DATA_3)
        db.session.add(testUser3)

        db.session.commit()

        followers = Follows(user_following_id=self.testUser1.id,
                            user_being_followed_id=testUser2.id)
        db.session.add(followers)
        db.session.commit()

        self.assertEqual(len(self.testUser1.following), 1)
        self.assertEqual(len(testUser2.followers), 1)
        self.assertEqual(self.testUser1.following[0].id, testUser2.id)
        self.assertEqual(testUser2.followers[0].id, self.testUser1.id)

        self.assertNotEqual(self.testUser1.following[0].id, testUser3.id)
        self.assertNotEqual(testUser2.followers[0].id, testUser3.id)


# Here are some questions your tests should answer for the User model:

# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?