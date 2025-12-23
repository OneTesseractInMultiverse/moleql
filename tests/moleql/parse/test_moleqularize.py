from moleql import moleqularize


class TestMoleqularize:
    def test_when_empty_query(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = moleqularize("").mongo_query
        assert expected == actual


class TestMoleqularizeProjection:
    def test_simple_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1},
        }
        actual = moleqularize("fields=_id").mongo_query
        assert expected == actual

    def test_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0},
        }
        actual = moleqularize("fields=-_id").mongo_query
        assert expected == actual

    def test_embedded_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"settings.group": 1},
        }
        actual = moleqularize("fields=settings.group").mongo_query
        assert expected == actual

    def test_multiple_field_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1, "score": 1, "status": 1},
        }
        actual = moleqularize("fields=_id,score,status").mongo_query
        assert expected == actual

    def test_multiple_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0, "score": 0, "status": 0},
        }
        actual = moleqularize("fields=-_id,-score,-status").mongo_query
        assert expected == actual

    def test_complex_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {
                "vulnerabilities": {"$elemMatch": {"score": {"$gt": 5}}},
                "last_seen": 1,
                "due_date": 1,
            },
        }
        actual = moleqularize(
            'fields={"vulnerabilities": {"$elemMatch":{"score": {"$gt":' " 5}}}},last_seen,due_date"
        ).mongo_query
        assert expected == actual
