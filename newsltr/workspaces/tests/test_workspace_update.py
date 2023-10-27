from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from djet import assertions

from payments.tests.common import setup_subscription
from workspaces.models import Workspace
from .common import create_workspace, invite_user_to_workspace, TEST_DATA
from authorization.tests.common import (
    TEST_DATA as TEST_USER_DATA,
    create_user,
    login_user,
)


class WorkspaceUpdateViewTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    # We are using only partial update here, because we don't want to
    # update all fields, but only those that are provided in the request.
    # If we would use full update, we would have to provide all fields
    # in the request, otherwise they would be set to default values.
    def setUp(self):
        self.workspace, self.user = create_workspace()
        self.base_url = reverse("workspace-detail", args=(self.workspace.pk,))

    def test_update_workspace_without_authorization(self):
        response = self.client.patch(self.base_url, data=TEST_DATA)
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_update_workspace_with_authorization_without_subscription(self):
        login_user(self.client, self.user.email, TEST_USER_DATA["password"])

        response = self.client.patch(self.base_url, data=TEST_DATA)
        self.assert_status_equal(response, status.HTTP_403_FORBIDDEN)
        self.assert_instance_exists(
            Workspace, pk=self.workspace.pk, name=TEST_DATA["name"]
        )

    def test_update_workspace_with_authorization_with_subscription(self):
        setup_subscription(self.user)
        login_user(self.client, self.user.email, TEST_USER_DATA["password"])

        response = self.client.patch(self.base_url, data=TEST_DATA)
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assert_instance_exists(
            Workspace, pk=self.workspace.pk, name=TEST_DATA["name"]
        )

    def test_update_workspace_with_authorization_as_member(self):
        user = create_user(email="test2@test.com")
        invite_user_to_workspace(user, self.workspace, role="member")
        login_user(self.client, user.email, TEST_USER_DATA["password"])

        response = self.client.patch(self.base_url, data=TEST_DATA)
        self.assert_status_equal(response, status.HTTP_403_FORBIDDEN)
        self.assert_instance_exists(
            Workspace, pk=self.workspace.pk, name=self.workspace.name
        )
