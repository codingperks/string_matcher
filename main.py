# String Matcher

'''
    Author =  Ryan Perkins
    Date of Creation: 01/06/22
    Date of last edit: 18/08/22
    Description: This script takes a folder of .csv files and performs absolute and fuzzy matching on a list of columns
        and exports csv files with corresponding columns containing results
'''

# Import modules
import pandas as pd
from thefuzz import fuzz    # used for fuzzy matching
import glob


# Defining Search class
class Search:
    def __init__(self):
        self.case = case
        self.lowercase = lowercase
        self.df = pd.read_csv(chosen_csv)    # Import data here, update filename with final

    # Import data and set up dataframe
    def import_setup(self):
        colnames = ["QE1", "QE2"] # column names
        self.df = self.df[colnames]  # filter dataset to open-answer columns
        self.df = self.df.rename(columns={self.df.columns[0]: 'QE1'})
        self.df = self.df.rename(columns={self.df.columns[1]: 'QE2'})
        self.df = self.df.reindex(columns=list(['QE1', 'QE1absolute',
                                                'QE1fuzzyratio', 'QE1fuzzyword', 'QE1fuzzyratio_2', 'QE1fuzzyword_2',
                                                'QE2', 'QE2absolute',
                                                'QE2fuzzyratio', 'QE2fuzzyword', 'QE2fuzzyratio_2', 'QE2fuzzyword_2']),
                                  fill_value="")    # Create output dataframe

    # Absolute matching
    # Evaluates TRUE if search terms are found
    def absolute_match(self):
        self.df['QE1absolute'] = self.df['QE1'].str.contains(r'(?:{})'.format('|'.join(lowercase)), case=False) | \
                                 self.df['QE1'].str.contains(r'(?:{})'.format('|'.join(case)))
        self.df['QE2absolute'] = self.df['QE2'].str.contains(r'(?:{})'.format('|'.join(lowercase)), case=False) | \
                                 self.df['QE2'].str.contains(r'(?:{})'.format('|'.join(case)))

    # Fuzzy matching
    # Partial ratio matching, produces a ratio of % match, reports the highest matching ratio and search term
    def fuzzy_match(self):
        for index, row in self.df.iterrows():
            fuzz_rank_1 = {}  # Create dictionaries to store highest score
            fuzz_rank_2 = {}
            for string in case:
                dictionary_update_1 = {string: (fuzz.partial_ratio(row['QE1'], string))}
                fuzz_rank_1.update(dictionary_update_1)
                dictionary_update_2 = {string: (fuzz.partial_ratio(row['QE2'], string))}
                fuzz_rank_2.update(dictionary_update_2)
            for string in lowercase:
                dictionary_update_1 = {string: (fuzz.partial_ratio(row['QE1'], string))}
                fuzz_rank_1.update(dictionary_update_1)
                dictionary_update_2 = {string: (fuzz.partial_ratio(row['QE2'], string))}
                fuzz_rank_2.update(dictionary_update_2)

            # Sorting fuzzy ratios and words by ratio value
            rank_1_sorted = sorted(fuzz_rank_1.items(), key=lambda item: item[1])
            rank_2_sorted = sorted(fuzz_rank_2.items(), key=lambda item: item[1])

            # QE1 First and second rank fuzzy ratios and words
            rank_1_sorted_1st = (rank_1_sorted[-1])
            rank_1_sorted_2nd = (rank_1_sorted[-2])
            self.df.at[index, 'QE1fuzzyratio'] = rank_1_sorted_1st[1]
            self.df.at[index, 'QE1fuzzyword'] = rank_1_sorted_1st[0]
            self.df.at[index, 'QE1fuzzyratio_2'] = rank_1_sorted_2nd[1]
            self.df.at[index, 'QE1fuzzyword_2'] = rank_1_sorted_2nd[0]

            # QE2 First and second rank fuzzy ratios and words
            rank_2_sorted_1st = (rank_2_sorted[-1])
            rank_2_sorted_2nd = (rank_2_sorted[-2])
            self.df.at[index, 'QE2fuzzyratio'] = rank_2_sorted_1st[1]
            self.df.at[index, 'QE2fuzzyword'] = rank_2_sorted_1st[0]
            self.df.at[index, 'QE2fuzzyratio_2'] = rank_2_sorted_2nd[1]
            self.df.at[index, 'QE2fuzzyword_2'] = rank_2_sorted_2nd[0]

        # Deletes word if ratio is 0
        self.df.loc[self.df['QE1fuzzyratio'] == 0, 'QE1fuzzyword'] = ""
        self.df.loc[self.df['QE2fuzzyratio'] == 0, 'QE2fuzzyword'] = ""
        self.df.loc[self.df['QE1fuzzyratio_2'] == 0, 'QE1fuzzyword_2'] = ""
        self.df.loc[self.df['QE2fuzzyratio_2'] == 0, 'QE2fuzzyword_2'] = ""

    # Export results to csv
    def export_results(self):
        export_folder = 'results'
        start = "/"
        end = "/csv"
        filename = chosen_csv[chosen_csv.find(start)+len(start):chosen_csv.rfind(end)]
        self.df.to_csv(export_folder + "/" + filename + "_results.csv")


if __name__ == '__main__':
    # Search lists
    # Read search list from .txt file
    with open('search.txt', encoding="utf-8") as f:
        start = "["
        end = "]"
        search_lines = f.readlines()
        lowercase = []
        case = []
        for line in search_lines:
            if line.startswith('lowercase = ['):
                lowercase_words = (line[line.find(start) + len(start):line.rfind(end)])
                lowercase = lowercase_words.split(', ')
            if line.startswith('case = ['):
                case_words = (line[line.find(start) + len(start):line.rfind(end)])
                case = case_words.split(', ')
        print(lowercase)
        print(case)

    # Read all csv files in folder
    input_folder = 'input'
    csv_files = glob.glob((input_folder + '/*.csv'))

    # Functions
    for chosen_csv in csv_files:
        print(chosen_csv)
        search = Search()
        search.import_setup()
        search.absolute_match()
        search.fuzzy_match()
        search.export_results()
        print('Exported')

# Authorship metadata
__author__ = "Ryan Perkins"
__copyright__ = "Copyright-free"
__credits__ = ["Ryan Perkins"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Ryan Perkins"
__email__ = "r.perkins925@gmail.co.uk"
__status__ = "Production"
