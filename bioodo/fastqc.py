# Copyright (C) 2016 by Per Unneberg
from blaze import resource, DataFrame
import re
import pandas as pd
from .pandas import annotate_by_uri
import logging

logger = logging.getLogger(__name__)

SECTION_NAMES=['Header', 'Basic_Statistics', 'Per_base_sequence_quality', 'Per_sequence_quality_scores', 'Per_base_sequence_content', 'Per_sequence_GC_content', 'Per_base_N_content', 'Sequence_Length_Distribution', 'Sequence_Duplication_Levels', 'Overrepresented_sequences', 'Adapter_Content', 'Kmer_Content']


@resource.register('.*fastqc_data.txt')
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
        raise KeyError("Not in section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = re.sub(">>END_MODULE", "", "".join(fh))
    sections = [x for x in re.split(">>+[a-zA-Z _\t\n]+", data)]
    ## Pass/fail summary
    if key == "Summary":
        return DataFrame.from_records([re.sub(" ", "_", x).split("\t") for x in re.findall(">>(.+)", data)], columns=["Statistic", "Value"], index="Statistic")
    for h, sec in zip(SECTION_NAMES, sections):
        if not h == key:
            continue
        logger.debug("Parsing section ", h)
        if h == "Header":
            d = DataFrame.from_records([[re.sub("#", "", x) for x in re.split("\t", sec.strip())]], index=columns[0])
        else:
            i = 1 if h.startswith("Sequence_Duplication") else 0
            columns = [re.sub("#", "", x) for x in re.split("\t", sec.split("\n")[i])]
            d = DataFrame.from_records([re.split("\t", x.strip()) for x in sec.split("\n") if x and not x.startswith("#")],
                                          columns = columns, index=columns[0])
    return d