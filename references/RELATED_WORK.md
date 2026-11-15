# Related work and the surviving contribution

The task is to compile ordinary uses of an unknown unital channel into a physical channel close to a unitary encoding its Liouville matrix. The output must act coherently on arbitrary data and reference systems. The contribution is a dimension-optimal operational characterization at fixed precision: a marginal-sensitive construction gives $`\widetilde O(d^2/\delta)`$ ordinary queries, and a reduction to universal unitary inversion gives $`\Omega(d^2)`$ for constant-normalization blocks at fixed sufficiently small error. The precision dependence is not matched.

## The closest channel-spectral construction

Niwa, Rossi, Taranto and Murao, *Singular value transformation for unknown quantum channels*, [arXiv:2506.24112v3](https://arxiv.org/pdf/2506.24112v3), published as [PRA 114, L030401 (2026)](https://doi.org/10.1103/321q-k5dh), provide the central construction being refined. Their Theorem 1 converts ordinary channel queries into an approximate unitary block encoding of the Hermitian dilation of the Liouville matrix. The construction forms controlled-SWAP Choi states, exponentiates their partial transposes, combines the resulting evolutions, and converts a sine block to the desired block with an arcsine polynomial. These ingredients, their use of unitality to permit constant normalization, and the resulting route to singular-value transformations are inherited here.

Their current Theorem 1 has query cost

```math
O\!\left(\frac{d^{2k+1}}\delta
\log^2\frac1\delta\right),\qquad
H=\frac1{2d^{1-k}}
\begin{pmatrix}0&L_{\mathcal E}\\L_{\mathcal E}^{\dagger}&0\end{pmatrix}.
```

For unital channels, $`k=1`$ supplies constant normalization and gives the $`\widetilde O(d^3/\delta)`$ comparison. Keeping the fixed program marginal in the collision estimate removes one factor of $`d`$ for this promise. The present lower bound then shows that the improved power of dimension is necessary already on the unitary subset, including for a single forward use of the compiled block channel.

Version history matters to this comparison. [Version 1, dated 30 June 2025](https://arxiv.org/pdf/2506.24112v1), already displayed a $`\widetilde O(d^2/\delta)`$ constant-normalization scaling and a $`d^{2k}`$ prefactor in Theorem 1. [Version 2, dated 15 July 2025](https://arxiv.org/pdf/2506.24112v2), changed the prefactor to $`d^{2k+1}`$; the published version retains it. Thus the present scaling is not its first appearance in a preprint. The claim here is a justified unital-case refinement together with its operational dimension lower bound; the earlier, superseded prefactor is not used as an established generic-channel theorem.

The current paper's Appendix D lower bound also has a relevant restriction. Its hard family in Eq. (D13) contains a trace-and-prepare reset on $`n-1`$ qubits, and is not unital. Its general-channel $`\Omega(dt^2/\delta)`$ conclusion does not by itself yield the unital lower bound needed here. The [dimension lower-bound proof](../science/dimension-lower-bound.md) instead uses unitary channels and the modern robust inversion theorem.

## Moment-sensitive exponentiation and the inherited variance estimate

Wei, Liu, Liu, Han, Deng and Liu, *Simulating non-completely positive actions via exponentiation of Hermitian-preserving maps*, [npj Quantum Information 10, 134 (2024)](https://doi.org/10.1038/s41534-024-00949-z), introduced the HME interaction for exponentiating a Hermitian-preserving linear image of an unknown program state. The corresponding preprint is [arXiv:2308.07956v1](https://arxiv.org/pdf/2308.07956v1), under the earlier title *Realizing Non-Physical Actions through Hermitian-Preserving Map Exponentiation*.

Their general sample bound uses the norm of the joint interaction. Appendix C2 goes further for partial transposition: Proposition 3 improves the bound to $`O(d_A t^2/\epsilon)`$, and Eq. (C17) explicitly retains

```math
d_A\Vert\mathrm{Tr}_B\rho\Vert_\infty
```

before bounding it by $`d_A`$. Their convolution inequality and parity analysis already exhibit the relevance of reduced program states. The present account therefore credits marginal-sensitive exponentiation to this prior work; it does not introduce that observation as a new principle.

The all-time collision estimate used here is also inherited. The public proof in [*Collective Quantum Programming*, `science/collision_bound.md`, revision `0fefb607599f9c864918ed1ab58a778fe5b50cf1`](https://github.com/GoGoKo699/Collective-Quantum-Programming/blob/0fefb607599f9c864918ed1ab58a778fe5b50cf1/science/collision_bound.md) establishes

```math
\Vert\Phi_\tau-\mathrm{Ad}_{e^{-i\tau h}}\Vert_\diamond
\le2\tau^2
\left\Vert\mathcal E_\sigma(V^2)
-\mathcal E_\sigma(V)^2\right\Vert_\infty,
\qquad h=\mathcal E_\sigma(V),
```

for every real $`\tau`$, using a purification isometry and a leakage decomposition. Its original application programs collective reflections from specimens of a flat-rank state. Here the program comes from one ordinary use of a black-box channel, the required output encodes the channel's Liouville action, and the matching dimension obstruction concerns live channel queries. The shared variance lemma is credited once; its specialization and the operational frontier are the present task.

## Robust unitary inversion as the lower-bound input

Chen, Yu and Zhang, *Approximation does not help in quantum unitary time-reversal*, [arXiv:2507.05736v4](https://arxiv.org/pdf/2507.05736v4), STOC 2026, prove that every $`q`$-query inverse-producing strategy has Haar-averaged channel fidelity at most $`(q+1)/d^2`$ (Theorem 3.7). This is the external theorem behind the lower bound, rather than a new inversion lower bound.

For a unitary channel, the Hermitian Liouville dilation contains $`U^{\dagger}\otimes U^{\mathsf T}`$. A designated block with constant amplitude $`c`$ consequently supplies the inverse on its successful branch. Completing failure arbitrarily gives fidelity at least $`c^2-\delta/2`$. Comparing this with Theorem 3.7 gives

```math
q\ge d^2(c^2-\delta/2)-1.
```

This extraction uses the compiled channel only in its forward direction. It strengthens the relevance of the inversion theorem to block-encoding compilers whose inverse implementation has not been supplied. The earlier exact lower bound of Odake, Yoshida and Murao, [PRL 135, 230603 (2025)](https://doi.org/10.1103/drp2-rzzw), alone would not cover approximate compiled channels. Conversely, the exact $`O(d^2)`$ inversion algorithm of Chen et al., [arXiv:2403.04704v3](https://arxiv.org/abs/2403.04704v3), prevents interpreting inversion as a $`d^2/\delta`$ lower bound.

## Channel adjoints and virtual transformations have different outputs

Zhu, Tang, Zhen, Li, Bai and Wang, *Simulation of Adjoints and Petz Recovery Maps for Unknown Quantum Channels*, [arXiv:2602.05828v1](https://arxiv.org/pdf/2602.05828v1), distinguish exact physical channel transformations from virtual ones. Their Theorem 1 rules out a finite-copy completely positive supermap that exactly conjugates every general channel; an adjoint no-go follows by composing with channel transposition. Their virtual construction reconstructs expectation values through signed classical postprocessing.

The present task asks for an approximate physical unitary on vectorized data in a larger Hilbert space. It neither exactly implements $`\mathcal E^{\dagger}`$ on density matrices for all channels nor returns only a signed expectation-value estimate. The no-go theorem and virtual protocol therefore do not subsume, and are not contradicted by, the unital coherentization result. The unitary subclass remains special because extracting $`U^{\dagger}`$ from the dilation is then a valid physical channel operation.

## Noisy-unitary purification and the open precision dependence

Niwa, Yoshida and Murao, *Asymptotically optimal purification of noisy unitary channels in any dimension*, [arXiv:2608.26061v1](https://arxiv.org/abs/2608.26061v1), study an unknown unitary followed by depolarizing noise. They obtain leading-order purification and conjugation costs proportional to $`d^2p/\epsilon`$, optimizing over adaptive sequential strategies in the specified low-noise and large-query limits. This is a relevant neighboring transformation problem. Its ordered, leading-order statement is not a uniform $`\Omega(d^2/\delta)`$ theorem for the present compilation task at fixed nonzero noise. No such transfer is assumed here.

The supported conclusion consequently remains specific: for ordinary access to unknown unital channels, constant-normalization coherent Liouville compilation has optimal quadratic dimension dependence at fixed sufficiently small precision, up to logarithmic factors. Determining its full joint dimension–precision frontier is left open.
