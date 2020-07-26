import argparse
import sys
import string

parser = argparse.ArgumentParser()
parser.add_argument('-first',
                    '--start_letter',
                    type=str,
                    default='a',
                    help='choose first year of data to scrap')
parser.add_argument('-last',
                    '--end_letter',
                    type=str,
                    default='z',
                    help='choose last year of data to scrap')
args = parser.parse_args()

letters = string.ascii_lowercase
FIRST_LETTER = args.start_letter.lower()
LAST_LETTER = args.end_letter.lower()

# Checking that FIRST_LETTER and LAST_LETTER are alphabet letters
try:
    assert (FIRST_LETTER.isalpha())
    assert (LAST_LETTER.isalpha())
except AssertionError:
    print("Please enter a valid letter")
    sys.exit()

range_alphabet = letters[letters.find(FIRST_LETTER): letters.find(LAST_LETTER) + 1]