from typing import Any

import pytest

from moleql.mql.errors import ProjectionError
from moleql.mql.projection_handler import ProjectionHandler


def get_projection_with_json():
    return ProjectionHandler(
        projection_parameter=(
            'fields={"vulnerabilities":{"$elemMatch":'
            '{"risk_score": {"$gt": 5}}}},created,last_updated'
        )
    ).projection


def get_projection_with_invalid_json():
    return ProjectionHandler(
        projection_parameter=(
            "fields={'vulnerabilities': "
            "{'$elemMatch':{'score': {'$gt': "
            "5}}}},created,last_updated"
        )
    ).projection


class TestProjection:
    def test_when_projection_has_no_value(self):
        expected: Any = None
        actual: Any = ProjectionHandler(projection_parameter="fields=").projection
        assert expected == actual

    def test_when_projection_has_inclusion_values(self):
        expected: Any = {"_id": 1, "score": 1}
        actual: Any = ProjectionHandler(projection_parameter="fields=_id,score").projection
        assert expected == actual

    def test_when_projection_has_exclusion_values(self):
        expected: Any = {"_id": 0, "score": 0}
        actual: Any = ProjectionHandler(projection_parameter="fields=-_id,-score").projection
        assert expected == actual

    def test_when_json_is_not_valid(self):
        with pytest.raises(ProjectionError):
            get_projection_with_invalid_json()

    def test_when_projection_has_json_value(self):
        expected: Any = {
            "vulnerabilities": {"$elemMatch": {"risk_score": {"$gt": 5}}},
            "created": 1,
            "last_updated": 1,
        }
        assert get_projection_with_json() == expected
