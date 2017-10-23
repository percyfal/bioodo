# Copyright (C) 2016 by Per Unneberg
import re
from os.path import join, basename
import logging
import bioodo
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils


logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['fastqc']


# Possible section names
SECTION_NAMES = ['Header', 'Basic_Statistics',
                 'Per_base_sequence_quality', 'Per_tile_sequence_quality',
                 'Per_sequence_quality_scores', 'Per_base_sequence_content',
                 'Per_sequence_GC_content', 'Per_base_N_content',
                 'Sequence_Length_Distribution', 'Sequence_Duplication_Levels',
                 'Overrepresented_sequences', 'Adapter_Content',
                 'Kmer_Content']


@resource.register(config['fastqc']['pattern'],
                   priority=config['fastqc']['priority'])
@pivot
@annotate_by_uri
def resource_fastqc_data(uri, key="Basic_Statistics", **kwargs):
    """Parse fastqc text output file.

    Args:
      uri (str): filename
      key (str): result section to return

    Returns:
      DataFrame: DataFrame for requested section
    """
    def _parse():
        fastqc_data = kwargs.get('fastqc_data', 'fastqc_data.txt')
        if uri.endswith(".zip"):
            logger.debug("Reading zipped fastqc file")
            from zipfile import ZipFile
            with ZipFile(uri) as zf:
                with zf.open(
                        join(basename(uri.strip(".zip")), fastqc_data)) as fh:
                    data = re.sub(">>END_MODULE", "",
                                  fh.read().decode("utf-8"))
        else:
            logger.debug("Reading fastqc_data.txt file")
            with open(uri) as fh:
                data = re.sub(">>END_MODULE", "", "".join(fh))
        return data

    logger.debug("Reading {}".format(uri))
    if key not in SECTION_NAMES + ['Summary']:
        raise KeyError(
            "Not in allowed section names; allowed values are {}".format(
                ", ".join(SECTION_NAMES + ["Summary"])))
    data = _parse()
    sections = [x for x in re.split(">>+[a-zA-Z _\t\n]+", data)]
    headings = ['Header'] + \
               [re.sub(" ", "_", (re.sub(">>", "", x.split("\t")[0])))
                for x in re.split("\n", data) if x.startswith(">>")]
    if key not in headings + ['Summary']:
        raise KeyError("Not in available names; " +
                       "analysis has not been performed")
    # Pass/fail summary
    if key == "Summary":
        return DataFrame.from_records(
            [re.sub(" ", "_", x).split("\t")
             for x in re.findall(">>(.+)", data)],
            columns=["Statistic", "Value"], index="Statistic")
    for h, sec in zip(headings, sections):
        if not h == key:
            continue
        logger.debug("Parsing section {}".format(h))
        if h == "Header":
            d = DataFrame.from_records(
                [[re.sub("#", "", x)
                  for x in re.split("\t", sec.strip())]])
        else:
            i = 1 if h.startswith("Sequence_Duplication") else 0
            columns = [re.sub("#", "", x)
                       for x in re.split("\t", sec.split("\n")[i].strip())]
            d = DataFrame.from_records(
                [re.split("\t", x.strip())
                 for x in sec.split("\n") if x and not x.startswith("#")],
                columns=columns, index=columns[0])
    return d


aggregate = utils.aggregate_factory("fastqc")
