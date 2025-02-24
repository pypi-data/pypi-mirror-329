import os
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template

from .differ import DiffDataChanges, DiffDataCoverage, DiffDataDiscrepancy


class Generator:
    _PATH_TEMPLATES = os.path.dirname(os.path.realpath(__file__)) + '/templates'
    _TEMPLATE_COVERAGE = 'coverage.html.j2'
    _TEMPLATE_DISCREPANCY = 'discrepancy.html.j2'
    _TEMPLATE_CHANGES = 'changes.html.j2'

    def __init__(self) -> None:
        self._templates = Environment(loader=FileSystemLoader(self._PATH_TEMPLATES))

    def _get_template(self, template_name: str) -> Template:
        return self._templates.get_template(name=template_name)

    def _render_template(self, template_name: str, **kwargs: Any) -> str:
        template = self._get_template(template_name=template_name)
        return template.render(**kwargs)

    @staticmethod
    def _create_dir(dirname: str) -> None:
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    def _create_file(self, file_path: str, content: str) -> None:
        self._create_dir(os.path.dirname(file_path))
        with open(file_path, 'w') as file:
            file.write(content)

    def render_coverage_report(self, diff: DiffDataCoverage) -> str:
        return self._render_template(self._TEMPLATE_COVERAGE, **vars(diff))

    def coverage_report(self, diff: DiffDataCoverage, file_path: str) -> None:
        content = self.render_coverage_report(diff)
        self._create_file(file_path, content)

    def render_discrepancy_report(self, diff: DiffDataDiscrepancy) -> str:
        return self._render_template(self._TEMPLATE_DISCREPANCY, **vars(diff))

    def discrepancy_report(self, diff: DiffDataDiscrepancy, file_path: str) -> None:
        content = self.render_discrepancy_report(diff)
        self._create_file(file_path, content)

    def render_changes_report(self, diff: DiffDataChanges) -> str:
        return self._render_template(self._TEMPLATE_CHANGES, **vars(diff))

    def changes_report(self, diff: DiffDataChanges, file_path: str) -> None:
        content = self.render_changes_report(diff)
        self._create_file(file_path, content)
