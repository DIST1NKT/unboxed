import unittest
from exercise1 import *


class TestGitApiURL(unittest.TestCase):

    def setUp(self):
        self.subdomain = 'subdomain'
        self.folder = 'folder'
        self.path = 'path'
        self.url = 'https://api.github.com/subdomain/folder/path'
        self.git_url = GitApiUrl(self.subdomain, self.folder, self.path)
        self.my_url = GitApiUrl('users', 'unboxed', 'repos')

    def test_init_url(self):
        self.assertEqual(self.subdomain, self.git_url.subdomain)
        self.assertEqual(self.folder, self.git_url.folder)
        self.assertEqual(self.path, self.git_url.path)
        self.assertEqual(self.url, self.git_url.url)

    def test_make_request(self):
        bad_response = self.git_url.make_request()
        self.assertIsNone(bad_response)
        good_response = self.my_url.make_request()
        self.assertTrue(isinstance(good_response, list))

    def tearDown(self):
        del self


class TestGitHubUser(unittest.TestCase):

    def setUp(self):
        self.subdomain = 'subdomain'
        self.folder = 'folder'
        self.path = 'path'
        self.url = 'https://api.github.com/subdomain/folder/path'
        self.repositories = {'repo1': 'Python', 'repo4': 'Python'}
        self.user = GitUser('username', self.url, self.repositories)

    def test_add_repositories(self):
        new_repos = {'repo2': 'Haskell', 'repo3': 'Java'}
        total_repos = dict(new_repos, **self.repositories)

        self.user.add_repositories({'repo2': 'Haskell', 'repo3': 'Java'})
        self.assertEqual(self.user.repositories, total_repos)

        with self.assertRaises(AssertionError):
            self.user.add_repositories(['repo1', 'Haskell'])

    def test_get_repositories(self):
        repos = self.repositories.keys()
        self.assertIsInstance(repos, list)
        self.assertEqual(repos, self.user.get_repos())

    def test_get_languages(self):
        langs = self.repositories.values()
        self.assertIsInstance(langs, list)
        self.assertEqual(langs, self.user.get_languages())

    def test_favourite_language(self):
        self.assertEqual(self.user.favourite_language(), 'Python')

    def tearDown(self):
        del self


if __name__ == "__main__":
    unittest.main()
