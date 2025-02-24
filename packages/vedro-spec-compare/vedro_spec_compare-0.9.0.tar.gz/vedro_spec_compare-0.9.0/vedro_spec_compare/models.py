from dataclasses import dataclass
from typing import Any, Dict, Set

from schemax import SchemaData


@dataclass
class RawSpecMethod:
    method_spec_id: str
    method: str
    route: str
    query_params: Set[str]
    request_body_schema: Dict[str, Any]
    response_code: str
    response_body_schema: Dict[str, Any]

    @staticmethod
    def create(data: Any) -> "RawSpecMethod":
        if isinstance(data, SchemaData):
            return RawSpecMethod(
                method_spec_id=data.http_method + data.path,
                method=data.http_method,
                route=data.path,
                query_params=set(data.queries),
                request_body_schema=data.request_schema,
                response_code=str(data.status),
                response_body_schema=data.response_schema
            )
        else:
            raise ValueError("Unsupported data format")


@dataclass
class BodySchema:
    schema: Dict[str, Dict[str, Any]]

    @classmethod
    def create(cls, content_type: str, schema: Dict[str, Any]) -> "BodySchema":
        return BodySchema({
            content_type: schema
        })

    def get_content_types(self) -> Set[str]:
        return set(self.schema.keys())

    def __getitem__(self, key: str) -> Dict[str, Any]:
        return self.schema[key]


@dataclass
class ResponseBodySchema:
    schema: Dict[str, BodySchema]

    @classmethod
    def create(cls, status: str, content: BodySchema) -> "ResponseBodySchema":
        return ResponseBodySchema({
            status: content
        })

    def add_info(self, code: str, content_type: str, schema: Dict[str, Any]) -> None:
        if code not in schema:
            self.schema[code] = BodySchema.create(content_type, schema)

    def get_codes(self) -> Set[str]:
        return set(self.schema.keys())

    def __getitem__(self, key: str) -> BodySchema:
        return self.schema[key]


@dataclass
class APIMethod:
    method: str
    route: str
    query_params: Set[str]

    request_body_schema: BodySchema
    response_body_schema: ResponseBodySchema

    @classmethod
    def create(cls, rsm: RawSpecMethod) -> "APIMethod":
        return APIMethod(
            rsm.method,
            rsm.route,
            rsm.query_params,
            BodySchema.create("application/json", rsm.request_body_schema),
            ResponseBodySchema.create(
                rsm.response_code,
                BodySchema.create("application/json", rsm.response_body_schema)
            )
        )

    def add_info(self, spec_method: RawSpecMethod) -> None:
        self.response_body_schema.add_info(
            spec_method.response_code, "application/json", spec_method.response_body_schema
        )

    def get_codes(self) -> Set[str]:
        return self.response_body_schema.get_codes()


@dataclass
class APIMethods:
    methods: Dict[str, APIMethod]

    def add_method(self, rsm: RawSpecMethod) -> None:
        if rsm.method_spec_id not in self.methods:
            self.methods[rsm.method_spec_id] = APIMethod.create(rsm)
        else:
            self.methods[rsm.method_spec_id].add_info(rsm)

    def get_ids(self) -> Set[str]:
        return set(self.methods.keys())

    def __getitem__(self, key: str) -> APIMethod:
        return self.methods[key]
