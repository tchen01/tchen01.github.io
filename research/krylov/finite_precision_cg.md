% The Conjugate Gradient Algorithm in Finite Precision
% Tyler Chen

This page is a work in progress.

A key component of our derivations of the [Lanczos](./arnoldi_lanczos.html) and [Conjugate Gradient](./cg_derivation.html) methods was the orthogonality of certain basis vectors.
In finite precision, our induction based arguments no longer hold, and so it's reasonable to expect the algorithms will fail.
That said, since you're reading about these methods, they must somehow still be usable in practice.
This turns out to be the case, and both methods are widely used for eignevalue problems and solving linear systems.

The first major progress in the analysis of the Lanczos algorithm was done by Chris Paige, who characterized the behavior of the method in finite precision. 
A similarly important analysis of Conjugate Gradient was done by Anne Greenbaum in her 1989 paper, ["Behavior of slightly perturbed Lanczos and conjugate-gradient recurrences"](https://www.sciencedirect.com/science/article/pii/0024379589902851).
A big takeaway from Greenbaum's analysis is that the error bound from the Chevyshev polynomials still holds in finite precision (to a close approximation).
My goal here is to present the highlights of that paper.

## The results


## Some conditions for the analysis
It turns out that CG is doing the Lanczos algorithm in disguise. In particular, normalizing the residuals from CG gives the vectors $q_j$ produced by the Lanczos algorithm, and combing the CG constants in the right way gives the coefficients for the three term Lanczos recurrence.

The analysis by Greenbaum requires that the finite precision Conjugate Gradient algorithm (viewed as the Lanczos algorithm) satisfy a few properties.
Namely,

- the three term Lanczos recurrence is well satisfied
- the Lanczos vectors have norm close to one
- successive Lanczos vectors are nearly orthogonal

As it turns out, nobody has actually ever proved that any of the Conjugate Variant methods used in practice actually satisfy these conditions (although some do numerically satisfy the conditions).

