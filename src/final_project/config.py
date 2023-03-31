"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()


GROUP = [
    "pop_share_in_manuf_sector_1900",
    "ln_income_per_capita",
    "ln_population_density_2000",
    "agriculture_diversity",
]

__all__ = ["BLD", "SRC", "TEST_DIR", "PAPER_DIR", "GROUP"]
