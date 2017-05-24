# Copyright (C) 2015 by Per Unneberg
import re
import logging
import math
from datetime import datetime
import pandas as pd
from blaze import odo, DataFrame

logger = logging.getLogger(__name__)


# FIXME: utilize pandas builtin functionality for handling these issues
def recast(x, strpfmt="%b %d %H:%M:%S"):
    """Reformat strings to numeric or datestrings.

    Args:
      x (str): string
      strpfmt (str): strpfmt time string

    Returns:
      datetime.strptime: datetime object
    """
    if isinstance(x, float):
        if math.isnan(x):
            return x
    x = x.rstrip().lstrip()
    if re.match('^[0-9]+$', x):
        return int(x)
    elif re.match('^[0-9]+[,\.][0-9]+$', x):
        return float(x.replace(",", "."))
    elif re.search("%", x):
        return float(x.replace(",", ".").replace("%", ""))
    else:
        try:
            dateobj = datetime.strptime(x, strpfmt)
            return dateobj
        except:
            return x


# Replace whitespace with underscore, convert percent characters to PCT
def trim_header(x, underscore=False, percent=False):
    return x.lstrip().rstrip().replace(" ", "_" if underscore else " ").replace("%", "PCT" if percent else "%").replace(",", "_" if underscore else " ")


def annotate_df(infile, parser, groupnames=["SM"]):
    """Annotate a parsed odo unit.

    Assumes metadata information is stored in input file name.

    Args:
      infile (str): file name
      parser (re): regexp object to parse input file name with. Metadata information to parse is stored in file name

      groupnames (list): list of parser group names to use. For each
      name <name>, the parser should have a corresponding (?P<name>...)
      expression
    """
    df = odo(infile, pd.DataFrame)
    m = parser.parse(infile)
    for name in groupnames:
        df[name] = str(m[name])
    return df


def aggregate(infiles, regex=None, parser=None, **kwargs):
    """Helper function to aggregate files.

    Given a list of input files for a bioinformatics application,
    seamlessly apply odo to each input file and concatenate the
    results. Additional file-based information, such as sample names,
    can be added on the fly by supplying a regular expression with
    group names that parses the file names. The regular expression
    group name will be added to the data frame.

    Note that the function is not directly called from
    :mod:`bioodo.utils` but rather from one of the application
    modules, as the following example shows.

    Examples:

      The following example uses :func:`bioodo.qualimap.aggregate` to
      parse two qualimap output files, extract sample names via the
      regular expression, and concatenate the results together with an
      additional column named "sample".

      .. code-block:: python

         from bioodo import qualimap
         qualimap_files = ["Sample1/genome_results.txt",
                           "Sample2/genome_results.txt"]
         df = qualimap.aggregate(qualimap_files,
                                 regex="(?P<sample>Sample[0-9]+)/genome_results.txt")

    Args:
      infiles (list): list of input file names
      regex (str): regex pattern to parse file
      parser (func): bioodo parser function to use in case the generic
                     parsing fails
      kwargs (dict): keyword arguments

    Returns:
      Aggregated data frame

    """
    import odo
    dflist = []
    for f in infiles:
        logger.debug("loading {}".format(f))
        if parser:
            df = odo.odo(parser(f, **kwargs), DataFrame)
        else:
            df = odo.odo(f, DataFrame, **kwargs)
        if regex:
            m = re.search(regex, f)
            if m:
                logger.debug("adding columns {}".format(",".join(["{}={}".format(k, v) for k, v in m.groupdict().items()])))
                for k, v in m.groupdict().items():
                    df[k] = v
        dflist.append(df)
    df = pd.concat(dflist)
    return df
