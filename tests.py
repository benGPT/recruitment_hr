import unittest
from auth import hash_password, verify_password
from database import init_db, execute_db_query

class TestAuthFunctions(unittest.TestCase):
    def test_password_hashing(self):
        password = "test_password"
        hashed = hash_password(password)
        self.assertTrue(verify_password(hashed, password))
        self.assertFalse(verify_password(hashed, "wrong_password"))

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Set up a test database
        self.original_db_name = database.DATABASE_NAME
        database.DATABASE_NAME = 'test_miracle_healthcare.db'
        init_db()

    def tearDown(self):
        # Clean up the test database
        import os
        os.remove('test_miracle_healthcare.db')
        database.DATABASE_NAME = self.original_db_name

    def test_execute_db_query(self):
        # Test inserting and retrieving data
        insert_query = "INSERT INTO users (email, password) VALUES (?, ?)"
        execute_db_query(insert_query, ('test@example.com', 'password'), fetch=False)

        select_query = "SELECT * FROM users WHERE email = ?"
        result = execute_db_query(select_query, ('test@example.com',))
        self.assertIsNotNone(result)
        self.assertEqual(result[0][1], 'test@example.com')

if __name__ == '__main__':
    unittest.main()

