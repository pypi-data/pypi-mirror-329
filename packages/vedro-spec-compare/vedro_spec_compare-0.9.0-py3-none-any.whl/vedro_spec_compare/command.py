import argparse

from .changes import changes
from .coverage import coverage
from .discrepancy import discrepancy


def command() -> None:
    parser = argparse.ArgumentParser(description='vedro-spec-compare commands')
    subparsers = parser.add_subparsers(help='Available commands', required=True)

    coverage_parser = subparsers.add_parser('coverage', help='Generate coverage report')
    coverage_parser.add_argument('golden_spec_path', type=str, help='Path to the golden OpenAPI spec')
    coverage_parser.add_argument('testing_spec_path', type=str, help='Path to the testing OpenAPI spec')
    coverage_parser.add_argument(
        '--report-path', type=str, help='The path of the coverage report', default='coverage.html'
    )
    coverage_parser.set_defaults(func=coverage)

    discrepancy_parser = subparsers.add_parser('discrepancy', help='Generate discrepancy report')
    discrepancy_parser.add_argument('golden_spec_path', type=str, help='Path to the golden OpenAPI spec')
    discrepancy_parser.add_argument('testing_spec_path', type=str, help='Path to the testing OpenAPI spec')
    discrepancy_parser.add_argument(
        '--report-path', type=str, help='The path of the discrepancy report', default='discrepancy.html'
    )
    discrepancy_parser.set_defaults(func=discrepancy)

    changes_parser = subparsers.add_parser('changes', help='Generate changes report')
    changes_parser.add_argument('current_spec_path', type=str, help='Path to the current OpenAPI spec')
    changes_parser.add_argument('previous_spec_path', type=str, help='Path to the previous OpenAPI spec')
    changes_parser.add_argument(
        '--report-path', type=str, help='The path of the changes report', default='changes.html'
    )
    changes_parser.set_defaults(func=changes)

    args = parser.parse_args()
    args.func(args)
