# cursed-toggle
This library is intended to implement a toggle function for Boolean values in a very bad or even the worst and most unmaintainable way, following the KICS (Keep it complicated, specialist) principle.

# Preamble
The variable `b` can be True (1) or False (0). One of the most basic implementation to get a toggle is
```
f(b) = not b
```
But this is way too simple and efficient and something cooler looking might be
```
f(b) = b^1
```
A trivial linear function is also possible
```
f(b) = 1 - b
```
and this sounds like a good start.
