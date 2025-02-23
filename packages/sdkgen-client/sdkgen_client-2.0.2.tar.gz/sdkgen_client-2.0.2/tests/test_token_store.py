import unittest

from src.sdkgen import MemoryTokenStore
from src.sdkgen.access_token import AccessToken


class TestTokenStore(unittest.TestCase):
    def test_memory_token_store(self):
        token = AccessToken()
        token.access_token = 'foobar'

        store = MemoryTokenStore()

        store.persist(token)

        stored_token = store.get()

        self.assertEqual(token.access_token, stored_token.access_token)

        store.remove()

        self.assertEqual(None, store.get())


if __name__ == '__main__':
    unittest.main()
