import logging
import operator
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Union

import pandas as pd

info_log = logging.getLogger("info")


def calculate_end_pos(variant_start: int, variant_ref: str) -> int:
    """Calculate the end position for a variant
    Args:
        variant_start (int): The start position of the variant
        variant_ref (str): The reference allele of the variant

    Returns:
        int: The end position of the variant
    """
    return variant_start + len(variant_ref) - 1


@dataclass
class PhEvalResult:
    """Base class for PhEval results."""


@dataclass
class PhEvalGeneResult(PhEvalResult):
    """Minimal data required from tool-specific output for gene prioritisation result
    Args:
        gene_symbol (Union[List[str], str]): The gene symbol(s) for the result entry
        gene_identifier (Union[List[str], str]): The ENSEMBL gene identifier(s) for the result entry
        score (float): The score for the gene result entry
    Notes:
        While we recommend providing the gene identifier in the ENSEMBL namespace,
        any matching format used in Phenopacket interpretations is acceptable for result matching purposes
        in the analysis.
    """

    gene_symbol: Union[List[str], str]
    gene_identifier: Union[List[str], str]
    score: float


@dataclass
class RankedPhEvalGeneResult(PhEvalGeneResult):
    """PhEval gene result with corresponding rank
    Args:
        rank (int): The rank for the result entry
    """

    rank: int

    @staticmethod
    def from_gene_result(pheval_gene_result: PhEvalGeneResult, rank: int):
        """Return RankedPhEvalGeneResult from a PhEvalGeneResult and rank
        Args:
            pheval_gene_result (PhEvalGeneResult): The gene result entry
            rank (int): The corresponding rank for the result entry

        Returns:
            RankedPhEvalGeneResult: The result as a RankedPhEvalGeneResult
        """
        return RankedPhEvalGeneResult(
            gene_symbol=pheval_gene_result.gene_symbol,
            gene_identifier=pheval_gene_result.gene_identifier,
            score=pheval_gene_result.score,
            rank=rank,
        )


@dataclass
class PhEvalVariantResult(PhEvalResult):
    """Minimal data required from tool-specific output for variant prioritisation
    Args:
        chromosome (str): The chromosome position of the variant recommended to be provided in the following format.
        This includes numerical designations from 1 to 22 representing autosomal chromosomes,
        as well as the sex chromosomes X and Y, and the mitochondrial chromosome MT.
        start (int): The start position of the variant
        end (int): The end position of the variant
        ref (str): The reference allele of the variant
        alt (str): The alternate allele of the variant
        score (float): The score for the variant result entry
    Notes:
        While we recommend providing the variant's chromosome in the specified format,
        any matching format used in Phenopacket interpretations is acceptable for result matching purposes
        in the analysis.
    """

    chromosome: str
    start: int
    end: int
    ref: str
    alt: str
    score: float
    grouping_id: str = field(default=None)


@dataclass
class RankedPhEvalVariantResult(PhEvalVariantResult):
    """PhEval variant result with corresponding rank
    Args:
        rank (int): The rank for the result entry
    """

    rank: int = 0

    @staticmethod
    def from_variant_result(pheval_variant_result: PhEvalVariantResult, rank: int):
        """Return RankedPhEvalVariantResult from a PhEvalVariantResult and rank
        Args:
            pheval_variant_result (PhEvalVariantResult): The variant result entry
            rank (int): The corresponding rank for the result entry

        Returns:
            RankedPhEvalVariantResult: The result as a RankedPhEvalVariantResult
        """
        return RankedPhEvalVariantResult(
            chromosome=pheval_variant_result.chromosome,
            start=pheval_variant_result.start,
            end=pheval_variant_result.end,
            ref=pheval_variant_result.ref,
            alt=pheval_variant_result.alt,
            score=pheval_variant_result.score,
            rank=rank,
        )


@dataclass
class PhEvalDiseaseResult(PhEvalResult):
    """Minimal data required from tool-specific output for disease prioritisation
    Args:
        disease_name (str): Disease name for the result entry
        disease_identifier (str): Identifier for the disease result entry in the OMIM namespace
        score (str): Score for the disease result entry
    Notes:
        While we recommend providing the disease identifier in the OMIM namespace,
        any matching format used in Phenopacket interpretations is acceptable for result matching purposes
        in the analysis.
    """

    disease_name: str
    disease_identifier: str
    score: float


@dataclass
class RankedPhEvalDiseaseResult(PhEvalDiseaseResult):
    """PhEval disease result with corresponding rank
    Args:
        rank (int): The rank for the result entry
    """

    rank: int

    @staticmethod
    def from_disease_result(pheval_disease_result: PhEvalDiseaseResult, rank: int):
        """Return RankedPhEvalDiseaseResult from a PhEvalDiseaseResult and rank
        Args:
            pheval_disease_result (PhEvalDiseaseResult): The disease result entry
            rank (int): The corresponding rank for the result entry

        Returns:
            RankedPhEvalDiseaseResult: The result as a RankedPhEvalDiseaseResult
        """
        return RankedPhEvalDiseaseResult(
            disease_name=pheval_disease_result.disease_name,
            disease_identifier=pheval_disease_result.disease_identifier,
            score=pheval_disease_result.score,
            rank=rank,
        )


class SortOrder(Enum):
    """Enumeration representing sorting orders."""

    ASCENDING = 1
    """Ascending sort order."""
    DESCENDING = 2
    """Descending sort order."""


class ResultSorter:
    """Class for sorting PhEvalResult instances based on a given sort order."""

    def __init__(self, pheval_results: [PhEvalResult], sort_order: SortOrder):
        """
        Initialise ResultSorter

        Args:
            pheval_results ([PhEvalResult]): List of PhEvalResult instances to be sorted
            sort_order (SortOrder): Sorting order to be applied
        """
        self.pheval_results = pheval_results
        self.sort_order = sort_order

    def _sort_by_decreasing_score(self) -> [PhEvalResult]:
        """
        Sort results in descending order based on the score

        Returns:
            [PhEvalResult]: Sorted list of PhEvalResult instances.
        """
        return sorted(self.pheval_results, key=operator.attrgetter("score"), reverse=True)

    def _sort_by_increasing_score(self) -> [PhEvalResult]:
        """
        Sort results in ascending order based on the score

        Returns:
            [PhEvalResult]: Sorted list of PhEvalResult instances.
        """
        return sorted(self.pheval_results, key=operator.attrgetter("score"), reverse=False)

    def sort_pheval_results(self) -> [PhEvalResult]:
        """
        Sort results based on the specified sort order.

        Returns:
            [PhEvalResult]: Sorted list of PhEvalResult instances.
        """
        return (
            self._sort_by_increasing_score()
            if self.sort_order == SortOrder.ASCENDING
            else self._sort_by_decreasing_score()
        )


class ResultRanker:
    def __init__(self, pheval_result: List[PhEvalResult], sort_order: SortOrder):
        """
        Initialise the PhEvalRanker.
        Args:
            pheval_result (List[PhEvalResult]): PhEval results to rank.
            sort_order (SortOrder): Sorting order based on which ranking is performed.
        """
        self.pheval_result = pheval_result
        self.sort_order = sort_order
        self.ascending = sort_order == SortOrder.ASCENDING

    def rank(self) -> pd.DataFrame:
        """
        Rank PhEval results, managing tied scores (ex aequo) and handling grouping_id if present.

        Returns:
            pd.DataFrame : Ranked PhEval results with tied scores managed.
        """
        pheval_result_df = pd.DataFrame([data.__dict__ for data in self.pheval_result])

        if self._has_valid_grouping_id(pheval_result_df):
            pheval_result_df = self._rank_with_grouping_id(pheval_result_df)
        else:
            pheval_result_df = self._rank_without_grouping_id(pheval_result_df)
        return pheval_result_df.drop(columns=["min_rank", "grouping_id"], errors="ignore")

    @staticmethod
    def _has_valid_grouping_id(pheval_result_df: pd.DataFrame) -> bool:
        """Check if grouping_id exists and has no None values."""
        return (
            "grouping_id" in pheval_result_df.columns
            and not pheval_result_df["grouping_id"].isnull().any()
        )

    def _rank_with_grouping_id(self, pheval_result_df: pd.DataFrame) -> pd.DataFrame:
        """Apply ranking when grouping_id is present and has no None values."""
        pheval_result_df["min_rank"] = (
            pheval_result_df.groupby(["score", "grouping_id"])
            .ngroup()
            .rank(method="dense", ascending=self.ascending)
        ).astype(int)
        pheval_result_df["rank"] = pheval_result_df.groupby("score")["min_rank"].transform("max")
        return pheval_result_df

    def _rank_without_grouping_id(self, pheval_result_df: pd.DataFrame) -> pd.DataFrame:
        """Apply ranking without using grouping_id."""
        pheval_result_df["rank"] = (
            pheval_result_df["score"].rank(method="max", ascending=self.ascending).astype(int)
        )
        return pheval_result_df


def _return_sort_order(sort_order_str: str) -> SortOrder:
    """
    Convert a string derived from the config file into SortOrder Enum

    Args:
        sort_order_str (str): String representation of the sorting order

    Returns:
        SortOrder: Enum representing the specified sorting order

    Raises:
        ValueError: If an incompatible or unknown sorting method is provided
    """
    try:
        return SortOrder[sort_order_str.upper()]
    except KeyError:
        raise ValueError("Incompatible ordering method specified.")


def _create_pheval_result(pheval_result: [PhEvalResult], sort_order_str: str) -> pd.DataFrame:
    """
    Create PhEval results with corresponding ranks based on the specified sorting order.

    Args:
        pheval_result ([PhEvalResult]): List of PhEvalResult instances to be processed.
        sort_order_str (str): String representation of the desired sorting order.

    Returns:
       pd.DataFrame: PhEval results with ranks assigned.
    """
    sort_order = _return_sort_order(sort_order_str)
    sorted_pheval_result = ResultSorter(pheval_result, sort_order).sort_pheval_results()
    return ResultRanker(sorted_pheval_result, sort_order).rank()


def _write_pheval_gene_result(
    ranked_pheval_result: pd.DataFrame, output_dir: Path, tool_result_path: Path
) -> None:
    """
    Write ranked PhEval gene results to a TSV file

    Args:
        ranked_pheval_result ([PhEvalResult]): List of ranked PhEval gene results
        output_dir (Path): Path to the output directory
        tool_result_path (Path): Path to the tool-specific result file
    """
    pheval_gene_output = ranked_pheval_result.loc[
        :, ["rank", "score", "gene_symbol", "gene_identifier"]
    ]
    pheval_gene_output.to_csv(
        output_dir.joinpath(
            "pheval_gene_results/" + tool_result_path.stem + "-pheval_gene_result.tsv"
        ),
        sep="\t",
        index=False,
    )


def _write_pheval_variant_result(
    ranked_pheval_result: pd.DataFrame, output_dir: Path, tool_result_path: Path
) -> None:
    """
    Write ranked PhEval variant results to a TSV file

    Args:
        ranked_pheval_result ([PhEvalResult]): List of ranked PhEval gene results
        output_dir (Path): Path to the output directory
        tool_result_path (Path): Path to the tool-specific result file
    """
    pheval_variant_output = ranked_pheval_result.loc[
        :, ["rank", "score", "chromosome", "start", "end", "ref", "alt"]
    ]
    pheval_variant_output.to_csv(
        output_dir.joinpath(
            "pheval_variant_results/" + tool_result_path.stem + "-pheval_variant_result.tsv"
        ),
        sep="\t",
        index=False,
    )


def _write_pheval_disease_result(
    ranked_pheval_result: pd.DataFrame, output_dir: Path, tool_result_path: Path
) -> None:
    """
    Write ranked PhEval disease results to a TSV file

    Args:
        ranked_pheval_result ([PhEvalResult]): List of ranked PhEval gene results
        output_dir (Path): Path to the output directory
        tool_result_path (Path): Path to the tool-specific result file
    """
    pheval_disease_output = ranked_pheval_result.loc[
        :, ["rank", "score", "disease_name", "disease_identifier"]
    ]
    pheval_disease_output.to_csv(
        output_dir.joinpath(
            "pheval_disease_results/" + tool_result_path.stem + "-pheval_disease_result.tsv"
        ),
        sep="\t",
        index=False,
    )


def generate_pheval_result(
    pheval_result: [PhEvalResult],
    sort_order_str: str,
    output_dir: Path,
    tool_result_path: Path,
) -> None:
    """
    Generate PhEval variant, gene or disease TSV result based on input results.

    Args:
        pheval_result ([PhEvalResult]): List of PhEvalResult instances to be processed.
        sort_order_str (str): String representation of the desired sorting order.
        output_dir (Path): Path to the output directory.
        tool_result_path (Path): Path to the tool-specific result file.

    Raises:
        ValueError: If the results are not all the same type or an error occurs during file writing.
    """
    if not pheval_result:
        info_log.warning(f"No results found for {tool_result_path.name}")
        return
    ranked_pheval_result = _create_pheval_result(pheval_result, sort_order_str)
    if all(isinstance(result, PhEvalGeneResult) for result in pheval_result):
        _write_pheval_gene_result(ranked_pheval_result, output_dir, tool_result_path)
    elif all(isinstance(result, PhEvalVariantResult) for result in pheval_result):
        _write_pheval_variant_result(ranked_pheval_result, output_dir, tool_result_path)
    elif all(isinstance(result, PhEvalDiseaseResult) for result in pheval_result):
        _write_pheval_disease_result(ranked_pheval_result, output_dir, tool_result_path)
    else:
        raise ValueError("Results are not all of the same type.")
