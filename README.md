# association-rule-mining
## Description 
In this project I implement a simplified version of the A-Piori association rule mining algorithm using Python. The A-Priori algorithm utilizes the subset property for frequent itemsets, enabling significant pruning of the space of possible itemset combinations. The program takes 4 parameters:
- `input_filename`
- `output_filename` this name is up to the user
- `min_support_percentage` the support percentage (expressed as a floating number between 0 and 1 with 4 decimal points) for the specific frequent itemset or for the specific association rule (and both should be above the user-specified min_support_percentage) e.g., 0.05, 0.4, 0.5 are used to denote 5%, 40%, and 50% respectively. You should not include a percent symbol.
- `min_confidence` should be the confidence percentage (expressed as a floating number between 0 and 1 with 4 decimal points) for the specific association rule (and should be above the user-specified min_confidence) e.g., 0.05, 0.4, 0.5 are used to denote 5%, 40%, and 50% respectively. You should not include a percent symbol.

An example call would look like: `python armin.py input.csv output.csv 0.5 0.7`

Example input files are included in the repository.
