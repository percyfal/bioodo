# Copyright (C) 2016 by Per Unneberg
import re
import os
import logging
from bioodo import resource, annotate_by_uri, DataFrame
import pandas as pd

logger = logging.getLogger(__name__)

# Possible section names
SECTION_NAMES=['Header', 'Basic_Statistics', 'Per_base_sequence_quality', 'Per_tile_sequence_quality', 'Per_sequence_quality_scores', 'Per_base_sequence_content', 'Per_sequence_GC_content', 'Per_base_N_content', 'Sequence_Length_Distribution', 'Sequence_Duplication_Levels', 'Overrepresented_sequences', 'Adapter_Content', 'Kmer_Content']


@resource.register('.*fastqc(_data.txt|.zip)', priority=30)
@annotate_by_uri
def resource_fastqc_data(uri, key="Basic_Statistics", **kwargs):
    """Parse fastqc text output file.

    Args:
      uri (str): filename
      key (str): result section to return
      
    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES + ['Summary']:
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    if uri.endswith(".zip"):
        from zipfile import ZipFile
        with ZipFile(uri) as zf:
            with zf.open(os.path.join(os.path.basename(uri.strip(".zip")), kwargs.get('fastqc_data', 'fastqc_data.txt'))) as fh:
                data = re.sub(">>END_MODULE", "", fh.read().decode("utf-8"))
    else:
        with open(uri) as fh:
            data = re.sub(">>END_MODULE", "", "".join(fh))
    sections = [x for x in re.split(">>+[a-zA-Z _\t\n]+", data)]
    headings = ['Header'] + [re.sub(" ", "_", (re.sub(">>", "", x.split("\t")[0]))) for x in re.split("\n", data) if x.startswith(">>")]
    if key not in headings + ['Summary']:
        raise KeyError("Not in available names; analysis has not been performed")
    ## Pass/fail summary
    if key == "Summary":
        return DataFrame.from_records([re.sub(" ", "_", x).split("\t") for x in re.findall(">>(.+)", data)], columns=["Statistic", "Value"], index="Statistic")
    for h, sec in zip(headings, sections):
        if not h == key:
            continue
        logger.debug("Parsing section ", h)
        if h == "Header":
            d = DataFrame.from_records([[re.sub("#", "", x) for x in re.split("\t", sec.strip())]])
        else:
            i = 1 if h.startswith("Sequence_Duplication") else 0
            columns = [re.sub("#", "", x) for x in re.split("\t", sec.split("\n")[i].strip())]
            d = DataFrame.from_records([re.split("\t", x.strip()) for x in sec.split("\n") if x and not x.startswith("#")],
                                          columns = columns, index=columns[0])
    return d



def aggregate(infiles, outfile, key="Kmer_content", regex=None, **kwargs):
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
