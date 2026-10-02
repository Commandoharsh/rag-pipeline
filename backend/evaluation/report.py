import json
from pathlib import Path


class EvaluationReport:

    def __init__(
        self,
        output_directory: str = "data/evaluation",
    ):
        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        report: dict,
        filename: str = "evaluation_report.json",
    ):

        path = (
            self.output_directory /
            filename
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    def load(
        self,
        filename: str = "evaluation_report.json",
    ):

        path = (
            self.output_directory /
            filename
        )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)
        