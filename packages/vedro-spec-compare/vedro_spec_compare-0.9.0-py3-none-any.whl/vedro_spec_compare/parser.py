import requests
import yaml
from schemax import collect_schema_data

from .models import APIMethods, RawSpecMethod


class Parser:
    @classmethod
    def parse(cls, spec_path: str) -> APIMethods:
        if spec_path.startswith("http://") or spec_path.startswith("https://"):
            return cls.parse_from_url(spec_path)
        else:
            return cls.parse_from_file(spec_path)

    @staticmethod
    def parse_from_raw(content: str) -> APIMethods:
        data = yaml.load(content, Loader=yaml.CLoader)
        api_methods = APIMethods({})
        for item in collect_schema_data(data):
            api_methods.add_method(RawSpecMethod.create(item))
        return api_methods

    @staticmethod
    def parse_from_url(url: str) -> APIMethods:
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {url}: status is {response.status_code}")

        return Parser.parse_from_raw(response.text)

    @staticmethod
    def parse_from_file(file_path: str) -> APIMethods:
        try:
            with open(file_path) as f:
                content = f.read()
            return Parser.parse_from_raw(content)
        except FileNotFoundError:
            raise ValueError(f"Failed to open file {file_path}: file not found")
