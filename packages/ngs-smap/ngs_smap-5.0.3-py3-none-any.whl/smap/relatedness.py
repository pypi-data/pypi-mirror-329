import pandas as pd
from smap.haplotype import DosageMatrix
from smap.haplotype import INDEX_COLUMNS, LOCUS_COLUMN_NAME
from pathlib import Path
import argparse
from typing import Sequence, List, Union
from pandas.core.frame import DataFrame
from itertools import combinations_with_replacement, combinations
import logging
from natsort import natsort_keygen, natsorted
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from multiprocessing.pool import Pool
from timeit import default_timer as timer
import scipy.cluster.hierarchy as sch
import os
import sys
import scanpy as sc
import plotly.express as px

from smap import __version__

# logger = logging.getLogger(__name__)


def get_argument_parser() -> argparse.ArgumentParser:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        add_help=False,
        description="""Convert the haplotype table from SMAP
                                                    haplotype-sites or SMAP haplotype-windows into
                                                    a genetic similarity/distance matrix and/or a
                                                    locus information matrix.""",
    )

    parser.add_argument("-v", "--version", action="version", version=__version__)

    # Mandatory argument.
    """
    Mandatory argument specifying the name of the haplotypes table (haplotypes_R*_F*_*.txt).
    """
    parser.add_argument(
        "-t",
        "--table",
        required=True,
        type=str,
        help="""Name of the haplotypes table retrieved from SMAP haplotype-sites
                             or SMAP haplotype-windows in the input directory.""",
    )

    # Optional arguments.
    """
    Input data options.
    """
    parser.add_argument(
        "-i",
        "--input_directory",
        default=".",
        type=str,
        help="""Input directory containing the haplotypes table, the --samples
                                text file, and/or the --loci text file (default = current
                                directory).""",
    )
    parser.add_argument(
        "-n",
        "--samples",
        type=str,
        default=None,
        help="""Name of a tab-delimited text file in the input directory defining
                                the order of the (new) sample IDs in the matrix: first column =
                                old IDs, second column (optional) = new IDs (default = no list
                                provided, the order of sample IDs in the matrix equals their
                                order in the haplotypes table).""",
    )
    parser.add_argument(
        "-l",
        "--loci",
        type=str,
        default=None,
        help="""Name of a tab-delimited text file in the input directory
                                containing a one-column list of locus IDs formatted as in
                                the haplotypes table (default = no list provided).""",
    )

    """
    Analysis options.
    """

    parser.add_argument(
        "-lc",
        "--locus_completeness",
        default=0,
        type=float,
        help="""Minimum proportion of samples with haplotype data in a locus.
                                Loci with less data are removed (default = all loci are
                                included).""",
    )
    parser.add_argument(
        "-sc",
        "--sample_completeness",
        default=2,
        type=int,
        help="""Minimum number of loci with haplotype data in a sample. Samples
                                with less data are removed (default = all samples are
                                included).""",
    )
    parser.add_argument(
        "-p",
        "--processes",
        default=1,
        type=int,
        help="Number of processes used by the script (default = 1).",
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        default=".",
        type=str,
        help="Output directory (default = current directory).",
    )
    parser.add_argument(
        "--prefix",
        default="",
        type=str,
        help="Prefix added to all output file names (default = no prefix added).",
    )

    parser.add_argument(
        "--plot_format",
        choices=["pdf", "png", "svg", "jpg", "jpeg", "tif", "tiff"],
        default="pdf",
        help="""File format of plots (default = pdf, other options are png, svg,
                                jpg, jpeg, tif, and tiff).""",
    )

    parser.add_argument(
        "--debug", required=False, action="store_true", help="Enable verbose logging"
    )

    parser2 = argparse.ArgumentParser(
        prog="smap relatedness",
        description="""Convert the haplotype table from SMAP
        haplotype-sites or SMAP haplotype-windows into
        a genetic similarity/distance matrix and/or a
        locus information matrix using GRM or a Uniform Manifold Approximation
        and Projection for Dimension Reduction plot using UMAP.""",
    )
    subparsers = parser2.add_subparsers(dest="command")
    pairwise = subparsers.add_parser(
        "pairwise",
        help="Analyze all-against-all pairwise genetic similarities, or conversely or the loci that discriminate between sets of samples.",
        parents=[parser],
    )

    umap = subparsers.add_parser(
        "umap",
        help="Calculate the relatedness with the Uniform Manifold Approximation and Projection for Dimension Reduction technique.",
        parents=[parser],
    )

    umap.add_argument(
        "--clustering",
        choices=["leiden", "louvain"],
        default="leiden",
        help="Cluster cells using either the Leiden or Louvain algorithm",
    )

    """
    Output data options.
    """
    pairwise.add_argument(
        "--excel",
        action="store_true",
        help="""Write the matrix of the Pairwise analysis to excel""",
    )
    pairwise.add_argument(
        "--distance",
        default=None,
        choices=["d", "i"],
        help="""Convert genetic similarity estimates into
                genetic distances (default = no conversion
                to distances). Type 'd' for normal distance and 'i'
                for inversed distance""",
    )
    pairwise.add_argument(
        "--informative_loci",
        action="store_true",
        help="""Print locus information to the output directory.""",
    )
    pairwise.add_argument(
        "--mask",
        choices=["none", "upper", "lower"],
        default="lower",
        help="""Mask values on the main diagonal of each matrix and above (upper)
                                or below (lower) the main diagonal (default = Lower,
                                other options are: upper (mask upper half) and None (No masking).""",
    )
    pairwise.add_argument(
        "--cluster",
        action="store_true",
        help="Create a clustered matrix. The order provided in the samples file is ignored.",
    )

    # Parse arguments to a dictionary
    return parser2


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    logging.info("Parsing arguments.")
    parser = get_argument_parser()
    parsed_args = parser.parse_args(args)

    return parsed_args


# def create_pairwise_matrix(dosage_matrix: DosageMatrix):
#     """
#     Reads a dosage matrix and create a pairwise matrix by converting all values > 0
#     to 1. This thus creates an absent or present matrix for the haplotypes within
#     a loci for each sample.

#     Args:
#         dosage_matrix (DosageMatrix): A dosage matrix based on multi-allelic
#         haplotypes generated by SMAP haplotype-sites or SMAP haplotype-window

#     Returns:
#         Pairwise dataframe: A dataframe where all values > 0 are converted
#         to 1 that can be used to calculate the genetic relatedness between
#         samples. This thus returns an absent or present matrix for the
#         haplotypes within a loci for each sample
#     """
#     dosage_matrix._df[dosage_matrix._df > 0] = 1
#     return Pairwise(dosage_matrix._df)


class DosageMatrixExtended(DosageMatrix):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)
        self.samples = self._df.columns.to_list()

    @classmethod
    def read_dosage_matrix(cls, file_location: Path):
        logging.info("Reading dosage matrix")
        df = (
            pd.read_csv(file_location, sep="\t", parse_dates=False, dtype=str, header=0)
            .set_index(INDEX_COLUMNS)
            .apply(pd.to_numeric, errors="raise")
        )
        logging.info("Reading dosage matrix finished")
        return cls(df)

    def convert_dosage_matrix(self):
        self._df[self._df > 0] = 1
        return self

    def order_and_pool_samples(self, samples):
        try:
            with open(samples, "r") as file:
                IDs = dict(line.strip().split(maxsplit=1) for line in file)
        except ValueError:
            logging.warning(
                "No new sample IDs or groups where provided, "
                "continuing with samples only"
            )
            with open(samples, "r") as file:
                samples_list = [line.strip().split()[0] for line in file]
                IDs = {sample: sample for sample in samples_list}

        """
        Pool samples if specified in the samples file. Rename samples in the
        haplotypes table.
        """
        try:
            assert len(list(set(IDs.keys()) - set(list(self._df.columns)))) == 0
        except AssertionError:
            missing = list(set(IDs.keys()) - set(list(self._df.columns)))
            logging.error(
                f"Samples {missing} could not be found in the input table."
                "\nPlease check your samples file."
            )
            sys.exit("Terminating SMAP relatedness")
        for sample, ID in IDs.items():
            if ID:
                pool = [s for s in IDs if IDs[s] == ID]
                if len(pool) > 1 and ID not in self._df.columns:
                    # Pool samples with the same sample ID.
                    logging.info(
                        f"The samples {', '.join(pool[:-1])} and {pool[-1]} "
                        f"were combined into one sample with ID {ID}."
                    )
                    self._df[ID] = (
                        self._df.loc[:, pool]
                        .astype(float)
                        .sum(axis=1, numeric_only=True, min_count=1)
                    )
                    self._df.drop(pool, axis=1, inplace=True)
                else:
                    # Rename samples if a new ID is specified.
                    self._df.rename(columns={sample: ID}, inplace=True)
        """
        Reorder the columns in the dataframe based on the order of the samples
        in IDs.
        """
        order = list()
        for sample, ID in IDs.items():
            if ID:
                if ID not in order:
                    order.append(ID)
            else:
                order.append(sample)
        self._df = self._df[order]
        self._df[self._df > 0] = 1
        self.samples = self._df.columns.tolist()
        return self

    def subset_loci(self, loci: Path):
        with open(loci, "r") as file:
            loci_list = [locus.strip() for locus in file]
        original_loci = self._df.index.get_level_values("Locus").to_list()
        try:
            assert all(locus in original_loci for locus in loci_list)
        except AssertionError:
            logging.error("Not all loci could be found in the haplotype table!")
            # exit(1)
        self._df = self._df[self._df.index.get_level_values("Locus").isin(loci_list)]
        return self

    def filter_locus_completeness(self, min_completeness: float) -> None:
        """
        Minimum proportion of samples with haplotype data in a locus. Loci
        with less data are removed

        Args:
            min_completeness (float): treshold value for the minimum proportion
            of samples with haplotype data

        Returns:
            A dataframe where loci that have less than the minimum
            proportion of samples with haplotype data are removed.
        """

        logging.info("Filtering for locus completeness")
        _, number_of_samples = self._df.shape
        threshold = min_completeness * number_of_samples
        loci = self._df.index.get_level_values("Locus")
        loci_with_enough_data = (
            self._df.groupby(LOCUS_COLUMN_NAME, dropna=False)
            .sum(min_count=1)
            .dropna(thresh=threshold)
            .index.get_level_values("Locus")
        )
        deleted = list(set(loci).difference(loci_with_enough_data))
        if len(deleted) > 0:
            self._df.drop(deleted, level="Locus", inplace=True)
            logging.warning(
                "%s region%s ignored due to a completeness lower than %s",
                len(deleted),
                "s were" if len(deleted) > 1 else " was",
                min_completeness,
            )
        logging.info("Filtering for locus completeness done!")
        return self

    def filter_for_sample_completeness(self, treshold: int):
        """
        This function filters for sample completeness based on a user defined
        treshold for the minimum number of loci with haplotype data in a sample.
        Samples with less data will be removed.

        Args:
            treshold (int): the minimum number of loci with haplotype data in
            a sample.

        Returns:
            A dataframe where the samples are filtered on sample completeness.
        """
        samples = list(self._df.columns)
        samples_to_keep = (
            self._df.groupby(LOCUS_COLUMN_NAME, dropna=False)
            .sum(numeric_only=True, min_count=1)
            .dropna(axis=1, thresh=treshold)
            .columns.tolist()
        )
        deleted = list(set(samples).difference(samples_to_keep))
        self._df.drop(deleted, axis=1, inplace=True)
        self.samples = self._df.columns.tolist()
        return self


# def create_dosage_matrix(file_location: Path):
#     logging.info("Reading dosage matrix")
#     df = (
#         pd.read_csv(file_location, sep="\t", parse_dates=False, dtype=str, header=0)
#         .set_index(INDEX_COLUMNS)
#         .apply(pd.to_numeric, errors="raise")
#     )
#     dosage_matrix = DosageMatrix(df)
#     logging.info("Reading dosage matrix finished")
#     return dosage_matrix


class Pairwise(DosageMatrixExtended):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)
        # self.samples = self._df.columns.to_list()

    # @classmethod
    # def convert_dosage_matrix(cls, dosage_matrix: DataFrame):
    #     dosage_matrix._df[dosage_matrix._df > 0] = 1
    #     return cls(dosage_matrix._df)

    # def order_and_pool_samples(self, samples):
    #     try:
    #         with open(samples, "r") as file:
    #             IDs = dict(line.strip().split(maxsplit=1) for line in file)
    #     except ValueError:
    #         logging.warning(
    #             "No new sample IDs or groups where provided, "
    #             "continuing with samples only"
    #         )
    #         with open(samples, "r") as file:
    #             samples_list = [line.strip().split()[0] for line in file]
    #             IDs = {sample: sample for sample in samples_list}

    #     """
    #     Pool samples if specified in the samples file. Rename samples in the
    #     haplotypes table.
    #     """
    #     try:
    #         assert len(list(set(IDs.keys()) - set(list(self._df.columns)))) == 0
    #     except AssertionError:
    #         missing = list(set(IDs.keys()) - set(list(self._df.columns)))
    #         logging.error(
    #             f"Samples {missing} could not be found in the input table."
    #             "\nPlease check your samples file."
    #         )
    #         sys.exit("Terminating SMAP GRM")
    #     for sample, ID in IDs.items():
    #         if ID:
    #             pool = [s for s in IDs if IDs[s] == ID]
    #             if len(pool) > 1 and ID not in self._df.columns:
    #                 # Pool samples with the same sample ID.
    #                 logging.info(
    #                     f"The samples {', '.join(pool[:-1])} and {pool[-1]} "
    #                     f"were combined into one sample with ID {ID}."
    #                 )
    #                 self._df[ID] = (
    #                     self._df.loc[:, pool]
    #                     .astype(float)
    #                     .sum(axis=1, numeric_only=True, min_count=1)
    #                 )
    #                 self._df.drop(pool, axis=1, inplace=True)
    #             else:
    #                 # Rename samples if a new ID is specified.
    #                 self._df.rename(columns={sample: ID}, inplace=True)
    #     """
    #     Reorder the columns in the dataframe based on the order of the samples
    #     in IDs.
    #     """
    #     order = list()
    #     for sample, ID in IDs.items():
    #         if ID:
    #             if ID not in order:
    #                 order.append(ID)
    #         else:
    #             order.append(sample)
    #     self._df = self._df[order]
    #     self._df[self._df > 0] = 1
    #     self.samples = self._df.columns.tolist()
    #     return self

    # def subset_loci(self, loci: Path):
    #     with open(loci, "r") as file:
    #         loci_list = [locus.strip() for locus in file]
    #     original_loci = self._df.index.get_level_values("Locus").to_list()
    #     try:
    #         assert all(locus in original_loci for locus in loci_list)
    #     except AssertionError:
    #         logging.error("Not all loci could be found in the haplotype table!")
    #         # exit(1)
    #     self._df = self._df[self._df.index.get_level_values("Locus").isin(loci_list)]
    #     return self

    # def filter_locus_completeness(self, min_completeness: float) -> None:
    #     """
    #     Minimum proportion of samples with haplotype data in a locus. Loci
    #     with less data are removed

    #     Args:
    #         min_completeness (float): treshold value for the minimum proportion
    #         of samples with haplotype data

    #     Returns:
    #         A dataframe where loci that have less than the minimum
    #         proportion of samples with haplotype data are removed.
    #     """

    #     logging.info("Filtering for locus completeness")
    #     _, number_of_samples = self._df.shape
    #     threshold = min_completeness * number_of_samples
    #     loci = self._df.index.get_level_values("Locus")
    #     loci_with_enough_data = (
    #         self._df.groupby(LOCUS_COLUMN_NAME, dropna=False)
    #         .sum(min_count=1)
    #         .dropna(thresh=threshold)
    #         .index.get_level_values("Locus")
    #     )
    #     deleted = list(set(loci).difference(loci_with_enough_data))
    #     if len(deleted) > 0:
    #         self._df.drop(deleted, level="Locus", inplace=True)
    #         logging.warning(
    #             "%s region%s ignored due to a completeness lower than %s",
    #             len(deleted),
    #             "s were" if len(deleted) > 1 else " was",
    #             min_completeness,
    #         )
    #     logging.info("Filtering for locus completeness done!")
    #     return self

    # def filter_for_sample_completeness(self, treshold: int):
    #     """
    #     This function filters for sample completeness based on a user defined
    #     treshold for the minimum number of loci with haplotype data in a sample.
    #     Samples with less data will be removed.

    #     Args:
    #         treshold (int): the minimum number of loci with haplotype data in
    #         a sample.

    #     Returns:
    #         A dataframe where the samples are filtered on sample completeness.
    #     """
    #     samples = list(self._df.columns)
    #     samples_to_keep = (
    #         self._df.groupby(LOCUS_COLUMN_NAME, dropna=False)
    #         .sum(numeric_only=True, min_count=1)
    #         .dropna(axis=1, thresh=treshold)
    #         .columns.tolist()
    #     )
    #     deleted = list(set(samples).difference(samples_to_keep))
    #     self._df.drop(deleted, axis=1, inplace=True)
    #     self.samples = self._df.columns.tolist()
    #     return self

    def compare_haplotypes(self, sample_pair):

        compl_dup = {}
        partial_dup = {}
        s1, s2 = sample_pair
        t_df = self._df[[s1, s2]]
        # t_df = self._df[[s1, s2]].sort_values(by="Locus", key=natsort_keygen())

        # compl_dup = pd.DataFrame(columns=[s1, s2])
        # partial_dup = pd.DataFrame(columns=[s1, s2])
        t_df = t_df.assign(test=np.where(t_df[s1] == t_df[s2], True, False))
        l1 = t_df["test"].groupby(level="Locus", sort=False).all().astype(int)
        t_df = self._df[[s1, s2]].replace(0, np.nan)
        t_df = t_df.assign(test=np.where(t_df[s1] == t_df[s2], True, False))
        l2 = t_df["test"].groupby(level="Locus", sort=False).any().astype(int)
        compl_dup = l1.to_numpy()
        partial_dup = l2.to_numpy()

        return compl_dup, partial_dup, s1, s2

    def number_of_comparisons(self) -> pd.DataFrame:
        """
        This functions calculates the total number of sample pairs for which
        the loci were considered.

        Returns:
            pd.DataFrame: A dataframe with the column TotalCombinations which
            has the number of total possible sample combinations for which the
            loci where compared to determine if they were informative.
        """
        df = self._df.copy()
        df = df.replace(0, 1)
        n = df.sum(axis=1).groupby(level="Locus", sort=False).mean()
        nminus1 = n - 1
        combs = pd.DataFrame((n * nminus1) / 2, columns=["TotalCombinations"])
        return combs

    def determine_informative_loci(self, processes):
        """
        This functions finds haplotypes that occure only in one sample in a set of samples.
        This is done by checking if the sum of the observations is one. Then it searches
        for which samples this value was 1.
        """
        logging.info("Determining informative loci")
        self._df = self._df.sort_values(by="Locus", key=natsort_keygen())
        loci = natsorted(list(set(self._df.index.get_level_values("Locus"))))
        sum_complete_uniq = pd.DataFrame(0, columns=["sum"], index=loci)
        # self.partial_dups= #keys from list
        # self.complete_dups =
        sum_complete_uniq.index.name = "Locus"

        sample_pairs = combinations(self._df.columns, r=2)

        # Calculate number of comparisons
        total_combs = self.number_of_comparisons().sort_values(
            by="Locus", key=natsort_keygen()
        )
        # Create dataframes and fill with 0 to avoid NA when merging
        self.complete_u_combs = pd.DataFrame(0, index=loci, columns=["CompleteUniq"])
        # self.p_sh_combs = pd.DataFrame(0, index=loci, columns=['PartialShared'])
        self.p_un_combs = pd.DataFrame(0, index=loci, columns=["PartialUniq"])
        self.c_sh_combs = pd.DataFrame(0, index=loci, columns=["CompleteShared"])

        a = np.empty(len(loci))
        a.fill(0)
        dict_inf_loci_complete = {s: a for s in self._df.columns}
        dict_inf_loci_complete["Locus"] = loci
        dict_inf_loci_partial = {s: a for s in self._df.columns}
        dict_inf_loci_partial["Locus"] = loci
        total = (len(self._df.columns) * (len(self._df.columns) - 1)) / 2

        pbar = tqdm(total=total, position=1, leave=True)
        # self._df = self._df.sort_values(by="Locus", key=natsort_keygen())

        with Pool(processes) as pool:
            for result in pool.imap_unordered(
                self.compare_haplotypes, sample_pairs, chunksize=1500
            ):
                list1, list2, s1, s2 = result
                dict_inf_loci_complete[s1] = np.add(dict_inf_loci_complete[s1], list1)
                dict_inf_loci_complete[s2] = np.add(dict_inf_loci_complete[s2], list1)
                dict_inf_loci_partial[s1] = np.add(dict_inf_loci_partial[s1], list2)
                dict_inf_loci_partial[s2] = np.add(dict_inf_loci_partial[s2], list2)
                pbar.update()

        # Convert the result for the partial duplicate haplotopes in a dataframe
        list_df1 = pd.DataFrame(dict_inf_loci_partial).set_index("Locus")
        list_df1 = list_df1.sort_values(by="Locus", key=natsort_keygen())

        p_sh_combs = pd.DataFrame(index=loci)
        # Calculate combs
        p_sh_combs["PartialShared"] = list_df1.sum(axis=1) / 2
        self.p_sh_combs = p_sh_combs

        self.samples_n_compl_unique_haps = list_df1

        # Convert the result for the complete duplicate haplotopes in a dataframe
        list_df2 = pd.DataFrame(dict_inf_loci_complete).set_index("Locus")
        list_df2 = list_df2.sort_values(by="Locus", key=natsort_keygen())

        # Calculate combs
        c_sh_combs = pd.DataFrame(index=loci, columns=["CompleteShared"])
        c_sh_combs["CompleteShared"] = list_df2.sum(axis=1) / 2
        self.c_sh_combs = c_sh_combs
        self.samples_n_part_unique_haps = list_df2
        # del c_sh_combs, p_sh_combs, list_df1, list_df2, empty_df
        # gc.collect()

        self.complete_u_combs["CompleteUniq"] = (
            total_combs["TotalCombinations"] - self.p_sh_combs["PartialShared"]
        )
        self.p_un_combs["PartialUniq"] = (
            total_combs["TotalCombinations"] - self.c_sh_combs["CompleteShared"]
        )

        # Find unique haplotype
        """
        When a locus is never partially shared for a sample, it contains a unique
        haplotype (set) only occuring in that sample. In that case, the sum is 0"""
        coords = (
            self.samples_n_compl_unique_haps.where(
                self.samples_n_compl_unique_haps.eq(0)
            )
            .stack()
            .index.tolist()
        )
        uniques = {}
        idx = pd.IndexSlice
        remove = []

        # We need to avoid that there is missing data for a locus for a sample.
        # These loci should not be used to look for samples with unique haplotypes
        for index, column in coords:
            hh = self._df.loc[idx[:, index, :]]
            if not hh[column].isnull().values.any():
                zz = list(
                    set(hh.loc[hh[column] == 1].index.get_level_values("Haplotypes"))
                )
                uniques.setdefault(index, []).append({column: zz})
            else:
                remove.append(index)

        for key in remove:
            uniques.pop(key, None)

        # Convert the list of dictionaries to a more readable string
        mapping_table = str.maketrans({"'": "", "{": "", "}": ""})
        for locus, z in uniques.items():
            n_string = []
            for i in z:
                n_string.append(str(i).translate(mapping_table))
            uniques[locus] = "; ".join(n_string)
        uniques_df = pd.Series(uniques, dtype="object").to_frame()
        uniques_df = uniques_df.rename({0: "SamplesWithUniqHaplotypes"}, axis="columns")

        # Find unique combinations of haplotypes for a locus

        coords = (
            self.samples_n_part_unique_haps.where(self.samples_n_part_unique_haps.eq(0))
            .stack()
            .index.tolist()
        )

        part_uniques = {}
        idx = pd.IndexSlice
        remove = []
        for index, column in coords:
            # hh = self._df.loc[(self._df.index.get_level_values(index)[column] == 1)]
            hh = self._df.loc[idx[:, index, :]]
            if not hh[column].isnull().values.any():
                zz = list(
                    set(hh.loc[hh[column] == 1].index.get_level_values("Haplotypes"))
                )
                part_uniques.setdefault(index, []).append({column: zz})
            else:
                remove.append(index)

        for key in remove:
            part_uniques.pop(key, None)

        for locus, z in part_uniques.items():
            n_string = []
            for i in z:
                n_string.append(str(i).translate(mapping_table))
            part_uniques[locus] = "; ".join(n_string)
        part_uniques_df = pd.Series(part_uniques, dtype="object").to_frame()
        part_uniques_df = part_uniques_df.rename(
            {0: "SamplesWithUniqCombHaplotypes"}, axis="columns"
        )
        prop_complete_uniq = pd.DataFrame(index=loci, columns=["PropCompleteUniq"])
        prop_complete_uniq["PropCompleteUniq"] = (
            self.complete_u_combs["CompleteUniq"] / total_combs["TotalCombinations"]
        )

        prop_partial_uniq = pd.DataFrame(index=loci, columns=["PropPartialUniq"])
        prop_partial_uniq["PropPartialUniq"] = (
            self.p_un_combs["PartialUniq"] / total_combs["TotalCombinations"]
        )

        prop_complete_shared = pd.DataFrame(index=loci, columns=["PropCompleteShared"])
        prop_complete_shared["PropCompleteShared"] = (
            self.c_sh_combs["CompleteShared"] / total_combs["TotalCombinations"]
        )

        prop_partial_shared = pd.DataFrame(index=loci, columns=["PropPartialShared"])
        prop_partial_shared["PropPartialShared"] = (
            self.p_sh_combs["PartialShared"] / total_combs["TotalCombinations"]
        )

        dfs_to_m = [
            total_combs,
            self.complete_u_combs,
            prop_complete_uniq,
            uniques_df,
            self.p_un_combs,
            prop_partial_uniq,
            part_uniques_df,
            self.c_sh_combs,
            prop_complete_shared,
            self.p_sh_combs,
            prop_partial_shared,
        ]
        inf_loci = pd.concat(dfs_to_m, axis=1)
        inf_loci.index.names = ["Locus"]
        inf_loci = inf_loci.sort_values(by="Locus", key=natsort_keygen())
        logging.info("Determining informative loci finished")

        return inf_loci

    def create_relatedness_df(self, processes) -> pd.DataFrame:
        df = pd.DataFrame(
            columns=[
                "s1",
                "s2",
                "shared_loci",
                "n_shared_haplotypes",
                "partial_shared",
                "partial_shared_p",
                "partial_unique",
                "partial_unique_p",
                "complete_shared",
                "complete_shared_p",
                "complete_unique",
                "complete_unique_p",
                "n_unique_haps_s1",
                "n_unique_haps_s2",
                "Jaccard",
                "Sorensen-Dice",
                "Ochiai",
            ]
        )
        samples = self._df.columns.tolist()

        pbar = tqdm(
            total=sum(1 for ignore in combinations_with_replacement(samples, 2)),
            position=1,
            leave=True,
        )
        combs = combinations_with_replacement(samples, 2)
        list_df = []
        with Pool(processes) as pool:
            for result in pool.imap_unordered(
                self.calculate_relatedness_between_sample_pair, combs, chunksize=600
            ):
                list_df.append(result)
                pbar.update()
        df = pd.DataFrame.from_dict(list_df)

        return df

    def calculate_relatedness_between_sample_pair(self, combs) -> dict:
        s1, s2 = combs
        t_df = self._df[[s1, s2]]
        locus_present = t_df.query(
            f"(1 == `{s1}` or 1 == `{s2}`) and (`{s1}` == `{s1}`) and (`{s2}` == `{s2}`)",
            engine="numexpr",
        )
        shared_loci = list(set(locus_present.index.get_level_values("Locus")))
        shared_haplotypes = t_df.query(
            f"(1 == `{s1}` and 1 == `{s2}`)", engine="numexpr"
        )
        n_shared_haplotypes = len(shared_haplotypes)
        partial_shared = list(set(shared_haplotypes.index.get_level_values("Locus")))
        partial_shared_p = len(partial_shared) / len(shared_loci)
        partial_unique = t_df.query(
            f"(0 == `{s1}` and 1 == `{s2}`) or (1 == `{s1}` and 0 == `{s2}`)",
            engine="numexpr",
        )
        partial_unique = list(set(partial_unique.index.get_level_values("Locus")))
        partial_unique_p = len(partial_unique) / len(shared_loci)
        complete_shared = list(set(partial_shared).difference(partial_unique))
        complete_shared_p = len(complete_shared) / len(shared_loci)
        complete_unique = list(set(partial_unique).difference(partial_shared))
        complete_unique_p = len(complete_unique) / len(shared_loci)
        unique_s1 = t_df.query(f"(1 == `{s1}` and 0 == `{s2}`)", engine="numexpr")
        n_unique_haps_s1 = len(unique_s1)
        unique_s2 = t_df.query(f"(1 == `{s2}` and 0 == `{s1}`)", engine="numexpr")
        n_unique_haps_s2 = len(unique_s2)
        if n_shared_haplotypes > 0 or n_unique_haps_s1 > 0 or n_unique_haps_s2 > 0:
            jaccard = n_shared_haplotypes / (
                n_shared_haplotypes + n_unique_haps_s1 + n_unique_haps_s2
            )
            sorensen_dice = (2 * n_shared_haplotypes) / (
                (2 * n_shared_haplotypes) + n_unique_haps_s1 + n_unique_haps_s2
            )
            ochiai = n_shared_haplotypes / math.sqrt(
                (n_shared_haplotypes + n_unique_haps_s1)
                * (n_shared_haplotypes + n_unique_haps_s2)
            )
        else:
            jaccard = pd.NA
            sorensen_dice = pd.NA
            ochiai = pd.NA
        # Define the new row to be added
        new_row = {
            "s1": s1,
            "s2": s2,
            "shared_loci": len(shared_loci),
            "n_shared_haplotypes": n_shared_haplotypes,
            "partial_shared": len(partial_shared),
            "partial_shared_p": partial_shared_p,
            "partial_unique": len(partial_unique),
            "partial_unique_p": partial_unique_p,
            "complete_shared": len(complete_shared),
            "complete_shared_p": complete_shared_p,
            "complete_unique": len(complete_unique),
            "complete_unique_p": complete_unique_p,
            "n_unique_haps_s1": n_unique_haps_s1,
            "n_unique_haps_s2": n_unique_haps_s2,
            "Jaccard": jaccard,
            "Sorensen-Dice": sorensen_dice,
            "Ochiai": ochiai,
        }
        return new_row


class UMAP:
    def __init__(
        self,
        df: DataFrame,
        clustering_method: str,
    ):
        self.df = df
        self.clustering_method = clustering_method

    def calculate(self):
        dataset_cp = self.df
        dataset_cp.index = dataset_cp.index.map("_".join)
        dataset_tr = dataset_cp.transpose()

        # data_matrix = np.nan_to_num(dataset_p.loc[:,genenames].to_numpy(), nan=0.0)
        # dataset_p._df.index = dataset_p._df.index.map('_'.join)
        data_matrix = np.nan_to_num(dataset_tr.loc[:].to_numpy(), nan=0.0)
        # data_matrix_tr = data_matrix.transpose()

        vars = list(dataset_tr.columns)
        samples = list(dataset_tr.index)
        adata = sc.AnnData(X=data_matrix, obs=samples, var=vars)
        adata.var_names = vars

        sc.tl.pca(adata)
        sc.pp.neighbors(adata, n_neighbors=10, n_pcs=30)

        sc.tl.umap(adata)

        sc.pl.umap(adata)

        sc.tl.leiden(adata, flavor="igraph", n_iterations=-1)
        sc.tl.leiden(adata, flavor="igraph", n_iterations=-1)
        sc.pl.umap(adata, color=[self.clustering_method], save="test.png")

        # Convert the UMAP coordinates to a DataFrame for easy plotting
        umap_df = adata.obsm["X_umap"]
        # test = adata.to_df()
        umap_df = pd.DataFrame(umap_df, columns=["UMAP1", "UMAP2"])
        umap_df["id"] = list(adata.obs.index)
        umap_df.index = umap_df["id"]
        umap_df = pd.concat([umap_df, adata.obs], axis=1)
        return umap_df

        umap_df.to_csv("umap_result_df.tsv", sep="\t")

        fig = px.scatter(umap_df, x="UMAP1", y="UMAP2", color="leiden", hover_data=[0])
        fig.update_traces(marker=dict(size=5), selector=dict(mode="markers"))
        fig.write_html("test.html")


class WriteMatrixOutput:
    def __init__(
        self,
        df: DataFrame,
        samples: List,
        mask: Union[None, str],
        prefix: str,
        output_dir,
    ) -> None:
        self.df = df
        self.samples = samples
        self.mask = mask
        self.prefix = prefix
        self.output_dir = output_dir + "/"
        print(self.output_dir)

    def matrix(self, column):
        matrix = self.df.pivot(values=column, index="s2", columns="s1")
        matrix = matrix.reindex(self.samples, axis=0)
        matrix = matrix.reindex(self.samples, axis=1)
        if not self.mask:
            matrix = matrix.combine_first(matrix.T)
        if self.mask == "upper":
            matrix = matrix.T
        return matrix

    def calc_clustered_matrix(self, column):
        matrix = self.matrix(column)
        matrix = matrix.combine_first(matrix.T)
        X = matrix.corr().values
        d = sch.distance.pdist(X)  # vector of ('55' choose 2) pairwise distances
        L = sch.linkage(d, method="ward")
        ind = sch.fcluster(L, 0.5 * d.max(), "distance")
        columns = [matrix.columns.tolist()[i] for i in list((np.argsort(ind)))]
        clustered_matrix = matrix.reindex(index=columns, columns=columns)
        return clustered_matrix

    def plot_heatmap(self, matrix, filename, title):
        height = len(self.samples) * 0.5
        width = len(self.samples) * 0.6
        if width > 150:
            width = 150
            height = 150 * 0.9
        fig, ax = plt.subplots(1, 1, figsize=(width, height), dpi=300)
        sns.heatmap(matrix, annot=True, fmt=".2f")
        ax.set_ylabel("")
        ax.set_xlabel("")
        plt.title(title)
        plt.yticks(rotation=0)
        plt.xticks(rotation=0)
        fig.savefig(filename)

    def interactive_heatmap(self, matrix, filename):
        pfig = px.imshow(
            matrix, text_auto=True, color_continuous_scale="matter", aspect="auto"
        )
        pfig.write_html(filename)

    def similarity(self, column, filetype):
        matrix = self.matrix(column)
        # fig = heatm.get_figure()
        # filename = self.prefix + column + '.' + filetype

        if len(self.samples) <= 500:
            filename = self.output_dir + self.prefix + column + "." + filetype
            title = column.replace("_p", "").replace("_", " ")
            self.plot_heatmap(matrix, filename, title)
        elif len(self.samples) > 500:
            logging.warning(
                """You have more then 500 samples to be plotted.
                            Switching to interactive plot"""
            )
            filename = self.output_dir + self.prefix + column + "." + "html"
            self.interactive_heatmap(matrix, filename)
        txtfile = self.output_dir + self.prefix + column + "_matrix.txt"
        matrix.to_csv(txtfile, sep="\t")

    def clustered_similarity(self, column, filetype):
        clustered_matrix = self.calc_clustered_matrix(column)
        clustered_matrix.to_csv("test.txt", sep="\t")
        filename = self.output_dir + self.prefix + column + "_clustered." + "html"
        self.interactive_heatmap(clustered_matrix, filename)

    def distance(self, distance, filetype):
        matrix = self.matrix(distance)
        filename = self.output_dir + self.prefix + distance + "." + filetype
        if len(self.samples) <= 500:
            self.plot_heatmap(matrix, filename, "Jaccard distance (JD)")
        txtfile = self.output_dir + self.prefix + distance + "_matrix.txt"
        matrix.to_csv(txtfile, sep="\t")

    def inversed_distance(self, distance, filetype):
        dist_matrix = 1 - self.matrix(distance)
        filename = self.output_dir + self.prefix + distance + "." + filetype
        if len(self.samples) <= 500:
            self.plot_heatmap(dist_matrix, filename, "Jaccard inversed distance (JID)")
        txtfile = self.output_dir + self.prefix + distance + "inversed_matrix.txt"
        dist_matrix.to_csv(txtfile, sep="\t")

    def to_excel(self, column):
        """
        This functions writes all the possible output to an excel file
        with seperate sheets for each matrix
        """
        matrix = self.matrix(column)
        with pd.ExcelWriter(
            self.output_dir + self.prefix + "pairwise.xlsx",
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
        ) as writer:
            matrix.to_excel(writer, sheet_name=column)


def subset_loci(loci: Path, matrix: DataFrame):
    with open(loci, "r") as file:
        loci_list = [locus.strip() for locus in file]
    original_loci = matrix._df.index.get_level_values("Locus").to_list()
    try:
        assert all(locus in original_loci for locus in loci_list)
    except AssertionError:
        logging.error("Not all loci could be found in the haplotype table!")
        # exit(1)
    table = matrix[matrix._df.index.get_level_values("Locus").isin(loci_list)]
    return table


def convert_to_preferred_format(sec):
    """
    This function converts the measured runtime to a human readable format
    in hours, minutes, seconds

    Args:
        sec (int): the elapsed time in seconds

    Returns:
        string: strig the the execution runtime
    """
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60

    return "%02d:%02d:%02d" % (hour, min, sec)


def main(args=None) -> None:
    # if args is None:
    #     args = sys.argv
    start = timer()
    parsed_args = parse_args(args)
    prefix = parsed_args.prefix
    processes = parsed_args.processes
    if "/" not in parsed_args.output_directory and parsed_args.output_directory != ".":
        output_dir = os.getcwd() + "/" + parsed_args.output_directory
    else:
        output_dir = os.path.abspath(parsed_args.output_directory)
    os.makedirs(output_dir, exist_ok=True)
    t = DosageMatrixExtended.read_dosage_matrix(parsed_args.table)
    logging.info("Creating observation matrix")
    obs_matrix = t.convert_dosage_matrix()
    logging.info("Creating observation matrix finished")

    # Remove loci with a higher percentage of missing data than allowed by the locus completeness.
    logging.info(
        "Removing loci with a higher percentage of missing data than allowed by the locus completeness."
    )
    t = obs_matrix.filter_locus_completeness(parsed_args.locus_completeness)
    logging.info(
        "Removing loci with a higher percentage of missing data than allowed by the locus completeness finished"
    )

    if parsed_args.samples:
        t = t.order_and_pool_samples(parsed_args.samples)

    if parsed_args.loci:
        t = t.subset_loci(parsed_args.loci)

    # Remove samples with more missing data than allowed by the sample completeness.
    logging.info(
        "Removing samples with more missing data than allowed by the sample completeness."
    )
    obs_matrix = t.filter_for_sample_completeness(parsed_args.sample_completeness)
    logging.info(
        "Removing samples with more missing data than allowed by the sample completeness finished"
    )

    if parsed_args.command == "umap":
        umap_df = UMAP(obs_matrix._df, parsed_args.clustering).calculate()
        umap_df.to_csv("umap_result_df.tsv", sep="\t")
        fig = px.scatter(
            umap_df, x="UMAP1", y="UMAP2", color=parsed_args.clustering, hover_data=[0]
        )
        fig.update_traces(marker=dict(size=5), selector=dict(mode="markers"))
        fig.write_html("test.html")

    elif parsed_args.command == "pairwise":
        logging.info("Creating relatedness df")
        samples = obs_matrix.samples
        pairwise = Pairwise(obs_matrix._df)
        df = pairwise.create_relatedness_df(processes)
        logging.info("Creating relatedness df finished")
        df.to_csv(
            output_dir + "/" + prefix + "relatedness_table_per_sample_pair.csv",
            sep="\t",
            index=False,
        )

        if parsed_args.informative_loci:
            inf_loci = pairwise.determine_informative_loci(processes)
            inf_loci.to_csv(
                output_dir + "/" + prefix + "informative_loci.csv", sep="\t", index=True
            )

        options = [
            "partial_unique_p",
            "partial_shared_p",
            "complete_unique_p",
            "complete_shared_p",
        ]

        filetype = parsed_args.plot_format
        mask = parsed_args.mask
        if mask == "none":
            mask = None

        output = WriteMatrixOutput(df, samples, mask, prefix, output_dir)

        for option in options:
            output.similarity(option, filetype)
            output.clustered_similarity(option, filetype)

        if parsed_args.excel:
            dfx = pd.DataFrame()
            dfx.to_excel(prefix + "pairwise.xlsx")
            for option in options:
                output.to_excel(option)

        distances = ["Jaccard", "Sorensen-Dice", "Ochiai"]
        if parsed_args.distance == "i":
            for option in distances:
                output.inversed_distance(option, filetype)
        elif parsed_args.distance == "d":
            for option in distances:
                output.distance(option, filetype)

    end = timer()
    total = end - start
    readible_time = convert_to_preferred_format(total)
    logging.info(
        f"Execution time SMAP relatedness {parsed_args.command}: {readible_time}"
    )


if __name__ == "__main__":
    main()
