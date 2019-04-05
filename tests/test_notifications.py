import unittest

from models import Subscription


class TestNotifications(unittest.TestCase):

    def test_should_subscribe_to_notifications():

        username = 'mtslucasmartins99'
        application_id = 'ottimizza-zapcontabil'
        subscription_info = {

        }

        subscription = Subscription(username, application_id, subscription_info)

        # testings
        self.assertEquals(username, subscription.username)
