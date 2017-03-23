# Copyright (C) 2015 by Per Unneberg
import re
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame
import logging
logger = logging.getLogger(__name__)

COVERAGE_PER_CONTIG_COLUMNS = ["chr", "chrlen", "mapped_bases",
                               "mean_coverage", "sd"]


re_trim = re.compile(r'(,|\s+bp.*$|\s+\(.*%\)|%)')

def _split_x(x, delim=" = "):
    y = x.strip().split(delim)
    return [y[0], re_trim.sub("", y[1])]

@resource.register('.*genome_results.txt', priority=20)
@annotate_by_uri
def resource_genome_results(uri, key="Globals", **kwargs):
    with open(uri) as fh:
        data = "".join(fh)
    sections = re.split(">+\s+[a-zA-Z ]+", data)
    section_names = ["Header"] + [re.sub(" ", "_", x) for x in re.findall(">+\s+([a-zA-Z ]+)", data)]
    d = dict()
    for h, sec in zip(section_names, sections):
        if h == "Coverage_per_contig":
            d[h] = DataFrame.from_records([re.split("\s+", x.strip()) for x in sec.split("\n") if x],
                                          columns=COVERAGE_PER_CONTIG_COLUMNS,
                                          index="chr")
            d[h] = d[h].apply(pd.to_numeric)
        elif h in ["Coverage", "Header"]:
            pass
        else:
            d[h] = DataFrame.from_records([_split_x(x) for x in sec.split("\n") if x],
                                          columns=["statistic", "value"],
                                          index="statistic")
            if not h in ["Input"]:
                d[h] = d[h].apply(pd.to_numeric)
    return d[key]


@resource.register('.*coverage_across_reference.txt', priority=20)
@resource.register('.*coverage_histogram.txt', priority=20)
@resource.register('.*duplication_rate_histogram.txt', priority=20)
@resource.register('.*genome_fraction_coverage.txt', priority=20)
@resource.register('.*homopolymer_indels.txt', priority=20)
@resource.register('.*insert_size_across_reference.txt', priority=20)
@resource.register('.*insert_size_histogram.txt', priority=20)
@resource.register('.*mapped_reads_clipping_profile.txt', priority=20)
@resource.register('.*mapped_reads_gc-content_distribution.txt', priority=20)
@resource.register('.*mapped_reads_nucleotide_content.txt', priority=20)
@resource.register('.*mapping_quality_across_reference.txt', priority=20)
@resource.register('.*mapping_quality_histogram.txt', priority=20)
@annotate_by_uri
def resource_read_data_frame(uri, **kwargs):
    d = pd.read_table(uri)
    return d


def aggregate(infiles, outfile, key="Globals", regex=None,  **kwargs):
    import odo
    dflist = []
    for f in infiles:
        logger.info("loading {}".format(f))
        df = odo.odo(f, DataFrame, key=key)
        if regex:
            m = re.search(regex, f)
            if m:
                logger.info("adding columns {}".format(",".join(["{}={}".format(k, v) for k,v in m.groupdict().items()])))
                for k, v in m.groupdict().items():
                    df[k] = v
        dflist.append(df)
    df = pd.concat(dflist)
    df.to_csv(outfile)

