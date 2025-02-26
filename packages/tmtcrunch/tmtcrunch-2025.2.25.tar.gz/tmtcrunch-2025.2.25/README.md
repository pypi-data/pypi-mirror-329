# TMTCrunch

TMTCrunch is an open-source Python utility for analysis of tandem mass tag (TMT) proteomics data with the focus on protein isoforms resulting from alternative spicing.

## Installation

### Installing from PyPI
The latest released version can be installed from the [Python Package Index](https://pypi.org/project/tmtcrunch):
```shell
pip install tmtcrunch
```

### Installing from source
The development version can be installed directly from the source repository:
```shell
pip install https://codeberg.org/makc/tmtcrunch.git
```

## Dependencies
TMTCrunch relies on the following Python packages:
- [numpy](https://pypi.org/project/numpy/)
- [pandas](https://pypi.org/project/pandas/)
- [pyteomics](https://pypi.org/project/pyteomics/)
- [tomli](https://pypi.org/project/tomli/) (required only for Python < 3.11)

and it would use statistics functions from [astropy](https://pypi.org/project/astropy/) package if available.

## Command line options
```
usage: tmtcrunch [-h] [--specimen-tags SPECIMEN_TAGS] [--gis-tags GIS_TAGS]
                 [--cfg CFG] [--output-dir OUTPUT_DIR]
                 [--output-prefix OUTPUT_PREFIX] [--phospho]
                 [--keep-columns KEEP_COLUMNS [KEEP_COLUMNS ...]]
                 [--verbose {0,1,2}] [--show-config] [--version]
                 [file ...]

positional arguments:
  file                  Scavager *_PSMs_full.tsv files.

options:
  -h, --help            show this help message and exit
  --specimen-tags SPECIMEN_TAGS
                        Comma-separated sequence of specimen TMT tags.
  --gis-tags GIS_TAGS   Comma-separated sequence of GIS TMT tags.
  --cfg CFG             Path to configuration file. Can be specified multiple
                        times.
  --output-dir OUTPUT_DIR, --odir OUTPUT_DIR
                        Existing output directory. Default is current
                        directory.
  --output-prefix OUTPUT_PREFIX, --oprefix OUTPUT_PREFIX
                        Prefix for output files. Default is 'tmtcrunch_'.
  --phospho             Enable common modifications for phospho-proteomics.
  --keep-columns KEEP_COLUMNS [KEEP_COLUMNS ...]
                        Extra columns from input files to keep in output
                        files.
  --verbose {0,1,2}     Logging verbosity. Default is 1.
  --show-config         Show configuration and exit.
  --version             Output version information and exit.
```

## Configuration file
TMTCrunch stores its configuration in [TOML](https://toml.io) format.

Default TMTCrunch configuration:
```TOML
# Specimen TMT labels.
specimen_tags = ['127C', '127N', '128C', '128N', '129C', '129N', '130C', '130N', '131']
# Global internal standard (GIS) TMT labels.
gis_tags = ['126', '131C']

# Prefix of decoy proteins.
decoy_prefix = 'DECOY_'

# List of column names from input files to save in the output.
keep_columns = []

# If true, perform PSM groupwise analysis.
groupwise = true

# If true, respect peptide modifications and terminate analysis at peptide level.
with_modifications = false

# No modifications by default. Run TMTCrunch with --phospho argument
# to enable common modifications for phospho-proteomics.
[modification.universal]
[modification.selective]

# Keys below are only applicable if groupwise analysis is requested.
# Prefixes of target proteins. If not set, `target_prefixes` will be deduced
# from the prefixes of PSM groups.
# target_prefixes = ['alt_', 'canon_']

# Each PSM group is named after its subkey and defined by three keys:
# `descr` - group description
# `prefixes` - prefixes of target proteins
# `fdr` - groupwise false discovery rate

# Isoform PSMs: protein group of each PSM consists of target proteins
# with 'alt_' prefix only and any decoy proteins.
[psm_group.isoform]
descr = 'Isoform PSMs'
prefixes = [['alt_']]
fdr = 0.05

# Canonical PSMs: protein group of each PSM consists of target proteins
# with 'canon_' prefix only and any decoy proteins.
[psm_group.canon]
descr = 'Canonical PSMs'
prefixes = [['canon_']]
fdr = 0.01

# Shared PSMs: protein group of each PSM consists both of
# 'canon_' and 'alt_' target proteins and any decoy proteins.
[psm_group.shared]
descr = 'Shared PSMs'
prefixes = [['canon_', 'alt_']]
fdr = 0.01
```


Additional configuration for phospho-proteomics:
```TOML
with_modifications = true

# Modifications can be either universal or selective. PSMs for modified
# peptides with any universal modification and the same pattern of selective
# modifications are treated together, PSMs for peptides with different pattern
# of selective modifications are treated separately.

[modification.universal.1]
name = "Carboxyamidomethylation"
mass = "160.031"
modX = "camC"

[modification.universal.2]
name = "TMTplex at K"
mass = "357.258"
modX = "tK"

[modification.universal.3]
name = "TMTplex n-term"
mass = "230.171"
modX = "t-"

[modification.universal.4]
name = "Oxidation"
mass = "147.035"
modX = "oxM"

[modification.selective.5]
name = "Phosphorylation S"
mass = "166.998"
modX = "pS"

[modification.selective.6]
name = "Phosphorylation T"
mass = "181.014"
modX = "pT"

[modification.selective.7]
name = "Phosphorylation Y"
mass = "243.030"
modX = "pY"
```

## License
TMTCrunch is distributed under a BSD License.

## Related software
 - [Pyteomics](https://github.com/levitsky/pyteomics) - Python framework for proteomics data analysis.
 - [IdentiPy](https://github.com/levitsky/identipy) - search engine for bottom-up proteomics.
 - [Scavager](https://github.com/markmipt/scavager) - proteomics post-search validation tool.
