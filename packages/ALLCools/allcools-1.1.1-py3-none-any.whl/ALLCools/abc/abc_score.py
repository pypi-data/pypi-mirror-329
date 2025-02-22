import pathlib
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

import cooler
import numpy as np
import pandas as pd
import pyBigWig


def _activity_score_atac_mcg(all_values):
    activity_score = all_values["ATAC"] * (1 - all_values["mCG"])
    return activity_score


def _scan_single_bw(bw_path, bed, value_type="sum"):
    with pyBigWig.open(bw_path) as bw:
        bw_values = []
        for _, (chrom, start, end, *_) in bed.iterrows():
            v = bw.stats(chrom, start, end, type=value_type)[0]
            v = 0 if v is None else v
            bw_values.append(v)
        bw_values = np.array(bw_values)
    return bw_values


def _preprocess_bed(input_bed, blacklist_path, chrom_sizes, temp_dir):
    # sort and save to temp_dir
    bed_name = pathlib.Path(input_bed).name
    if bed_name.endswith(".gz"):
        bed_name = bed_name[:-3]
    new_path = f"{temp_dir}/{bed_name}"
    bed = pd.read_csv(input_bed, sep="\t", index_col=None, header=None)
    # sort bed
    bed = bed.sort_values([0, 1])
    bed = bed[bed[0].isin(chrom_sizes.index)]
    bed.to_csv(new_path, sep="\t", index=None, header=None)

    # remove blacklist
    if blacklist_path is not None:
        after_remove_path = f"{new_path}.remove_blacklist.bed"
        subprocess.run(
            f"bedtools intersect -a {new_path} -b {blacklist_path} -v > {after_remove_path}", shell=True, check=True
        )
        subprocess.run(f"mv -f {after_remove_path} {new_path}", shell=True, check=True)
    return new_path


class ABCModel:
    """Calculate ABC score between promoter and enhancer."""

    def __init__(
        self,
        cool_url,
        enhancer_bed_path,
        tss_bed_path,
        output_prefix,
        epi_mark: dict,
        calculation_mode,
        blacklist_path=None,
        enhancer_size=500,
        promoter_size=500,
        max_dist=5000000,
        min_score_cutoff=0.02,
        balance=False,
        cleanup=True,
        cpu=1,
    ):
        if calculation_mode == "ATAC-mCG":
            self.activity_score_func = _activity_score_atac_mcg
        else:
            raise NotImplementedError

        self.clr = cooler.Cooler(cool_url)
        self.enhancer_bed_path = enhancer_bed_path
        self.tss_bed_path = tss_bed_path
        self.blacklist_path = blacklist_path
        self.epi_mark = epi_mark
        self.output_prefix = output_prefix
        self.temp_dir = f"{output_prefix}_temp"
        pathlib.Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

        # cool sizes
        self.bin_size = self.clr.binsize
        self.chrom_names = self.clr.chromnames.copy()
        self.chrom_sizes = self.clr.chromsizes.copy()
        self.chrom_sizes_path = f"{self.temp_dir}/chrom_sizes.txt"
        self.chrom_sizes.to_csv(self.chrom_sizes_path, header=None, sep="\t")

        self.min_score_cutoff = min_score_cutoff
        self.max_dist = max_dist
        self.enhancer_slop = enhancer_size // 2
        self.promoter_slop = promoter_size // 2

        self.enhancer_bed = self._enhancer_bed()
        self.tss_bed = self._tss_bed()
        self.tss_ids = set(self.tss_bed["id"].tolist())
        self.tss_bin = self._tss_bin()
        self.promoter_bed = self._promoter_bed()

        # promoter and enhancer bed
        self.pe_bed = self._promoter_and_enhancer_bed()

        # calculate
        self.results = self.calculate(balance=balance, cpu=cpu)

        if cleanup:
            subprocess.run(f"rm -rf {self.temp_dir}", shell=True)
        return

    def _enhancer_bed(self):
        self.enhancer_bed_path = _preprocess_bed(
            input_bed=self.enhancer_bed_path,
            blacklist_path=self.blacklist_path,
            chrom_sizes=self.chrom_sizes,
            temp_dir=self.temp_dir,
        )
        enhancer_bed = pd.read_csv(
            self.enhancer_bed_path, sep="\t", index_col=None, header=None, names=["chrom", "start", "end", "id"]
        )
        # filter chrom
        enhancer_bed = enhancer_bed[enhancer_bed["chrom"].isin(self.chrom_names)].copy()

        # standard size
        enhancer_bed = self._standard_bed(enhancer_bed, name="enhancer", slop=self.enhancer_slop)
        return enhancer_bed

    def _tss_bed(self):
        self.tss_bed_path = _preprocess_bed(
            input_bed=self.tss_bed_path,
            blacklist_path=self.blacklist_path,
            chrom_sizes=self.chrom_sizes,
            temp_dir=self.temp_dir,
        )
        tss_bed = pd.read_csv(
            self.tss_bed_path, header=None, index_col=None, sep="\t", names=["chrom", "start", "end", "id"]
        )

        # filter chrom
        tss_bed = tss_bed[tss_bed["chrom"].isin(self.chrom_names)].copy()
        return tss_bed

    def _tss_bin(self):
        # tss bin bed
        bin_size = self.bin_size
        tss_bin = self.tss_bed.copy()
        tss_bin["start"] = tss_bin["start"] // bin_size * bin_size
        tss_bin["end"] = (tss_bin["end"] // bin_size + 1) * bin_size
        # prevent last bin error
        tss_bin["end"] = tss_bin.apply(lambda i: min(self.chrom_sizes[i["chrom"]], i["end"]), axis=1)
        # merge TSS within the same bin
        records = []
        for (chrom, start, end), sub_df in tss_bin.groupby(["chrom", "start", "end"]):
            records.append([chrom, start, end, ",".join(sub_df["id"])])
        tss_bin = pd.DataFrame(records, columns=["chrom", "start", "end", "id"])
        return tss_bin

    def _promoter_bed(self):
        # standard size promoter
        promoter_bed = self._standard_bed(self.tss_bed, name="promoter", slop=self.promoter_slop)
        return promoter_bed

    def _promoter_and_enhancer_bed(self):
        temp_dir = self.temp_dir

        # concat enhancer and tss
        pe_bed = pd.concat([self.enhancer_bed, self.promoter_bed]).sort_values(["chrom", "start"])
        if pe_bed["id"].duplicated().sum() > 0:
            raise ValueError("enhancer and TSS ids have duplicates.")
        pe_bed.to_csv(f"{temp_dir}/enhancer_and_tss.bed", index=False, header=False, sep="\t")

        # merge regions
        merge_cmd = (
            f"bedtools merge -c 4 -o collapse "
            f"-i {temp_dir}/enhancer_and_tss.bed > "
            f"{temp_dir}/enhancer_and_tss.merge.bed"
        )
        subprocess.run(merge_cmd, shell=True, check=True)

        pe_bed = pd.read_csv(
            f"{temp_dir}/enhancer_and_tss.merge.bed", sep="\t", header=None, names=["chrom", "start", "end", "id"]
        )

        # add bin position
        pe_bed["bin_pos"] = np.round((pe_bed["start"] + pe_bed["end"]) / 2 / self.bin_size).astype(int)
        return pe_bed

    def _standard_bed(self, bed, name, slop):
        temp_dir = self.temp_dir
        bed = bed.copy()

        # standardize bed
        center = ((bed["end"] + bed["start"]) / 2).astype(int)
        bed["start"] = center - 1
        bed["end"] = center

        bed.to_csv(f"{temp_dir}/{name}_center.bed", sep="\t", header=None, index=None)

        subprocess.run(
            f"bedtools slop -b {slop} "
            f"-g {temp_dir}/chrom_sizes.txt "
            f"-i {temp_dir}/{name}_center.bed > "
            f"{temp_dir}/{name}_standard_size.bed",
            shell=True,
            check=True,
        )

        # standard size enhancers
        bed = pd.read_csv(
            f"{temp_dir}/{name}_standard_size.bed",
            sep="\t",
            index_col=None,
            header=None,
            names=["chrom", "start", "end", "id"],
        )
        return bed

    def _single_chrom_activity_score(self, chrom_pe_bed):
        all_values = {}
        for modality, reps in self.epi_mark.items():
            if modality == "mCG":
                value_type = "mean"
            else:
                value_type = "sum"

            modality_values = []
            for bw_path in reps:
                bw_values = _scan_single_bw(bw_path=bw_path, bed=chrom_pe_bed, value_type=value_type)
                modality_values.append(bw_values)
            # mean of reps
            modality_values = np.mean(modality_values, axis=0)
            all_values[modality] = modality_values

        # calculate score
        activity_score = self.activity_score_func(all_values)
        chrom_pe_bed["activity_score"] = activity_score
        return chrom_pe_bed

    def _single_chrom_abc_score(self, chrom_mat, chrom_tss_bin, chrom_pe_bed):
        # add activity score to chrom_pe_bed
        self._single_chrom_activity_score(chrom_pe_bed=chrom_pe_bed)

        # mask diagonal with max closest 4 pixel
        mat = chrom_mat
        for i in range(mat.shape[0]):
            if i + 5 < mat.shape[0]:
                mat[i, i] = mat[i, i + 1 : i + 5].max()
            else:
                mat[i, i] = mat[i, i - 5 : i - 1].max()

        tss_bin = chrom_tss_bin["start"] // self.bin_size
        tss_contacts = np.array([mat[b] for b in tss_bin])

        # calculate raw activity by contact score
        records = []
        # raw_abc_score.shape == [chrom_pe_bed.shape[0], chrom_tss_bed.shape[0]]
        for _, row in chrom_pe_bed.iterrows():
            raw_abc_score = row["activity_score"] * tss_contacts[:, row["bin_pos"]]
            records.append(raw_abc_score)

        # mask by enhancer tss distance
        # dist_mask.shape == [chrom_pe_bed.shape[0], chrom_tss_bed.shape[0]]
        max_bins = self.max_dist // self.bin_size
        dist_mask = np.abs(chrom_pe_bed["bin_pos"].values[:, None] - tss_bin.values[None, :]) < max_bins
        raw_abc_score = np.array(records) * dist_mask

        # chrom abc score
        # abc_score.shape == [chrom_pe_bed.shape[0], chrom_tss_bed.shape[0]]
        abc_score = raw_abc_score / (raw_abc_score.sum(axis=0) + 1e-9)
        abc_score = pd.DataFrame(abc_score, index=chrom_pe_bed["id"], columns=chrom_tss_bin["id"]).unstack()
        abc_score = abc_score[abc_score > self.min_score_cutoff].copy()

        # set index
        enhancer_activities = chrom_pe_bed.set_index("id")["activity_score"]

        ep_records = []
        for (promoter, enhancer), score in abc_score.items():
            enhancer_activity = enhancer_activities[enhancer]
            for e in enhancer.split(","):
                for p in promoter.split(","):
                    if e not in self.tss_ids:
                        ep_records.append([e, p, score, enhancer_activity])
        ep_records = pd.DataFrame(ep_records)
        columns = ["enhancer_id", "tss_id", "ABC_score", "enhancer_activity"]
        if ep_records.shape[0] == 0:
            ep_records = pd.DataFrame([], columns=columns)
        else:
            ep_records.columns = columns
        return ep_records

    def calculate(self, balance=False, cpu=1):
        """Calculate the ABC score."""
        with ProcessPoolExecutor(cpu) as exe:
            futures = {}
            for chrom in self.chrom_names:
                mat = self.clr.matrix(balance=balance).fetch(chrom)
                chrom_tss_bin = self.tss_bin[self.tss_bin["chrom"] == chrom].copy()
                chrom_pe_bed = self.pe_bed[self.pe_bed["chrom"] == chrom].copy()
                if (chrom_tss_bin.shape[0] == 0) or (chrom_pe_bed.shape[0] == 0):
                    continue
                f = exe.submit(
                    self._single_chrom_abc_score, chrom_mat=mat, chrom_tss_bin=chrom_tss_bin, chrom_pe_bed=chrom_pe_bed
                )
                futures[f] = chrom

            total_records = []
            for f in as_completed(futures):
                print(f"{chrom} ABC score finished")
                chrom = futures[f]
                ep_records = f.result()
                mean_enhancer = ep_records["tss_id"].value_counts().mean()
                print(f"{chrom_tss_bin.shape[0]} TSS, {chrom_pe_bed.shape[0]} promoter and enhancers.")
                print(
                    f"{ep_records.shape[0]} valid records, "
                    f"each TSS has {mean_enhancer:.2f} associated enhancers on average.\n"
                )
                total_records.append(ep_records)
            total_records = pd.concat(total_records)

        # make bedpe
        use_enhancer_bed = self.enhancer_bed.set_index("id").loc[total_records["enhancer_id"]].reset_index(drop=True)
        use_tss_bed = self.tss_bed.set_index("id").loc[total_records["tss_id"]].reset_index(drop=True)
        reorder_records = total_records[["ABC_score", "enhancer_id", "tss_id", "enhancer_activity"]].reset_index(
            drop=True
        )
        bedpe = pd.concat([use_enhancer_bed, use_tss_bed, reorder_records], axis=1)
        bedpe.columns = [
            "enhancer_chrom",
            "enhancer_start",
            "enhancer_end",
            "tss_chrom",
            "tss_start",
            "tss_end",
            "ABC_score",
            "enhancer_id",
            "tss_id",
            "enhancer_activity",
        ]
        output_path = f"{self.output_prefix}.bedpe.gz"
        bedpe.to_csv(output_path, sep="\t", index=False, header=False)
        return bedpe
