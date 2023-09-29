from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from djet import assertions

from djoser.views import UserViewSet

from authorization.tests.common import create_user, login_user, TEST_DATA


User = get_user_model()


class UserMeDeleteViewTestCase(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    viewset = UserViewSet

    def test_delete_user_if_logged_in(self):
        user = create_user()
        self.assert_instance_exists(User, email=TEST_DATA["email"])
        data = {"current_password": TEST_DATA["password"]}

        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse("user-me"), data=data)

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assert_instance_does_not_exist(User, email=TEST_DATA["email"])

    def test_not_delete_if_fails_password_validation(self):
        user = create_user()
        self.assert_instance_exists(User, email=TEST_DATA["email"])
        data = {"current_password": "incorrect"}

        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse("user-me"), data=data)

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"current_password": ["Invalid password."]})


class UserViewSetDeletionTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.EmailAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def test_delete_user_if_logged_in(self):
        user = create_user()
        self.assert_instance_exists(User, email=TEST_DATA["email"])
        data = {"current_password": TEST_DATA["password"]}

        login_user(self.client, user.email, TEST_DATA["password"])

        response = self.client.delete(
            reverse("user-detail", kwargs={User._meta.pk.name: user.pk}),
            data=data,
        )

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assert_instance_does_not_exist(User, email=TEST_DATA["email"])

    def test_not_delete_if_fails_password_validation(self):
        user = create_user()
        self.assert_instance_exists(User, email=TEST_DATA["email"])
        data = {"current_password": "incorrect"}

        login_user(self.client, user.email, TEST_DATA["password"])

        response = self.client.delete(
            reverse("user-detail", kwargs={User._meta.pk.name: user.pk}),
            data=data,
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"current_password": ["Invalid password."]})