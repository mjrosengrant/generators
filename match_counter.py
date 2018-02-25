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

    sequence_length = 40000000

    print 'Generating sequences'
    t0 = time.time()
    list_a = generate_sequence(start_a, factor_a, sequence_length=sequence_length)
    list_b = generate_sequence(start_b, factor_b, sequence_length=sequence_length)
    t1 = time.time()
    generation_time = t1 - t0

    print 'Counting matches.'
    t0 = time.time()
    match_count = get_match_count(list_a, list_b)
    t1 = time.time()
    match_algorithm_time = t1 - t0

    print '%d sequence length' % sequence_length
    print '%s matches found' % str(match_count if match_count else 0)
    print 'Sequences generated in %s seconds' % str(generation_time)
    print 'Matches found in %s seconds' % str(match_algorithm_time)


def generate_sequence(start_val, factor, sequence_length=5):
    """Create a sequence of numbers using the generator."""
    generated_list = []
    value = start_val
    for i in range(sequence_length):
        value = generator(value, factor)
        binary_value = get_binary_value(value)
        generated_list.append(binary_value)
    return generated_list


def generator(start_val, factor):
    """The generators both work on the same principle.

    To create its next value, a generator will take the previous
    value it produced, multiply it by a factor, and then keep the
    remainder of dividing that resulting product by 2147483647.
    """
    return (start_val * factor) % 2147483647


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
