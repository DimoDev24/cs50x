import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Error: Incorrect number of comand-line arguments.")
        sys.exit()

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        database = list(reader)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txtfile:
        sequence = txtfile.read()

    # TODO: Find longest match of each STR in DNA sequence
    matches = {}

    for i in database[0]:
        matches[i] = (longest_match(sequence, i))

    # TODO: Check database for matching profiles
    name = "No match"
    name_counter = 1

    for i in range(len(database)):
        for j in matches:
            if str(matches[j]) == database[i][j]:
                name_counter += 1

        if name_counter == len(matches):
            name = database[i]['name']
            break
        else:
            name_counter = 1

    print(name)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
