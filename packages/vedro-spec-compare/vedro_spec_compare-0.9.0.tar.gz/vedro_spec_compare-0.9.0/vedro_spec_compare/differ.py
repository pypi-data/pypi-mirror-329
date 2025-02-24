from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from .models import APIMethod, APIMethods


@dataclass
class ContentDiff:
    content: str
    added_fields: List[str]
    missed_fields: List[str]

    def __init__(self, content: str):
        self.content = content
        self.added_fields = []
        self.missed_fields = []

    def set_added_fields(self, fields: List[str]) -> None:
        self.added_fields = fields

    def set_missed_fields(self, fields: List[str]) -> None:
        self.missed_fields = fields


@dataclass
class ResponseBodyDiff:
    code: str
    content_diff: Dict[str, ContentDiff]

    def __init__(self, code: str):
        self.code = code
        self.content_diff = {}

    def add_added_fields(self, content: str, fields: List[str]) -> None:
        if content not in self.content_diff and fields:
            self.content_diff[content] = ContentDiff(content)
        if fields:
            self.content_diff[content].set_added_fields(fields)

    def add_missed_fields(self, content: str, fields: List[str]) -> None:
        if content not in self.content_diff and fields:
            self.content_diff[content] = ContentDiff(content)
        if fields:
            self.content_diff[content].set_missed_fields(fields)


@dataclass
class APIMethodDiff:
    method: str
    route: str

    added_query_params: List[str]
    missed_query_params: List[str]

    request_body_diff: Dict[str, ContentDiff]

    added_status_codes: List[str]
    missed_status_codes: List[str]

    response_body_diff: Dict[str, ResponseBodyDiff]

    @classmethod
    def create(cls, method_data: APIMethod) -> "APIMethodDiff":
        return cls(
            method=method_data.method,
            route=method_data.route,
            added_query_params=[],
            missed_query_params=[],
            request_body_diff={},
            added_status_codes=[],
            missed_status_codes=[],
            response_body_diff={},
        )

    def set_added_query_params(self, query_params: Set[str]) -> None:
        self.added_query_params = sorted(query_params)

    def set_missed_query_params(self, query_params: Set[str]) -> None:
        self.missed_query_params = sorted(query_params)

    def add_added_request_body_fields(self, content: str, fields: List[str]) -> None:
        if content not in self.request_body_diff and fields:
            self.request_body_diff[content] = ContentDiff(content)
        if fields:
            self.request_body_diff[content].set_added_fields(fields)

    def add_missed_request_body_fields(self, content: str, fields: List[str]) -> None:
        if content not in self.request_body_diff and fields:
            self.request_body_diff[content] = ContentDiff(content)
        if fields:
            self.request_body_diff[content].set_missed_fields(fields)

    def set_added_status_codes(self, codes: Set[str]) -> None:
        self.added_status_codes = sorted(codes)

    def set_missed_status_codes(self, codes: Set[str]) -> None:
        self.missed_status_codes = sorted(codes)

    def add_added_response_body_fields(self, code: str, content: str, fields: List[str]) -> None:
        if code not in self.response_body_diff and fields:
            self.response_body_diff[code] = ResponseBodyDiff(code)
        if fields:
            self.response_body_diff[code].add_added_fields(content, fields)

    def add_missed_response_body_fields(self, code: str, content: str, fields: List[str]) -> None:
        if code not in self.response_body_diff and fields:
            self.response_body_diff[code] = ResponseBodyDiff(code)
        if fields:
            self.response_body_diff[code].add_missed_fields(content, fields)

    def is_modified(self) -> bool:
        if (
            self.added_query_params
            or self.missed_query_params
            or self.request_body_diff
            or self.added_status_codes
            or self.missed_status_codes
            or self.response_body_diff
        ):
            return True
        return False


@dataclass
class Diff:
    added: List[APIMethodDiff]
    similar: List[APIMethodDiff]
    modified: List[APIMethodDiff]
    missed: List[APIMethodDiff]

    def __init__(self) -> None:
        self.added: List[APIMethodDiff] = []
        self.similar: List[APIMethodDiff] = []
        self.modified: List[APIMethodDiff] = []
        self.missed: List[APIMethodDiff] = []

    def add_added(self, method: APIMethodDiff) -> None:
        self.added.append(method)

    def add_similar(self, method: APIMethodDiff) -> None:
        self.similar.append(method)

    def add_modified(self, method: APIMethodDiff) -> None:
        self.modified.append(method)

    def add_missed(self, method: APIMethodDiff) -> None:
        self.missed.append(method)


class Differ:
    def __init__(self, golden: APIMethods, testing: APIMethods) -> None:
        self.golden_ams = golden
        self.testing_ams = testing
        self.diff = Diff()

    @abstractmethod
    def get_diff(self) -> Any:
        pass

    def get_added_method_ids(self) -> List[str]:
        return sorted(self.golden_ams.get_ids() - self.testing_ams.get_ids())

    def get_missed_method_ids(self) -> List[str]:
        return sorted(self.testing_ams.get_ids() - self.golden_ams.get_ids())

    def get_common_method_ids(self) -> List[str]:
        return sorted(self.golden_ams.get_ids() & self.testing_ams.get_ids())

    def set_added_status_codes(self, method_id: str, method_diff: APIMethodDiff) -> None:
        method_diff.set_added_status_codes(
            self.golden_ams[method_id].get_codes() - self.testing_ams[method_id].get_codes()
        )

    def set_missed_status_codes(self, method_id: str, method_diff: APIMethodDiff) -> None:
        method_diff.set_missed_status_codes(
            self.testing_ams[method_id].get_codes() - self.golden_ams[method_id].get_codes()
        )

    def get_common_response_codes(self, method_id: str) -> List[str]:
        return sorted(self.golden_ams[method_id].get_codes() & self.testing_ams[method_id].get_codes())

    def set_added_queries(self, method_id: str, method_diff: APIMethodDiff) -> None:
        method_diff.set_added_query_params(
            self.golden_ams[method_id].query_params - self.testing_ams.methods[method_id].query_params
        )

    def set_missed_queries(self, method_id: str, method_diff: APIMethodDiff) -> None:
        method_diff.set_missed_query_params(
            self.testing_ams[method_id].query_params - self.golden_ams[method_id].query_params
        )

    def set_added_request_body_fields(
            self, method_id: str, method_diff: APIMethodDiff, content_type: str = "application/json"
    ) -> None:
        method_diff.add_added_request_body_fields(
            content_type,
            self.compare_schemas(
                self.golden_ams[method_id].request_body_schema[content_type].get("properties", {}),
                self.testing_ams[method_id].request_body_schema[content_type].get("properties", {})
            )
        )

    def set_missed_request_body_fields(
            self, method_id: str, method_diff: APIMethodDiff, content_type: str = "application/json"
    ) -> None:
        method_diff.add_missed_request_body_fields(
            content_type,
            self.compare_schemas(
                self.testing_ams.methods[method_id].request_body_schema[content_type].get("properties", {}),
                self.golden_ams.methods[method_id].request_body_schema[content_type].get("properties", {})
            )
        )

    def set_added_response_body_fields(
            self, method_id: str, method_diff: APIMethodDiff, code: str, content_type: str = "application/json"
    ) -> None:
        method_diff.add_added_response_body_fields(
            code,
            content_type,
            self.compare_schemas(
                self.golden_ams[method_id].response_body_schema[code][content_type].get("properties", {}),
                self.testing_ams[method_id].response_body_schema[code][content_type].get("properties", {})
            )
        )

    def set_missed_response_body_fields(
            self, method_id: str, method_diff: APIMethodDiff, code: str, content_type: str = "application/json"
    ) -> None:
        method_diff.add_missed_response_body_fields(
            code,
            content_type,
            self.compare_schemas(
                self.testing_ams[method_id].response_body_schema[code][content_type].get("properties", {}),
                self.golden_ams[method_id].response_body_schema[code][content_type].get("properties", {})
            )
        )

    def compare_schemas(
            self, golden_schema: Dict[str, Any], testing_schema: Dict[str, Any], path: str = ""
    ) -> List[str]:
        differences = []
        for key in golden_schema:
            current_path = f"{path}.{key}" if path else key
            if key not in testing_schema:
                differences.append(current_path)
            elif golden_schema[key]["type"] == "array" and golden_schema[key]["items"]["type"] == "object":
                differences.extend(self.compare_schemas(
                    golden_schema[key]["items"].get("properties", {}),
                    testing_schema[key]["items"].get("properties", {}),
                    current_path + ".[*]"
                ))
            elif golden_schema[key]["type"] == 'object':
                differences.extend(self.compare_schemas(
                    golden_schema[key].get("properties", {}),
                    testing_schema[key].get("properties", {}),
                    current_path
                ))
        return differences


@dataclass
class DiffDataCoverage:
    def __init__(self, diff: Diff):
        self.all: int = len(diff.added) + len(diff.similar) + len(diff.modified)
        self.full: int = len(diff.similar)
        self.partial: int = len(diff.modified)
        self.empty: int = len(diff.added)
        self.methods_full: List[APIMethodDiff] = diff.similar
        self.methods_partial: List[APIMethodDiff] = diff.modified
        self.methods_empty: List[APIMethodDiff] = diff.added
        self.full_percent: float = round(self.full / self.all * 100, 2)
        self.partial_percent: float = 100 - self.full_percent - round(self.empty / self.all * 100, 2)
        self.empty_percent: float = 100 - self.full_percent - self.partial_percent
        stat_min_percent = 5
        self.stat_full_percent: float = (
                100
                - (max(self.empty_percent, stat_min_percent) if self.empty_percent else 0)
                - (max(self.partial_percent, stat_min_percent) if self.partial_percent else 0)
        )
        self.stat_partial_percent: float = (
                100
                - self.stat_full_percent
                - (max(self.empty_percent, stat_min_percent) if self.empty_percent else 0)
        )
        self.stat_empty_percent: float = 100 - self.stat_full_percent - self.stat_partial_percent


class DifferCoverage(Differ):
    def get_diff(self) -> DiffDataCoverage:
        for method_id in self.get_added_method_ids():
            self.diff.add_added(APIMethodDiff.create(self.golden_ams[method_id]))

        for method_id in self.get_common_method_ids():
            method_diff = APIMethodDiff.create(self.golden_ams[method_id])

            self.set_added_queries(method_id, method_diff)
            self.set_added_request_body_fields(method_id, method_diff)
            self.set_added_status_codes(method_id, method_diff)

            for code in self.get_common_response_codes(method_id):
                self.set_added_response_body_fields(method_id, method_diff, code)

            if method_diff.is_modified():
                self.diff.add_modified(method_diff)
                continue

            self.diff.add_similar(method_diff)

        return DiffDataCoverage(self.diff)


class DiffDataDiscrepancy:
    def __init__(self, diff: Diff):
        self.methods_partial: List[APIMethodDiff] = diff.modified
        self.methods_empty: List[APIMethodDiff] = diff.missed


class DifferDiscrepancy(Differ):
    def get_diff(self) -> DiffDataDiscrepancy:
        for method_id in self.get_missed_method_ids():
            self.diff.add_missed(APIMethodDiff.create(self.testing_ams[method_id]))

        for method_id in self.get_common_method_ids():
            method_diff = APIMethodDiff.create(self.golden_ams[method_id])

            self.set_missed_queries(method_id, method_diff)
            self.set_missed_request_body_fields(method_id, method_diff)
            self.set_missed_status_codes(method_id, method_diff)

            for code in self.get_common_response_codes(method_id):
                self.set_missed_response_body_fields(method_id, method_diff, code)

            if method_diff.is_modified():
                self.diff.add_modified(method_diff)
                continue

        return DiffDataDiscrepancy(self.diff)


class DiffDataChanges:
    def __init__(self, diff: Diff):
        self.added: List[APIMethodDiff] = diff.added
        self.modified: List[APIMethodDiff] = diff.modified
        self.deleted: List[APIMethodDiff] = diff.missed


class DifferChanges(Differ):
    def get_diff(self) -> DiffDataChanges:
        for method_id in self.get_added_method_ids():
            self.diff.add_added(APIMethodDiff.create(self.golden_ams[method_id]))

        for method_id in self.get_missed_method_ids():
            self.diff.add_missed(APIMethodDiff.create(self.testing_ams[method_id]))

        for method_id in self.get_common_method_ids():
            method_diff = APIMethodDiff.create(self.golden_ams[method_id])

            self.set_added_queries(method_id, method_diff)
            self.set_missed_queries(method_id, method_diff)

            self.set_added_request_body_fields(method_id, method_diff)
            self.set_missed_request_body_fields(method_id, method_diff)

            self.set_added_status_codes(method_id, method_diff)
            self.set_missed_status_codes(method_id, method_diff)

            for code in self.get_common_response_codes(method_id):
                self.set_added_response_body_fields(method_id, method_diff, code)
                self.set_missed_response_body_fields(method_id, method_diff, code)

            if method_diff.is_modified():
                self.diff.add_modified(method_diff)
                continue

        return DiffDataChanges(self.diff)
