# cursed-toggle
This library is intended to implement a toggle function for Boolean values in a very bad or even the worst and most unmaintainable way, following the KISS ("Keep it sophisticated, specialist!") principle.

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

# The complication
## Midamble
Not even sure whether this is a word. Anyway, after each modification, there should be a $\LaTeX$-like representation of the "math" and after, the correspdoning python syntax (needed for testing this readme).

## The complication, take 2. Or take 1?. We should satisfy both index people. Take 2, Take 1, Take 0, Go!
The start function looks too negative and too simple. Let's make it positve and more complex, because $i^2 = -1$

$$ f(b) = 1 + i^2 \cdot b $$
```
f(b) = 1 + 1j**2 * b
```

The single lonely 1 in the beginning is also a bit boring. And since $e^{i\pi} + 1 = 0$, we know what to do.

$$ f(b) = -e^{i\pi} + i^2 \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**2 * b
```

Square 2. Two. 2 is 2 lame. Shifting 1234567 19 times to the right is also two. So, we will rightshift it 13 and 6 times.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> 6} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> 6) * b
```

$3! = 6$, so let's get rid of the 6.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> 3!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> math.factorial(3)) * b
```

During my research, I stumbled across the DRY-principle, that means "Do repeat yourself" or "duplication is excellent". Here we go with the Euler's idendity. For the 3. Three. Times.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> \left(-e^{i\pi} - e^{i\pi} - e^{i\pi}\right)!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> math.factorial(int((-math.e**(1j * math.pi) - math.e**(1j * math.pi) - math.e**(1j * math.pi)).real))) * b
```
