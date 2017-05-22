# Copyright (C) 2015 by Per Unneberg
import re
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, DataFrame, utils
import logging


logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['qualimap']

COVERAGE_PER_CONTIG_COLUMNS = ["chr", "chrlen", "mapped_bases",
                               "mean_coverage", "sd"]


re_trim = re.compile(r'(,|\s+bp.*$|\s+\(.*%\)|%)')


def _split_x(x, delim=" = "):
    y = x.strip().split(delim)
    return [y[0], re_trim.sub("", y[1])]


@resource.register(config['genome_results']['pattern'],
                   priority=config['genome_results']['priority'])
@annotate_by_uri
def resource_genome_results(uri, key="Globals", **kwargs):
    with open(uri) as fh:
        data = "".join(fh)
    sections = re.split(">+\s+[a-zA-Z ]+", data)
    section_names = ["Header"] + [
        re.sub(" ", "_", x) for x in re.findall(">+\s+([a-zA-Z ]+)", data)]
    d = dict()
    for h, sec in zip(section_names, sections):
        if h == "Coverage_per_contig":
            d[h] = DataFrame.from_records(
                [re.split("\s+", x.strip()) for x in sec.split("\n") if x],
                columns=COVERAGE_PER_CONTIG_COLUMNS,
                index="chr")
            d[h] = d[h].apply(pd.to_numeric)
        elif h in ["Coverage", "Header"]:
            pass
        else:
            d[h] = DataFrame.from_records(
                [_split_x(x) for x in sec.split("\n") if x],
                columns=["statistic", "value"],
                index="statistic")
            if h not in ["Input"]:
                d[h] = d[h].apply(pd.to_numeric)
    return d[key]


@resource.register(config['data_frame']['pattern'],
                   priority=config['data_frame']['priority'])
@annotate_by_uri
def resource_read_data_frame(uri, **kwargs):
    d = pd.read_table(uri)
    return d


# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual qualimap reports to one output file

    Params:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating qualimap infiles {} in qualimap aggregate".format(",".join(infiles)))
    df = utils.aggregate_files(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df
