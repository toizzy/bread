# BREAD

This repository contains **BREAD** (**B**oilerplate and **R**edundancy
**E**valuation on **A**ssorted **D**ocuments), as well as the canonical script
to score it. It also contains a simple implementation of the **CRED**
(**C**haracter **Red**undancy) scores to measure data quality and filter data.

More details are in [Separating the Wheat from the Chaff with BREAD: An
open-source benchmark and metrics to detect redundancy in
text](https://arxiv.org/abs/2311.06440).

NOTE: this is cloned from 

## The Breadwinners

The best classifiers according to the limited gridsearch we did in the paper are
presented here. For details on the parameters, please look in breadwinners.py.

According to these tables, the best score may appear to be the `sodabread`
score, which is based on the second moment of the frequency. However, be advised
that moment-based results had a slightly higher variance and lower mean on
average than Zipfianness-based methods for BREAD-noisy (Figure 2 in the paper),
so there is some possibility that the high scores of `sodabread` may have more
noise than those of `pumpernickel` and `vollkorn`.


#### Test results

classifier   | split | bread slice | score
------------ | ----- | ----------- | ------
Pumpernickel | test  | noisy       | 85.53%
Vollkorn     | test  | noisy       | 85.45%
Sodabread    | test  | noisy       | 87.92%
Wonderbread  | test  | noisy       | 79.62%

classifier   | split | bread slice | score
------------ | ----- | ----------- | ------
Pumpernickel | test  | repeat      | 94.12%
Vollkorn     | test  | repeat      | 93.69%
Sodabread    | test  | repeat      | 94.33%
Wonderbread  | test  | repeat      | 90.05%

#### Tune results

classifier   | split | bread slice | score
------------ | ----- | ----------- | ------
Pumpernickel | tune  | repeat      | 95.64%
Vollkorn     | tune  | repeat      | 94.73%
Sodabread    | tune  | repeat      | 95.68%
Crouton  | tune  | repeat      | 92.49%

classifier   | split | bread slice | score
------------ | ----- | ----------- | ------
Pumpernickel | tune  | noisy       | 87.11%
Vollkorn     | tune  | noisy       | 86.17%
Sodabread    | tune  | noisy       | 88.32%
Crouton  | tune  | noisy       | 81.87%

## Usage

Please see `demo.py`. Also please note that if you use this on a large dataset,
you may want to re-implement these scores (possibly in C++) for efficiency.

## The Code

The files in this repository are as follows:

-   `cred.py`: implementations of the different CRED scores, including Moment,
    Zipfianness, and TTR
-   `breadwinners.py`: Implementations of the best parameter settings from the
    paper
-   `get_bread_benchmark_table.py`: code to score BREAD with functions in
    `breadwinners` and output the table above
-   `bread.tsv`: the raw data for the BREAD benchmark.
-   `demo.py`: demonstration of how to use CRED scores
-   `README.md`: This file.

This not optimized code. If anyone wants to reimplement it in a faster way, or
in a different programming language, that would be welcome.
