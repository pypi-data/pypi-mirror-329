import logging
from typing import Any

from .differ import DifferDiscrepancy
from .generator import Generator
from .parser import Parser


def discrepancy(args: Any) -> None:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger("Discrepancy")

    try:
        logger.info("Determination of discrepancy in doc regarding tests")

        logger.info(f"Parsing the golden spec: {args.golden_spec_path}")
        golden_spec_method = Parser.parse(args.golden_spec_path)

        logger.info(f"Parsing the testing spec: {args.testing_spec_path}")
        testing_spec_method = Parser.parse(args.testing_spec_path)

        logger.info("Defining the difference")
        diff = DifferDiscrepancy(golden_spec_method, testing_spec_method).get_diff()

        logger.info(f"Generating the discrepancy report: {args.report_path}")
        Generator().discrepancy_report(diff, args.report_path)

    except ValueError as e:
        logger.critical(f"{e}")
