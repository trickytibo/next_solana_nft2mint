from which_solana_nft.howrareis import *
from which_solana_nft.twitterFollowersCount import *
from which_solana_nft.createPage import *
import argparse

file_howrareis='howrareis_source.json'
file_howareis_reformated='howrareis_reformated.json'

def main():
    r = getDataFromhowrareis(file_howrareis=file_howrareis, file_howareis_reformated=file_howareis_reformated)
    execute = r.executeTask()
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--top', type=int, help="nb of elements to display.", default=10)
    parser.add_argument('--period', type=int, help="the number of days to analyse from now.", default=14)
    # Parse the argument
    args = parser.parse_args()
    top=args.top
    period=args.period
    # Print "Hello" + the user input argument
    # r = createHtmlPagefromJSON(inputfile=file_howareis_reformated, nbElements2display=10, period2parse=9)
    r = createHtmlPagefromJSON(inputfile=file_howareis_reformated, nbElements2display=top, period2parse=period)
    r.buildHtmlPage()

if __name__ == "__main__":
    main()