"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
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
    "password": "password",
    "image_url": ""

}

USER_DATA_2 = {
    "username":  "test2",
    "email": "test2@test.com",
    "password": "password",
    "image_url": ""
}

USER_DATA_3 = {
    "username":  "test3",
    "email": "test3@test.com",
    "password": "password",
    "image_url": ""
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

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

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

    def test_user_create_happy(self):
        """ Tests the class method create on User """

        testUserTrue = User.signup(**USER_DATA_2)
        self.assertIsInstance(testUserTrue, User)

    def test_invalid_username_signup(self):
        User.signup(None, "test@test.com", "password", None)
        self.assertRaises(exc.IntegrityError, db.session.commit)

    def test_invalid_email_signup(self):
        User.signup("testtest", None, "password", None)
        self.assertRaises(exc.IntegrityError, db.session.commit)

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None)

        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None)

    def test_user_authenticate(self):
        """ Tests the class method authenticate on User """

        testUserTrue = User.signup(**USER_DATA_2)
        db.session.commit()
        goodUsername = testUserTrue.username
        badUsername = "badUsername"
        goodPassword = "password"
        badPassword = "badpassword"
        userAuthenticated = User.authenticate(goodUsername,
                                              goodPassword)
        usernameNotAuthenticated = User.authenticate(badUsername,
                                                     goodPassword)
        passwordNotAuthenticated = User.authenticate(goodUsername,
                                                     badPassword)
        self.assertIsInstance(testUserTrue, User)
        self.assertTrue(userAuthenticated)
        self.assertFalse(usernameNotAuthenticated)
        self.assertFalse(passwordNotAuthenticated)


# Here are some questions your tests should answer for the User model:

# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
