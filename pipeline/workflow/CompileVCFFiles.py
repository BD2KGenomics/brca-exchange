import datetime
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from shutil import copy

import luigi
from luigi.util import requires

luigi.auto_namespace(scope=__name__)

from workflow import bayesdel_processing, esp_processing, gnomad_processing, pipeline_common, pipeline_utils
from workflow.pipeline_common import DefaultPipelineTask, clinvar_method_dir, lovd_method_dir, \
    functional_assays_method_dir, data_merging_method_dir, priors_method_dir, priors_filter_method_dir, \
    utilities_method_dir, vr_method_dir

#######################################
# Default Globals / Env / Directories #
#######################################

luigi_dir = os.getcwd()

###############################################
#                   CLINVAR                   #
###############################################

class DownloadLatestClinvarData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.clinvar_file_dir + "/ClinVarFullRelease_00-latest.xml.gz")

    def run(self):
        os.chdir(self.clinvar_file_dir)

        clinvar_data_url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/ClinVarFullRelease_00-latest.xml.gz"
        pipeline_utils.download_file_and_display_progress(clinvar_data_url)


@requires(DownloadLatestClinvarData)
class ConvertLatestClinvarDataToXML(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.clinvar_file_dir + "/ClinVar.xml")

    def run(self):
        os.chdir(clinvar_method_dir)
        genes_opts = [ s for g in self.cfg.gene_metadata['symbol'] for s in ['--gene', g]]

        pipeline_utils.run_process(["python", "filter_clinvar_brca.py", self.input().path,
                                    self.output().path] + genes_opts)

        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertLatestClinvarDataToXML)
class ConvertClinvarXMLToTXT(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.clinvar_file_dir + "/ClinVar.txt")

    def run(self):
        os.chdir(clinvar_method_dir)

        args = ["python", "clinVarParse.py",
                self.input().path,
                "--logs", self.clinvar_file_dir + "/clinvar_xml_to_txt.log",
                "--assembly", "GRCh38"]

        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertClinvarXMLToTXT)
class ConvertClinvarTXTToVCF(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.clinvar_file_dir + "/ClinVar.vcf")

    def run(self):
        os.chdir(data_merging_method_dir)
        args = ["python", "convert_tsv_to_vcf.py", "-i",
                self.input().path, "-o",
                self.output().path, "-s", "ClinVar"]
        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertClinvarTXTToVCF)
class CopyClinvarVCFToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.cfg.output_dir + "/ClinVar.vcf")

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#                     BIC                     #
###############################################


class DownloadBICData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.bic_file_dir + "/bic_brca12.sorted.hg38.vcf")

    def run(self):
        os.chdir(self.bic_file_dir)

        brca1_data_url = "https://brcaexchange.org/backend/downloads/bic_brca12.sorted.hg38.vcf"
        pipeline_utils.download_file_and_display_progress(brca1_data_url)


@requires(DownloadBICData)
class CopyBICOutputToOutputDir(DefaultPipelineTask):

    def output(self):
        return luigi.LocalTarget(self.cfg.output_dir + "/bic_brca12.sorted.hg38.vcf")

    def run(self):
        copy(self.bic_file_dir + "/bic_brca12.sorted.hg38.vcf", self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#                  exLOVD                     #
###############################################


class ExtractDataFromLatestEXLOVD(DefaultPipelineTask):
    dir_name = 'exLOVD'

    def __init__(self):
        super(ExtractDataFromLatestEXLOVD, self).__init__()
        self.ex_lovd_file_dir = os.path.join(self.cfg.file_parent_dir,
                                        ExtractDataFromLatestEXLOVD.dir_name)

    def output(self):
        return {'brca1': luigi.LocalTarget(os.path.join(self.ex_lovd_file_dir, "BRCA1.txt")),
                'brca2': luigi.LocalTarget(os.path.join(self.ex_lovd_file_dir, "BRCA2.txt"))}

    def run(self):
        # calculating host path because we are running a docker within a docker
        ex_lovd_file_dir_host = os.path.join(os.path.dirname(self.cfg.output_dir_host), ExtractDataFromLatestEXLOVD.dir_name)

        os.chdir(lovd_method_dir)

        ex_lovd_data_host_url = "http://hci-exlovd.hci.utah.edu/"

        args = ['bash', 'extract_latest_exlovd.sh', ex_lovd_file_dir_host, "-u", ex_lovd_data_host_url, "-l", "BRCA1",
                "BRCA2", "-o", "/data"]

        pipeline_utils.run_process(args)


@requires(ExtractDataFromLatestEXLOVD)
class ConvertEXLOVDBRCA1ExtractToVCF(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.ex_lovd_file_dir, "exLOVD_brca1.hg19.vcf"))

    def run(self):
        os.chdir(lovd_method_dir)

        args = ["./lovd2vcf.py", "-i", self.ex_lovd_file_dir + "/BRCA1.txt", "-o",
                self.output().path, "-a",
                "exLOVDAnnotation", "-e",
                os.path.join(self.artifacts_dir, "exLOVD_BRCA1_error_variants.txt"),
                "-s", "exLOVD"]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertEXLOVDBRCA1ExtractToVCF)
class ConvertEXLOVDBRCA2ExtractToVCF(DefaultPipelineTask):

    def output(self):
        return luigi.LocalTarget(self.ex_lovd_file_dir + "/exLOVD_brca2.hg19.vcf")

    def run(self):
        os.chdir(lovd_method_dir)

        args = ["./lovd2vcf.py", "-i", self.ex_lovd_file_dir + "/BRCA2.txt", "-o",
                self.output().path, "-a",
                "exLOVDAnnotation", "-e",
                os.path.join(self.artifacts_dir, "exLOVD_BRCA2_error_variants.txt"),
                "-s", "exLOVD"]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertEXLOVDBRCA2ExtractToVCF)
class ConcatenateEXLOVDVCFFiles(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.ex_lovd_file_dir + "/exLOVD_brca12.hg19.vcf")

    def run(self):
        args = ["vcf-concat", self.ex_lovd_file_dir + "/exLOVD_brca1.hg19.vcf",
                self.ex_lovd_file_dir + "/exLOVD_brca2.hg19.vcf"]

        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConcatenateEXLOVDVCFFiles)
class CrossmapConcatenatedEXLOVDData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.ex_lovd_file_dir + "/exLOVD_brca12.hg38.vcf")

    def run(self):
        brca_resources_dir = self.cfg.resources_dir

        args = ["CrossMap.py", "vcf",
                brca_resources_dir + "/hg19ToHg38.over.chain.gz",
                self.input().path,
                brca_resources_dir + "/hg38.fa",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(CrossmapConcatenatedEXLOVDData)
class SortEXLOVDOutput(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(
            self.ex_lovd_file_dir + "/exLOVD_brca12.sorted.hg38.vcf")

    def run(self):
        args = ["vcf-sort", self.input().path]
        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(SortEXLOVDOutput)
class CopyEXLOVDOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(
            self.cfg.output_dir + "/exLOVD_brca12.sorted.hg38.vcf")

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


##############################################
#               sharedLOVD                   #
##############################################


class DownloadLOVDInputFile(DefaultPipelineTask):
    """ Downloads the shared LOVD data

    If the pipeline is run on a machine from which it is not possible to download the data (currently IP based authentication)
    the file can be manually staged in the path of `lovd_data_file`. In this case, the task will not be run.
    """

    lovd_data_file = luigi.Parameter(default='',
                                     description='path, where the shared LOVD data will be stored')

    shared_lovd_data_url = luigi.Parameter(
                                     default='https://databases.lovd.nl/shared/export/',
                                     description='URL to download shared LOVD BRCA data from')


    def output(self):
        if len(str(self.lovd_data_file)) != 0:
            return luigi.LocalTarget(str(luigi.LocalTarget(str(self.lovd_data_file))))
        else:
            output = {}

            for symbol in pipeline_utils.get_lovd_symbols(self.cfg.gene_metadata['symbol']):
                output[symbol] = luigi.LocalTarget(self.lovd_file_dir + f"/{symbol}.txt")

            return output

    def run(self):
        for symbol in pipeline_utils.get_lovd_symbols(self.cfg.gene_metadata['symbol']):
            pipeline_utils.create_path_if_nonexistent(
                os.path.dirname(self.output()[symbol].path))
            data = pipeline_utils.urlopen_with_retry(
                self.shared_lovd_data_url + symbol).read()
            with open(self.output()[symbol].path, "wb") as f:
                f.write(data)


@requires(DownloadLOVDInputFile)
class ConcatenateLOVDData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/lovd_concatenated_genes.txt")

    def run(self):
        pipeline_utils.concatenate_files_with_identical_headers(self.lovd_file_dir, self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConcatenateLOVDData)
class NormalizeLOVDSubmissions(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/LOVD_normalized.tsv")

    def run(self):
        os.chdir(lovd_method_dir)
        args = ["python", "normalizeLOVDSubmissions.py", "-i",
                self.input().path, "-o",
                self.output().path]
        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)



@requires(NormalizeLOVDSubmissions)
class CombineEquivalentLOVDSubmissions(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/LOVD_normalized_combined.tsv")

    def run(self):
        os.chdir(lovd_method_dir)
        args = ["python", "combineEquivalentVariantSubmissions.py", "-i",
                self.input().path, "-o",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(CombineEquivalentLOVDSubmissions)
class ConvertSharedLOVDToVCF(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/sharedLOVD.hg19.vcf")

    def run(self):
        os.chdir(lovd_method_dir)
        args = ["python", "lovd2vcf.py", "-i", self.input().path, "-o",
                self.output().path, "-a", "sharedLOVDAnnotation", "-e",
                self.artifacts_dir + f"/LOVD_error_variants.txt",
                "-s", "LOVD"]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertSharedLOVDToVCF)
class CrossmapConcatenatedSharedLOVDData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/sharedLOVD.hg38.vcf")

    def run(self):
        brca_resources_dir = self.cfg.resources_dir

        args = ["CrossMap.py", "vcf",
                brca_resources_dir + "/hg19ToHg38.over.chain.gz",
                self.input().path,
                brca_resources_dir + "/hg38.fa",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(CrossmapConcatenatedSharedLOVDData)
class SortSharedLOVDOutput(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.lovd_file_dir + f"/sharedLOVD.sorted.hg38.vcf")

    def run(self):
        args = ["vcf-sort", self.input().path]

        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(SortSharedLOVDOutput)
class CopySharedLOVDOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.cfg.output_dir + f"/sharedLOVD.sorted.hg38.vcf")

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#                    G1K                      #
###############################################


class DownloadG1KVCFs(DefaultPipelineTask):
    def output(self):
        return { chrom : luigi.LocalTarget(self.g1k_file_dir + f"/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz") for chrom in self.cfg.gene_metadata['chr'] }

    def run(self):
        os.chdir(self.g1k_file_dir)

        for chrom in self.cfg.gene_metadata['chr']:
            url = f"ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
            pipeline_utils.download_file_and_display_progress(url)


@requires(DownloadG1KVCFs)
class DownloadG1KTBIs(DefaultPipelineTask):
    def output(self):
        return { chrom : luigi.LocalTarget(self.g1k_file_dir + f"/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi") for chrom in self.cfg.gene_metadata['chr'] }

    def run(self):
        os.chdir(self.g1k_file_dir)

        for chrom in self.cfg.gene_metadata['chr']:
            url = f"ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi"
            pipeline_utils.download_file_and_display_progress(url)


@requires(DownloadG1KTBIs)
class ExtractData(DefaultPipelineTask):
    def output(self):
        return { symbol : luigi.LocalTarget(
                self.g1k_file_dir + f'/1000G_{symbol}.hg37.vcf') for symbol in self.cfg.gene_metadata['symbol'] }

    def run(self):
        for index, gene in self.cfg.gene_metadata.iterrows():
            chrom = gene['chr']
            start_hg37 = gene['start_hg37']
            end_hg37 = gene['end_hg37']
            symbol = gene['symbol']

            args = ["tabix", "-h",
                    self.g1k_file_dir + f"/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
                    f"{chrom}:{start_hg37}-{end_hg37}"]

            pipeline_utils.run_process(args, redirect_stdout_path=(self.g1k_file_dir + f'/1000G_{symbol}.hg37.vcf'))
            pipeline_utils.check_file_for_contents(self.g1k_file_dir + f'/1000G_{symbol}.hg37.vcf')


@requires(ExtractData)
class ConcatenateG1KData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.g1k_file_dir + f"/1000G.hg37.vcf")

    def run(self):
        args_for_concatenate_step = ["vcf-concat"]
        for symbol in self.cfg.gene_metadata['symbol']:
            args_for_concatenate_step.append(self.g1k_file_dir + f"/1000G_{symbol}.hg37.vcf")

        pipeline_utils.run_process(args_for_concatenate_step, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConcatenateG1KData)
class CrossmapG1KData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.g1k_file_dir + f"/1000G.hg38.vcf")

    def run(self):
        brca_resources_dir = self.cfg.resources_dir

        args = ["CrossMap.py", "vcf",
                brca_resources_dir + "/hg19ToHg38.over.chain.gz",
                self.input().path,
                brca_resources_dir + "/hg38.fa",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(CrossmapG1KData)
class SortG1KData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.g1k_file_dir + f"/1000G.sorted.hg38.vcf")

    def run(self):
        args = ["vcf-sort", self.input().path]

        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(SortG1KData)
class CopyG1KOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.cfg.output_dir + f"/1000G.sorted.hg38.vcf")

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#                    EXAC                     #
###############################################


class DownloadStaticExACData(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(
            self.exac_file_dir + "/exac.brca12.sorted.hg38.vcf")

    def run(self):
        os.chdir(self.exac_file_dir)

        exac_vcf_gz_url = "https://brcaexchange.org/backend/downloads/exac.brca12.sorted.hg38.vcf"
        pipeline_utils.download_file_and_display_progress(exac_vcf_gz_url)


@requires(DownloadStaticExACData)
class CopyEXACOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(
            self.cfg.output_dir + "/exac.brca12.sorted.hg38.vcf")

    def run(self):
        copy(self.input().path,
             self.cfg.output_dir)

        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#                  ENIGMA                     #
###############################################

@requires(ConvertLatestClinvarDataToXML)
class FilterEnigmaAssertions(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.enigma_file_dir, 'enigma_clinvar.xml'))

    def run(self):
        os.chdir(clinvar_method_dir)

        args = ["python", "filter_enigma_data.py", self.input().path,
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(FilterEnigmaAssertions)
class ExtractEnigmaFromClinvar(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.enigma_file_dir, 'enigma_from_clinvar.tsv'))

    def run(self):
        os.chdir(clinvar_method_dir)

        genes_opts = [ s for g in self.cfg.gene_metadata['symbol'] for s in ['--gene', g]]

        args = ["python", "enigma_from_clinvar.py", self.input().path,
                self.output().path,
                '--logs', os.path.join(self.enigma_file_dir, 'enigma_from_clinvar.log')
               ] + genes_opts

        pipeline_utils.run_process(args)


@requires(ExtractEnigmaFromClinvar)
class CopyEnigmaOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.cfg.output_dir + "/enigma_from_clinvar.tsv")

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#             FUNCTIONAL ASSAYS               #
###############################################


class DownloadFindlayBRCA1RingFunctionScoresInputFile(DefaultPipelineTask):
    findlay_BRCA1_ring_function_scores_url = luigi.Parameter(default='https://brcaexchange.org/backend/downloads/findlay_BRCA1_ring_function_scores.tsv',
                                            description='URL to download findlay_BRCA1_ring_function_scores data from')

    def output(self):
        return luigi.LocalTarget(self.assays_dir + "/findlay_BRCA1_ring_function_scores.tsv")

    def run(self):
        data = pipeline_utils.urlopen_with_retry(self.findlay_BRCA1_ring_function_scores_url).read()
        with open(self.output().path, "wb") as f:
            f.write(data)


@requires(DownloadFindlayBRCA1RingFunctionScoresInputFile)
class ParseFindlayBRCA1RingFunctionScores(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(self.assays_dir + "/findlay_BRCA1_ring_function_scores.clean.tsv")

    def run(self):
        os.chdir(functional_assays_method_dir)

        args = ["python", "parse_functional_assay_data.py", "-i", self.input().path, "-o",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ParseFindlayBRCA1RingFunctionScores)
class ConvertFindlayBRCA1RingFunctionScoresToVCF(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.assays_dir, "findlay_BRCA1_ring_function_scores.clean.hg19.vcf"))

    def run(self):
        os.chdir(functional_assays_method_dir)

        args = ["python", "functional_assays_to_vcf.py", "-v", "-i", self.input().path, "-o",
                self.output().path, "-a", "functionalAssayAnnotation",
                "-l", self.artifacts_dir + "/findlay_BRCA1_ring_function_scores_error_variants.log",
                "-s", "FindlayBRCA1RingFunctionScores"]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(ConvertFindlayBRCA1RingFunctionScoresToVCF)
class CrossmapFindlayBRCA1RingFunctionScores(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.assays_dir, "findlay_BRCA1_ring_function_scores.clean.hg38.vcf"))

    def run(self):
        brca_resources_dir = self.cfg.resources_dir

        args = ["CrossMap.py", "vcf", brca_resources_dir + "/hg19ToHg38.over.chain.gz",
                self.input().path, brca_resources_dir + "/hg38.fa",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(CrossmapFindlayBRCA1RingFunctionScores)
class SortFindlayBRCA1RingFunctionScores(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.assays_dir, "findlay_BRCA1_ring_function_scores.clean.sorted.hg38.vcf"))

    def run(self):
        args = ["vcf-sort", self.input().path]

        pipeline_utils.run_process(args, redirect_stdout_path=self.output().path)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(SortFindlayBRCA1RingFunctionScores)
class CopyFindlayBRCA1RingFunctionScoresOutputToOutputDir(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.cfg.output_dir, "findlay_BRCA1_ring_function_scores.clean.sorted.hg38.vcf"))

    def run(self):
        copy(self.input().path, self.cfg.output_dir)
        pipeline_utils.check_file_for_contents(self.output().path)


###############################################
#            VARIANT COMPILATION              #
###############################################


class MergeVCFsIntoTSVFile(DefaultPipelineTask):
    def requires(self):

        if 'BRCA1' in self.cfg.gene_metadata['symbol'] or 'BRCA2' in self.cfg.gene_metadata['symbol']:
            yield pipeline_common.CopyOutputToOutputDir(self.cfg.output_dir,
                                                        esp_processing.SortConcatenatedESPData())
            yield pipeline_common.CopyOutputToOutputDir(self.cfg.output_dir,
                                                        gnomad_processing.SortGnomADData())
            yield CopyBICOutputToOutputDir()
            yield CopyEXACOutputToOutputDir()
            yield CopyEXLOVDOutputToOutputDir()
            yield CopyEnigmaOutputToOutputDir()
            yield CopyFindlayBRCA1RingFunctionScoresOutputToOutputDir()

        yield CopyG1KOutputToOutputDir()
        yield CopySharedLOVDOutputToOutputDir()
        yield CopyClinvarVCFToOutputDir()

    def output(self):
        return {'merged': luigi.LocalTarget(os.path.join(self.artifacts_dir, "merged.tsv")),
                'reports': luigi.LocalTarget(os.path.join(self.artifacts_dir, "reports.tsv"))}

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "variant_merging.py", "-i", self.cfg.output_dir + "/",
                "-o",
                self.artifacts_dir + '/', "-a",
                self.artifacts_dir + '/', "-v",
                "-c", self.cfg.gene_config_path]

        pipeline_utils.run_process(args)

        pipeline_utils.check_file_for_contents(self.output()['merged'].path)
        pipeline_utils.check_file_for_contents(self.output()['reports'].path)


@requires(MergeVCFsIntoTSVFile)
class AggregateMergedOutput(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "aggregated.tsv"))

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "aggregate_across_columns.py",
                "-i", self.input()['merged'].path,
                "-o", self.output().path,
                "-c", self.cfg.gene_config_path]

        pipeline_utils.run_process(args)

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            self.input()['merged'].path,
            self.output().path)


@requires(AggregateMergedOutput)
class BuildAggregatedOutput(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "built.tsv"))

    def run(self):
        brca_resources_dir = self.cfg.resources_dir
        os.chdir(data_merging_method_dir)

        args = ["python", "brca_pseudonym_generator.py",
                self.input().path,
                self.output().path,
                "--log-path", os.path.join(self.artifacts_dir, "brca-pseudonym-generator.log"),
                "--config-file", self.cfg.gene_config_path,
                "--resources", brca_resources_dir]

        pipeline_utils.run_process(args)

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            self.input().path,
            self.output().path)


@requires(BuildAggregatedOutput)
class AppendCAID(DefaultPipelineTask):

    def output(self):
        artifacts_dir = self.cfg.output_dir + "/release/artifacts/"
        return luigi.LocalTarget(artifacts_dir + "built_with_ca_ids.tsv")

    def run(self):
        release_dir = self.cfg.output_dir + "/release/"
        artifacts_dir = release_dir + "artifacts/"
        brca_resources_dir = self.cfg.resources_dir
        os.chdir(data_merging_method_dir)

        args = ["python", "get_ca_id.py", "-i",
                artifacts_dir + "built.tsv", "-o",
                artifacts_dir + "/built_with_ca_ids.tsv", "-l",
                artifacts_dir + "/get_ca_id.log"]
        print("Running get_ca_id.py with the following args: %s" % (
            args))
        sp = subprocess.Popen(args, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        pipeline_utils.print_subprocess_output_and_error(sp)

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            artifacts_dir + "built.tsv",
            artifacts_dir + "built_with_ca_ids.tsv")


@requires(AppendCAID)
class AppendMupitStructure(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "built_with_mupit.tsv"))

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "getMupitStructure.py", "-i",
                self.input().path, "-o",
                self.output().path]

        pipeline_utils.run_process(args)

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            self.input().path,
            self.output().path)



@requires(AppendMupitStructure)
class CalculatePriors(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "built_with_priors.tsv"))

    def run(self):
        if 'BRCA1' in self.cfg.gene_metadata['symbol'] or 'BRCA2' in self.cfg.gene_metadata['symbol']:
            artifacts_dir_host = self.cfg.output_dir_host + "/release/artifacts/"
            os.chdir(priors_method_dir)

            args = ['bash', 'calcpriors.sh', self.cfg.priors_references_dir,
                    artifacts_dir_host, 'built_with_mupit.tsv',
                    'built_with_priors.tsv', self.cfg.priors_docker_image_name]

            pipeline_utils.run_process(args)

            pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
                self.input().path,
                self.output().path)
        else:
            copy(self.input().path, self.output().path)


@requires(CalculatePriors)
class FilterBlacklistedPriors(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "built_with_priors_clean.tsv"))

    def run(self):
        if 'BRCA1' in self.cfg.gene_metadata['symbol'] or 'BRCA2' in self.cfg.gene_metadata['symbol']:
            os.chdir(priors_filter_method_dir)

            args = ["python", "filterBlacklistedVars.py",
                    "--output", self.output().path,
                    "--blacklisted_vars", "blacklisted_vars.txt",
                    "filter",
                    self.input().path]

            pipeline_utils.run_process(args)

            # we only clear a few columns; we shouldn't be gaining or losing any variants
            pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
                self.input().path,
                self.output().path)
        else:
            copy(self.input().path, self.output().path)


@requires(FilterBlacklistedPriors)
class AppendVRId(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "built_with_vr_ids.tsv"))

    def run(self):
        artifacts_dir_host = self.cfg.output_dir_host + "/release/artifacts/"
        os.chdir(vr_method_dir)

        args = [
            'bash', 'appendvrids.sh',
            artifacts_dir_host,
            'built_with_priors_clean.tsv',
            'built_with_vr_ids.tsv',
            self.cfg.vr_docker_image_name,
            self.cfg.seq_repo_dir
        ]

        pipeline_utils.run_process(args)

        # we shouldn't be gaining or losing any variants
        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            self.input().path,
            self.output().path)


@requires(AppendVRId)
class PruneUnnecessaryColumns(DefaultPipelineTask):
    def output(self):
        return {'built_pruned': luigi.LocalTarget(os.path.join(self.artifacts_dir, "built_pruned.tsv")),
                'reports_pruned': luigi.LocalTarget(os.path.join(self.artifacts_dir, "reports_pruned.tsv"))}

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "prune_excess_columns.py", "-i",
                self.input().path, "-o",
                self.output()['built_pruned'].path,
                "-c", self.cfg.gene_config_path]

        pipeline_utils.run_process(args)

        args = ["python", "prune_excess_columns.py", "-i",
                os.path.join(self.artifacts_dir, "reports.tsv"),
                "-o", self.output()['reports_pruned'].path,
                "-c", self.cfg.gene_config_path]

        pipeline_utils.run_process(args)

        pipeline_utils.check_file_for_contents(self.output()['built_pruned'].path)
        pipeline_utils.check_file_for_contents(self.output()['reports_pruned'].path)


@requires(bayesdel_processing.AddBayesdelScores)
class FindMissingReports(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.artifacts_dir, "missing_reports.log"))

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "check_for_missing_reports.py", "-b",
                self.input().path, "-r",
                self.artifacts_dir,
                "-a", self.artifacts_dir, "-v"]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(FindMissingReports)
class RunDiffAndAppendChangeTypesToOutput(DefaultPipelineTask):
    def _extract_release_date(self, version_json):
        with open(version_json, 'r') as f:
            j = json.load(f)
            return datetime.datetime.strptime(j['date'], '%Y-%m-%d')

    def output(self):
        return {'built_with_change_types': luigi.LocalTarget(
            os.path.join(self.release_dir, "built_with_change_types.tsv")),
                'removed': luigi.LocalTarget(os.path.join(self.diff_dir , "removed.tsv")),
                'added': luigi.LocalTarget(os.path.join(self.diff_dir , "added.tsv")),
                'added_data': luigi.LocalTarget(os.path.join(self.diff_dir , "added_data.tsv")),
                'diff': luigi.LocalTarget(os.path.join(self.diff_dir , "diff.txt")),
                'diff_json': luigi.LocalTarget(os.path.join(self.diff_dir , "diff.json")),
                'README': luigi.LocalTarget(os.path.join(self.diff_dir , "README.txt"))}

    def run(self):
        os.chdir(utilities_method_dir)

        tmp_dir = tempfile.mkdtemp()
        previous_data_path = pipeline_utils.extract_file(
            self.cfg.previous_release_tar, tmp_dir,
            'output/release/built_with_change_types.tsv') if self.cfg.first_release is False else None
        version_json_path = pipeline_utils.extract_file(
            self.cfg.previous_release_tar, tmp_dir,
            'output/release/metadata/version.json')
        previous_release_date = self._extract_release_date(version_json_path)
        previous_release_date_str = datetime.datetime.strftime(
            previous_release_date, '%m-%d-%Y')

        args = ["python", "releaseDiff.py", "--v2",
                os.path.join(self.artifacts_dir, "built_pruned.tsv"), "--v1",
                previous_data_path,
                "--removed", os.path.join(self.diff_dir, "removed.tsv"), "--added",
                os.path.join(self.diff_dir, "added.tsv"), "--added_data",
                os.path.join(self.diff_dir, "added_data.tsv"), "--diff", os.path.join(self.diff_dir, "diff.txt"),
                "--diff_json", os.path.join(self.diff_dir, "diff.json"),
                "--output", os.path.join(self.release_dir, "built_with_change_types.tsv"),
                "--artifacts_dir", self.artifacts_dir,
                "--diff_dir", self.diff_dir, "--v1_release_date",
                previous_release_date_str, "--reports", "False"]

        pipeline_utils.run_process(args)

        shutil.rmtree(tmp_dir)  # cleaning up

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            os.path.join(self.artifacts_dir, "built_pruned.tsv"),
            os.path.join(self.release_dir, "built_with_change_types.tsv"))


@requires(RunDiffAndAppendChangeTypesToOutput)
class RunDiffAndAppendChangeTypesToOutputReports(DefaultPipelineTask):
    def _extract_release_date(self, version_json):
        with open(version_json, 'r') as f:
            j = json.load(f)
            return datetime.datetime.strptime(j['date'], '%Y-%m-%d')

    def output(self):
        return {'reports_with_change_types': luigi.LocalTarget(
            os.path.join(self.release_dir, "reports_with_change_types.tsv")),
                'removed_reports': luigi.LocalTarget(
                    os.path.join(self.diff_dir, "removed_reports.tsv")),
                'added_reports': luigi.LocalTarget(
                    os.path.join(self.diff_dir, "added_reports.tsv")),
                'added_data_reports': luigi.LocalTarget(
                    os.path.join(self.diff_dir, "added_data_reports.tsv")),
                'diff_reports': luigi.LocalTarget(
                    os.path.join(self.diff_dir, "diff_reports.txt")),
                'diff_json_reports': luigi.LocalTarget(
                    os.path.join(self.diff_dir, "diff_reports.json")),
                'README': luigi.LocalTarget(os.path.join(self.diff_dir, "README.txt"))}

    def run(self):
        os.chdir(utilities_method_dir)

        tmp_dir = tempfile.mkdtemp()
        previous_data_path = pipeline_utils.extract_file(
            self.cfg.previous_release_tar, tmp_dir,
            'output/release/artifacts/reports_with_change_types.tsv') if self.cfg.first_release is False else None
        version_json_path = pipeline_utils.extract_file(
            self.cfg.previous_release_tar, tmp_dir,
            'output/release/metadata/version.json')
        previous_release_date = self._extract_release_date(version_json_path)
        previous_release_date_str = datetime.datetime.strftime(
            previous_release_date, '%m-%d-%Y')

        args = ["python", "releaseDiff.py", "--v2",
                os.path.join(self.artifacts_dir, "reports_pruned.tsv"), "--v1", previous_data_path,
                "--removed", self.output()['removed_reports'].path, "--added",
                self.output()['added_reports'].path, "--added_data",
                self.output()['added_data_reports'].path, "--diff",
                self.output()['diff_reports'].path, "--diff_json",
                self.output()['diff_json_reports'].path,
                "--output", self.output()['reports_with_change_types'].path,
                "--artifacts_dir", self.artifacts_dir,
                "--diff_dir", self.diff_dir, "--v1_release_date",
                previous_release_date_str, "--reports", "True"]

        pipeline_utils.run_process(args)

        shutil.rmtree(tmp_dir)  # cleaning up

        pipeline_utils.check_input_and_output_tsvs_for_same_number_variants(
            os.path.join(self.artifacts_dir, "reports_pruned.tsv"),
            os.path.join(self.release_dir, "reports_with_change_types.tsv"))


@requires(RunDiffAndAppendChangeTypesToOutputReports)
class GenerateReleaseNotes(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.metadata_dir, "version.json"))

    def run(self):
        os.chdir(data_merging_method_dir)

        args = ["python", "buildVersionMetadata.py", "--date",
                str(self.cfg.date), "--notes", self.cfg.release_notes,
                "--output", self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(GenerateReleaseNotes)
class TopLevelReadme(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.cfg.output_dir, "README.txt"))

    def run(self):
        top_level_readme_src = os.path.abspath(
            os.path.join(os.path.realpath(__file__), os.pardir, os.pardir,
                         "top_level_readme.txt"))

        shutil.copyfile(top_level_readme_src, self.output().path)


@requires(TopLevelReadme)
class DataDictionary(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.release_dir, "built_with_change_types.dictionary.tsv"))

    def run(self):
        data_dictionary_src = os.path.abspath(
            os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, "built_with_change_types.dictionary.tsv"))

        shutil.copyfile(data_dictionary_src, self.output().path)


@requires(DataDictionary)
class GenerateMD5Sums(DefaultPipelineTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(self.cfg.output_dir, "md5sums.txt"))

    def run(self):
        os.chdir(utilities_method_dir)

        args = ["python", "generateMD5Sums.py", "-i", self.cfg.output_dir, "-o",
                self.output().path]

        pipeline_utils.run_process(args)
        pipeline_utils.check_file_for_contents(self.output().path)


@requires(GenerateMD5Sums)
class GenerateReleaseArchive(DefaultPipelineTask):
    def getArchiveName(self):
        # Format archive filename as release-mm-dd-yy.tar.gz
        return "release-" + self.cfg.date.strftime("%x").replace('/',
                                                                 '-') + ".tar.gz"

    def getArchiveParentDirectory(self):
        return os.path.dirname(self.cfg.output_dir) + "/"

    def output(self):
        return luigi.LocalTarget(
            self.getArchiveParentDirectory() + self.getArchiveName())

    def run(self):
        os.chdir(self.getArchiveParentDirectory())
        with tarfile.open(
                self.getArchiveParentDirectory() + self.getArchiveName(),
                "w:gz") as tar:
            tar.add(self.cfg.output_dir,
                    arcname=os.path.basename(self.cfg.output_dir))
