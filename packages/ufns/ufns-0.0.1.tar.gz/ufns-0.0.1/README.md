# ufns

Utility functions for Python

linspace(a, b, l, r)

- generates a list of length l of evenly spaced values between a and b
- rounds values to r decimal places, can be left blank if desired
- leaving l blank will generate a values differing by 1 if the difference
  between a and b is whole, or else will set the length to 100

gen(l, a, b)

- generates a list of length l of random integers between a and b

gen(l, list, allowDuplicates)

- generates a list of length l of random values picked from an iterable (in this case the iterable is list)
- iterable should not be passed as a string
- setting allowDuplicates to False will populate the list with unique values,
  leaving blank or setting to True will add duplicate values to the list

lininc(a, b, i)

- generates a list of values from a to b, in increments of i

ordmag(n)

- returns the power that 10 is raised to when n is expressed in scientific notation
