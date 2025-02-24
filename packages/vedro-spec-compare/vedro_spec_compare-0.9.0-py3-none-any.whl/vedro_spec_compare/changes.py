import logging
from typing import Any

from .differ import DifferChanges
from .generator import Generator
from .parser import Parser


def changes(args: Any) -> None:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger("Changes")

    try:
        logger.info("Determination changes to the Open API spec")

        logger.info(f"Parsing the current spec: {args.current_spec_path}")
        current_spec_method = Parser.parse(args.current_spec_path)

        logger.info(f"Parsing the previous spec: {args.previous_spec_path}")
        previous_spec_method = Parser.parse(args.previous_spec_path)

        logger.info("Defining the difference")
        diff = DifferChanges(current_spec_method, previous_spec_method).get_diff()

        logger.info(f"Generating the changes report: {args.report_path}")
        Generator().changes_report(diff, args.report_path)

    except ValueError as e:
        logger.critical(f"{e}")
