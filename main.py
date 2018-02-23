# https://gist.github.com/lukechampine/75141db4bcb2efc53f14dbb7e0263634
"""
In front of you are a pair of generators, generator A and generator B.

That produce an infinite sequence of numbers.

The generators both work on the same principle. To create its next value, a
generator will take the previous value
it produced, multiply it by a factor (generator A uses 16807;
generator B uses 48271),

and then keep the remainder of dividing that resulting product by 2147483647.
That final remainder is the value it produces next.

To calculate each generator's first value, it instead uses a specific starting
value as its "previous value."

For example, suppose that for starting values, generator A uses 65, while
generator B uses 8921. Then, the first five pairs of generated values are:

    --Gen. A--  --Gen. B--
       1092455   430625591
    1181022009  1233683848
     245556042  1431495498
    1744312007   137874439
    1352636452   285222916

Your task is to count the number of pairs that "match" among the
first 40 million pairs.
A pair is said to match if the least significant 16 bits of both values match.

For example, the pairs above in binary are (with generator A's value first in
each pair):

    00000000000100001010101101100111
    00011001101010101101001100110111

    01000110011001001111011100111001
    01001001100010001000010110001000

    00001110101000101110001101001010
    01010101010100101110001101001010

    01100111111110000001011011000111
    00001000001101111100110000000111

    01010000100111111001100000100100
    00010001000000000010100000000100

Here, you can see that the least significant (here, rightmost) 16 bits of the
third value match: 1110001101001010. None of the other pairs match, so after
processing these five pairs, your count would be 1.

After processing the full set of 40 million pairs using the starting values of
65 and 8921, your count would be 588.

Write a program that prints the number of matching pairs among the first
40 million pairs, for arbitrary starting values. Your program does not
need to accept the starting values as input;
they just need to be defined somewhere, e.g.

const startA = 65
const startB = 8921
You may write your program in any language.
"""
import time


def main():
    """Solve main problem."""
    start_a = 65
    factor_a = 16807

    start_b = 8921
    factor_b = 48271

    SEQUENCE_LENGTH = 5

    a = generate(start_a, factor_a, sequence_length=SEQUENCE_LENGTH)
    b = generate(start_b, factor_b, sequence_length=SEQUENCE_LENGTH)

    match_count = get_match_count(a, b)
    print '%s matches found' % str(match_count if match_count else 0)


def generate(start_val, factor, sequence_length=5):
    """Create a sequence of numbers using the generator.

    Default sequence_length is 5.
    """
    generated_list = []
    value = start_val

    for i in range(sequence_length):
        value = generator(value, factor)
        generated_list.append(value)
    return generated_list


def generator(start_val, factor):
    """The generators both work on the same principle.

    To create its next value, a generator will take the previous
    value it produced,
    multiply it by a factor (generator A uses 16807; generator B uses 48271),
    and then keep the remainder of dividing that resulting product by
    2147483647.
    That final remainder is the value it produces next.
    """
    return (start_val * factor) % 2147483647


def get_match_count(list_a, list_b):
    """Brute force check to find matches between list_a and list_b.
    Your task is to count the number of pairs that "match" among the

    first 40 million pairs.
    A pair is said to match if the least significant 16 bits of both
    values match.
    """
    match_count = 0
    for number_a in list_a:
        for number_b in list_b:
            if is_match(number_a, number_b):
                match_count = match_count + 1
    return match_count


def is_match(int_a, int_b):
    """Criteria for a match.

    Considered a match if last 16 bits of information are equal

    1. Convert to binary
    2. Check if least significant 16 bits are equal.
    """
    sig_figs = 5
    a_sig_figs = bin(int_a)[-sig_figs:]
    b_sig_figs = bin(int_b)[-sig_figs:]

    if a_sig_figs == b_sig_figs:
        return True
    return False

main()
