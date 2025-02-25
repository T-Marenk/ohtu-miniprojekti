import unittest
from services.reference_service import ReferenceService, ReferenceType
from entities.book_reference import BookReference


class StubRepo:
    def __init__(self, expected_data, database_content):
        self.expected_data = expected_data
        self.database_content = database_content

    def add_to_table(self, data):
        self.database_content.append(data)
        return data == self.expected_data

    def get_data(self):
        return self.database_content


class StubValidator:
    def __init__(self):
        pass

    def validate(self, reference_list):
        return reference_list


class TestReferenceService(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_book_reference_can_be_added(self):
        book_repo = StubRepo(["Test Author", "Test it to the limit",
                        2022, "TestPublishing", "test22", ""], [])
        web_repo = StubRepo([], [])
        validator = StubValidator()
        ref_service = ReferenceService(book_repo, web_repo, validator)
        result = ref_service.add_reference(
            ["Test Author", "Test it to the limit", 2022, "TestPublishing", "test22", ""], ReferenceType.Book)
        self.assertTrue(result)
        self.assertEqual(len(book_repo.database_content), 1)

    def test_all_references_from_database_with_one_book_reference_can_be_fetched(self):
        book_repo = StubRepo([], [
            (1, "Test Author", "Test it to the limit",
             2022, "TestPublishing", "test22", "")
        ])
        web_repo = StubRepo([], [])
        validator = StubValidator()
        ref_service = ReferenceService(book_repo, web_repo, validator)
        expected_list = [BookReference(
            "Test Author", "Test it to the limit", 2022, "TestPublishing", "test22", "")]
        result = ref_service.get_all_references()
        book_result = result["book_references"]
        self.assertEqual(str(book_result[0]), str(expected_list[0]))

    def test_all_references_from_database_with_two_book_references_can_be_fetched(self):
        book_repo = StubRepo([], [
            (1, "Test Author", "Test it to the limit",
             2022, "TestPublishing", "test22", ""),
            (2, "Stanley", "This is a story about a man named Stanley",
             2013, "GC", "stan13", "")
        ])
        validator = StubValidator()
        web_repo = StubRepo([], [])
        ref_service = ReferenceService(book_repo, web_repo, validator)
        expected_list = [
            BookReference("Test Author", "Test it to the limit",
                      2022, "TestPublishing", "test22", ""),
            BookReference(
                "Stanley", "This is a story about a man named Stanley", 2013, "GC", "stan13", "")
        ]
        result = ref_service.get_all_references()
        book_result = result["book_references"]
        for i, ref in enumerate(book_result):
            self.assertEqual(str(ref), str(expected_list[i]))
