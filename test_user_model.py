"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows, DEFAULT_IMAGE_URL

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Test that User is created with 0 messages, followers, and
        liked_messages."""
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)

        # self.assertEqual(u1.password, "password")
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)

    def test_user_repr(self):
        """Test that User repr is returning correct details."""

        u1 = User.query.get(self.u1_id)
        repr = u1.__repr__()

        self.assertEqual(repr, f"<User #{u1.id}: {u1.username}, {u1.email}>")

    def test_is_following_true_success(self):
        """Test if is_following correctly returns true
        when user1 added to user2's followers."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u2.followers.append(u1)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))

    def test_is_following_false_success(self):
        """Test if is_following correctly returns false
        when neither user follows the other"""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    # TODO: def test_is_followed_true_success(self):

    # TODO: def test_is_followed_false_success(self):

    # TODO: def test_signup_valid_creds(self):

    # TODO: def test_signup_invalid_creds(self):

    # TODO: def test_authenticate_valid_creds(self):

    # TODO: def test_authenticate_invalid_username(self):

    # TODO: def test_authenticate_invalid_password(self):
