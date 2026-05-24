from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Community, Post, Comment


class ModelTests(TestCase):
    """Tests for database models and their relationships."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", password="testpass")
        self.community = Community.objects.create(
            name="testcommunity", description="Test desc", created_by=self.user
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body text.",
            author=self.user,
            community=self.community,
        )

    def test_community_str(self):
        self.assertEqual(str(self.community), "r/testcommunity")

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_comment_count(self):
        self.assertEqual(self.post.comment_count(), 0)
        Comment.objects.create(post=self.post, author=self.user, body="hi")
        self.assertEqual(self.post.comment_count(), 1)

    def test_comment_parent_relationship(self):
        parent = Comment.objects.create(post=self.post, author=self.user, body="Parent")
        reply = Comment.objects.create(
            post=self.post, author=self.user, body="Reply", parent=parent
        )
        self.assertEqual(reply.parent, parent)
        self.assertIn(reply, parent.replies.all())


class ViewTests(TestCase):
    """Tests for views, including authentication and CRUD operations."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("viewuser", password="testpass")
        self.community = Community.objects.create(
            name="testcommunity", created_by=self.user
        )
        self.post = Post.objects.create(
            title="View Test Post",
            body="Some content",
            author=self.user,
            community=self.community,
        )

    # --- Accessibility / Response Code Tests ---

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_loads(self):
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_community_detail_loads(self):
        response = self.client.get(
            reverse("community_detail", args=[self.community.name])
        )
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    # --- Authentication Tests ---

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("create_post"))
        self.assertRedirects(response, "/login/?next=/post/new/")

    def test_create_community_requires_login(self):
        response = self.client.get(reverse("create_community"))
        self.assertRedirects(response, "/login/?next=/community/new/")

    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_can_login(self):
        response = self.client.post(
            reverse("login"), {"username": "viewuser", "password": "testpass"}
        )
        self.assertRedirects(response, reverse("home"))

    # --- CRUD Tests ---

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="viewuser", password="testpass")
        response = self.client.post(
            reverse("create_post"),
            {"title": "New Post", "body": "Content here.", "community": self.community.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New Post").exists())

    def test_logged_in_user_can_delete_own_post(self):
        self.client.login(username="viewuser", password="testpass")
        response = self.client.post(reverse("delete_post", args=[self.post.pk]))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_user_cannot_delete_others_post(self):
        other = User.objects.create_user("other", password="otherpass")
        self.client.login(username="other", password="otherpass")
        response = self.client.post(reverse("delete_post", args=[self.post.pk]))
        # Post should still exist
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    # --- Search Test ---

    def test_search_returns_matching_posts(self):
        response = self.client.get(reverse("home"), {"q": "View Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Post")

    def test_search_returns_no_results_for_bad_query(self):
        response = self.client.get(reverse("home"), {"q": "zzznomatch"})
        self.assertNotContains(response, "View Test Post")
