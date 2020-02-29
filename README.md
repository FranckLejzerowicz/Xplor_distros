# Xplor_distros

## Description

Xplor_distros is a command line tool that allows looking at the distributions of the numeric variables in a
metadata file.

It is emminently useful to have in order to make some checks of the data dimensions before throwing them all
into a joint analysis, such as a Correspondance Analysis. 

To dive in, click-select samples on the left panels to see only their distributions on the right histogram.
This way, you may see which groups of features could be analysed jointly, which other not, and also start 
thinking about applying transformations on your data before running analyses.
    

## Installation


For the first installation, please run:

```
pip install git+https://github.com/FranckLejzerowicz/Xplor_distros.git
```

If there's an update because the developer have been sloppy, please run:

```
pip install --upgrade git+https://github.com/FranckLejzerowicz/Xplor_distros.git
```

*_Note that pip should be for python3_

## Input

- **[required]**:
  - `-m` One (or more) metadata file path(s). Use option repeatedly for multiple metadata files
  - `-o` Output file path for the visualization (will create folder(s) if not exist).

    `Xplor_distros -m meta_1.tsv  -m meta_2.tsv -m meta_3.tsv -o visu.html`

- **[optional]**:
  - `-p` One (or more) categorical metadata variable(s) can be passed as optional arguments in order stratify the
distributions. Same for multiple metadata files:

    `Xplor_distros -p sex -p age_cat`

Variables are recognized as _Valid_ categorical metadata variables that satisfy the following criteria:
- is present in the metadata (obviously)
- is inferred as a categorical variable, i.e. it is not made only of integers, only of floats, or of a mixture 
of these numeric types and values form the following list of "nan" value placeholders:
  - `unknown`
  - `unspecified`
  - `not provided`
  - `not applicable`
  - `missing` 
 
## Outputs
 
A **.html** file containing visualization(s) of the metadata variables distributions. The file extension should be 
`.html`, otherwise, it will be added to the passed file path, e.g.:

- `path/to/output_file.html` --> `path/to/output_file.html`  
- `path/to/output_file.txt` --> `path/to/output_file.txt.html`  

_If you specified some level
 of stratification, you will have one row per factor_. For each row, you will see __3 panels__:

- **left panel**: metadata variables are dots located on a `skewness` _vs_ `median` scatter plot 
- **middle panel**: same but the median are changed to log10 scale (definitely indicating a scale issue!)
- **right panel**: histogram of the underlying numerical variables' distributions.

To the very least, there will be one row of three figure panels per metadata file.
If one provide valid categorical metadata variable(s), there will be one such row 
for each factor in provided categorical metadata variables.

It is possible to create new metadata variables based on the joining of all the variables passed to the `-p` options,
my activating the `--merge` flag, which will create a new stratification, e.g.:

For the metadata table:

#SampleID | col_1 | col_2 | col_3 
:---:|:---:|:---:|:---:
sample.1 | **A1** | **B1** | **C1** 
sample.2 | **A2** | **B2** | **C2**  
sample.3 | **A3** | **B3** | **C3**

Using the command `Xplor_distros -m meta_table.tsv -p col_1 -p col_2 -p col_3 --merge`

Will stratify the figure for each of these _created_ factors: **A1__B1__C1**, **A2__B2__C2**, **A3__B3__C3** 

Notes:
- the variables names pop-up by hoovering with the mouse.
- by default, distribution are computed based on a random sample of max 100 samples (using python `random.sample()`)

## Example
 
The metadata table in test/metadata/metadata.tsv containg 267 dummy samples and 9 variables, the columns are:

- `#SampleID`: sample name
- `num_1`: valid numeric variable
- `num_2`: valid numeric variable
- `num_3`: valid numeric variable
- `num_nan`: numeric variable also containing missing data (np.nan)
- `cat_1`: valid categorical variable, 2 factors:
  - cat_A: 107
  - cat_B: 160
- `cat_2`: valid categorical variable, 3 factors:
  - cat_2A: 33 samples
  - cat_2B: 104 samples
  - cat_2C: 130 samples
- `nan_only`: np.nan only variable
- `num_cat_valid`: mixture of 260 numeric values and 7 non-numeric, "avoidable" values, including: 
  - Not applicable: 4 samples
  - Unknown: 3 samples
- `num_cat`: mixture, include 260 numeric values and 8 non-numeric, "unavoidable" values, including:
  - Not applicable: 4 samples
  - **invalid_term: 2 samples**
  - Unknown: 2 samples

Running 
 
```
 Xplor_distros -m Xplor_distros/tests/metadata/metadata.tsv -o Xplor_distros/tests/metadata/metadata.html -p cat_1 -p cat_2 --merge
```

Will output the .html file in `Xplor_distros/tests/output/metadata.html` 

## Errors messages

Check the standard output (your screen) for message indicating what 
could have gone wring or need your attention, example:
 
```
Xplor_distros \
    -m Xplor_distros/tests/metadata/metadata.tsv 
    -o Xplor_distros/tests/metadata/metadata.html \
    -p cat_1 -p num_1 --merge -s 2 -n 10000

[not categorical]
Xplor_distros/tests/metadata/metadata.tsv
 - num_1
[not enough samples]
Xplor_distros/tests/metadata/metadata.tsv
 - cat_A samples for factor 107.0
 - cat_B samples for factor 160.0
```


 
```
Xplor_distros \
    -m Xplor_distros/tests/metadata/metadata.tsv \
    -o Xplor_distros/tests/metadata/metadata.html \
    -p cat_1 -p cat_2 --merge -s 2

[too many factors]
Xplor_distros/tests/metadata/metadata.tsv
 - variable cat_1__cat_2 has 4 factor (max 2 [options "-s"])
```


 
```
$ Xplor_distros \
    -m Xplor_distros/tests/metadata/metadata.tsv \
    -o Xplor_distros/tests/metadata/metadata.html \
    -p cat_1 -p numy --merge -s 2

[not in]
Xplor_distros/tests/metadata/metadata.tsv
 - numy
```


## Usage

```
Usage: Xplor_distros [OPTIONS]

Options:
  -m, --m-metadata-file TEXT      Metadata file(s) containing numeric
                                  valriables (to plot) and categorical
                                  variables (to stratify).  [required]
  -p, --p-stratify TEXT           Categorical variables to use for
                                  stratification.
  -s, --p-max-strata INTEGER      Maximum number of stratification to create
                                  (Some categorical variables may contain a
                                  high number of categories and you may not
                                  want hundreds of panels per variable, and
                                  for each metadata file...).  [default: 20]
  -n, --p-number-of-samples INTEGER
                                  Number of samples to randomly select to
                                  compute the distributions.  [default: 100]
  -o, --o-distributions TEXT      Output visualization file.  [required]
  --merge / --no-merge            Merge multiple stratification variables. For
                                  example, if 'sex' and 'wine_consumed' are
                                  passed: use their combined factors:
                                  'Male__Yes', 'Female__Yes', 'Male_No',
                                  'Female__No'.  [default: False]
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

### Bug Reports

contact `flejzerowicz@health.ucsd.edu`