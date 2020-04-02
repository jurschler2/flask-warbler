"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from flask import session

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

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


class UserViewTestCase(TestCase):
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

    def test_homepage(self):
        """ Tests whether the home page displays properly """

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(session), 0)
            self.assertIn("<h4>New to Warbler?</h4>", html)
            self.assertNotIn('<li><a href="/logout">Log out</a></li>', html)

    def view_followers_page(self):
        """ Test whether a logged in user can see any user's list of followers
        and people that user is following """
