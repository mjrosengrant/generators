"""Command line script to calculate matches based on description on the following site.

https://gist.github.com/lukechampine/75141db4bcb2efc53f14dbb7e0263634
"""
import numpy as np
import sys
import time


def main(argv):
    """Generate sequences, and identify matches between them."""
    start_a = 65
    factor_a = 16807

    start_b = 8921
    factor_b = 48271

    # For simplicity, ensure subset_size can divide the sequence_length evenly
    sequence_length = 40000000
    subset_size = 1000000

    total_matches = 0
    generation_time = 0
    match_algorithm_time = 0

    most_recent_a = start_a
    most_recent_b = start_b
    # Perform calculation in multiple iterations of subset_size, so that full sequence
    # does not need to be stored in memory at the same time.
    for i in range(sequence_length / subset_size):
        generation_t0 = time.time()
        a_sequence = generate_sequence(most_recent_a, factor_a, subset_size)
        b_sequence = generate_sequence(most_recent_b, factor_b, subset_size)
        # Save the last value of each sequence to use as start_val in the next iteration.
        most_recent_a = a_sequence[-1]
        most_recent_b = b_sequence[-1]
        # Now that we have the most recent values, convert sequences to binary.
        a_sequence = convert_to_binary(a_sequence)
        b_sequence = convert_to_binary(b_sequence)
        generation_t1 = time.time()

        # Calculate matches in subset, and add to total_matchs.
        counting_t0 = time.time()
        new_matches = get_match_count(a_sequence, b_sequence)
        total_matches += new_matches
        counting_t1 = time.time()

        # Update accumulated time spent on each step
        generation_time += generation_t1 - generation_t0
        match_algorithm_time += counting_t1 - counting_t0

    print '%d sequence length' % sequence_length
    print '%s matches found' % str(total_matches if total_matches else 0)
    print 'Sequences generated in %s seconds' % str(generation_time)
    print 'Matches found in %s seconds' % str(match_algorithm_time)


def generate_sequence(start_val, factor, sequence_length=5):
    """Create a sequence of numbers using the generator."""
    generated_list = []
    value = start_val
    for i in range(sequence_length):
        value = generator(value, factor)
        generated_list.append(value)
    return generated_list


def generator(start_val, factor):
    """The generators both work on the same principle.

    To create its next value, a generator will take the previous
    value it produced, multiply it by a factor, and then keep the
    remainder of dividing that resulting product by 2147483647.
    """
    return (start_val * factor) % 2147483647


def convert_to_binary(integer_array):
    """Convert integer to the binary value we are looking for."""
    for i in range(len(integer_array)):
        integer_array[i] = get_binary_value(integer_array[i])
    return integer_array


def get_match_count(list_a, list_b):
    """Find matches between list_a and list_b."""
    np_list_a = np.array(list_a)
    np_list_b = np.array(list_b)
    return np.count_nonzero(np_list_a == np_list_b)


def get_binary_value(integer):
    """Accept an integer and returns least significant 16 binary digits."""
    return bin(integer)[-16:]

if __name__ == "__main__":
    main(sys.argv[1:])
