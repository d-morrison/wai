# Theorem Examples

Code

Published

Last modified: 2026-07-14 09:48:50 (PDT)

This chapter demonstrates all the theorem-like environments available through the `callouty-theorem` and `custom-callout` extensions.

# 1 Theorems

> **NOTE:**
>
> **Theorem 1 (Pythagorean Theorem)** In a right triangle with legs of length \\a\\ and \\b\\ and hypotenuse of length \\c\\, we have: \\a^2 + b^2 = c^2\\

See [Theorem 1](#thm-pythagorean) for the famous Pythagorean theorem.

# 2 Lemmas

> **NOTE:**
>
> **Lemma 1 (Fundamental Lemma)** Every non-empty subset of \\\mathbb{N}\\ has a smallest element.

The result in [Lemma 1](#lem-fundamental) is used to prove many theorems in number theory.

# 3 Corollaries

> **NOTE:**
>
> **Corollary 1 (Rational Root Test Corollary)** If \\p/q\\ is a rational root of the polynomial \\a_n x^n + \cdots + a_1 x + a_0\\ with integer coefficients, then \\p\\ divides \\a_0\\ and \\q\\ divides \\a_n\\.

[Corollary 1](#cor-rational-root) follows directly from the Rational Root Theorem.

# 4 Propositions

> **NOTE:**
>
> **Proposition 1 (Triangle Inequality)** For any real numbers \\x\\ and \\y\\: \\\|x + y\| \leq \|x\| + \|y\|\\

The triangle inequality ([Proposition 1](#prp-triangle-inequality)) is fundamental in analysis.

# 5 Conjectures

> **NOTE:**
>
> **Conjecture 1 (Goldbach’s Conjecture)** Every even integer greater than 2 can be expressed as the sum of two prime numbers.

[Conjecture 1](#cnj-goldbach) remains one of the oldest unsolved problems in number theory.

# 6 Definitions

> **NOTE:**
>
> **Definition 1 (Derivative)** The derivative of a function \\f\\ at a point \\x\\ is defined as: \\f'(x) = \lim\_{h \to 0} \frac{f(x+h) - f(x)}{h}\\ provided this limit exists.

See [Definition 1](#def-derivative) for the formal definition of a derivative.

# 7 Examples

> **NOTE:**
>
> **Example 1 (Solving a Quadratic Equation)** Solve \\x^2 - 5x + 6 = 0\\.
>
> We can factor this as \\(x-2)(x-3) = 0\\, so the solutions are \\x = 2\\ and \\x = 3\\.

[Example 1](#exm-quadratic) shows how to solve a simple quadratic equation.

# 8 Exercises

> **NOTE:**
>
> **Exercise 1 (Integration Practice)** Compute the following integral: \\\int_0^1 x^2 \\ dx\\

Try [Exercise 1](#exr-integration) to practice basic integration.

# 9 Proofs

> **NOTE:**
>
> *Proof* (Proof of the Pythagorean Theorem). Consider a square with side length \\a+b\\. We can divide this square into four right triangles and a central square with side length \\c\\.
>
> The area equations show: \\a^2 + b^2 = c^2\\

> **NOTE:**
>
> *Proof* (Proof that the derivative of a constant is zero). Let \\f(x) = c\\ for some constant \\c\\. Then \\f'(x) = 0\\.

# 10 Solutions

> **NOTE:**
>
> *Solution 1* (Solution to Exercise on Integration). We use the power rule for integration: \\\int_0^1 x^2 \\ dx = \left\[\frac{x^3}{3}\right\]\_0^1 = \frac{1}{3}\\

> **NOTE:**
>
> *Solution* (Alternative Solution to Quadratic Equation). For the quadratic equation, we can use the quadratic formula: \\x = \frac{5 \pm 1}{2}\\
>
> This gives us \\x = 3\\ or \\x = 2\\.

# 11 Remarks

> **NOTE:**
>
> *Remark 1* (Convergence Note). The limit in [Definition 1](#def-derivative) may not exist for all functions at all points. For example, the absolute value function \\\|x\|\\ is not differentiable at \\x=0\\.

[Remark 1](#rem-convergence) highlights an important limitation of the derivative definition.

# 12 Mixed Example with Theorem and Solution

Here’s an example that combines multiple theorem types:

> **NOTE:**
>
> **Theorem 2 (Mean Value Theorem)** If \\f\\ is continuous on \\\[a,b\]\\ and differentiable on \\(a,b)\\, then there exists a point \\c \in (a,b)\\ such that: \\f'(c) = \frac{f(b) - f(a)}{b - a}\\

> **NOTE:**
>
> **Exercise 2 (Applying the Mean Value Theorem)** Let \\f(x) = x^2\\ on \\\[0, 2\]\\. Find the value of \\c\\ guaranteed by the Mean Value Theorem ([Theorem 2](#thm-mean-value)).

> **NOTE:**
>
> *Solution 2* (Solution to Mean Value Theorem Exercise). We have \\f(x) = x^2\\, so \\f'(x) = 2x\\.
>
> By the Mean Value Theorem: \\f'(c) = \frac{f(2) - f(0)}{2 - 0} = \frac{4 - 0}{2} = 2\\
>
> Since \\f'(c) = 2c\\, we need: \\2c = 2\\ \\c = 1\\
>
> Therefore, \\c = 1\\ is the value guaranteed by the Mean Value Theorem.

# References

Back to top
