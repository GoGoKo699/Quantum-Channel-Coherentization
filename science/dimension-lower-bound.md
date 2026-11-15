# Why coherent channel access costs quadratically in dimension

The dimension dependence of the construction can be tested on unitary channels alone. An ordinary application of an unknown unitary channel acts on density matrices. A coherent unitary encoding of its Liouville matrix acts on arbitrary vectors of a larger Hilbert space. The latter interface can implement the inverse of the unknown unitary, so a lower bound for universal unitary inversion also bounds channel coherentization.

This argument uses only the forward physical queries made by the compiler. It does not assume that the compiler's output can be inverted, and it does not charge a classical circuit description as though it were an available oracle.

## Model and normalization

Let $`d\ge2`$ and let $`\mathcal E`$ be an unknown channel on $`\mathbb C^d`$. An algorithm may use arbitrary known quantum operations, ancillas, measurements and classical feedback between ordinary calls to $`\mathcal E`$. Its query budget is a hard cap $`q`$ on every branch. There is no access to a Stinespring dilation, its inverse, an environment record, or a controlled version of the unknown channel.

Use the model’s explicit vectorization convention, so the Liouville matrix $`L_{\mathcal E}`$ obeys $`|\mathcal E(X)\rangle\!\rangle=L_{\mathcal E}|X\rangle\!\rangle`$. Define its Hermitian dilation by

```math
\mathsf H_{\mathcal E}
=\begin{pmatrix}
0&L_{\mathcal E}\\
L_{\mathcal E}^{\dagger}&0
\end{pmatrix}.
```

For a unitary channel $`\mathcal E_U(X)=UXU^{\dagger}`$,

```math
L_U=U\otimes\overline U,\qquad
L_U^{\dagger}=U^{\dagger}\otimes U^{\mathsf T},\qquad
\mathsf H_U^2=I.
```

All these channels are unital. Consequently a lower bound proved on this family applies to a compiler required to work on every unital channel. Each physical query to $`\mathcal E_U`$ is implemented by one forward use of $`U`$ on the queried register, including when that register is entangled with arbitrary memory.

Every diamond norm below is unhalved. The guarantee concerns the whole output channel on all data inputs and their reference systems.

## The inversion theorem used

For a deterministic ordinary-query algorithm $`\mathcal R`$ that makes at most $`q`$ forward calls to an unknown $`d`$-dimensional unitary, let $`\mathcal R_U`$ denote its output channel. Theorem 3.7 of Chen, Yu and Zhang, [arXiv:2507.05736v4](https://arxiv.org/pdf/2507.05736v4), gives

```math
\mathbb E_{U\sim\mathrm{Haar}}
F_{\mathrm{ch}}(\mathcal R_U,\mathrm{Ad}_{U^{\dagger}})
\le\frac{q+1}{d^2}.
```

Here $`F_{\mathrm{ch}}`$ is the fidelity of normalized Choi states, with the second argument a pure unitary Choi state. The bound covers adaptive coherent strategies and unrestricted ancillas. A strategy using fewer than $`q`$ calls on some branches can be padded by querying and discarding fresh registers, so the same hard-cap formulation follows from the fixed-query theorem.

We use this fidelity bound directly. This matters when extracting an inverse from a heralded block: the failure branch need not approximate the inverse.

## Direct coherent evolution

Suppose a $`q`$-query compiler produces $`\widetilde{\mathcal V}_{\mathcal E}`$ satisfying

```math
\left\Vert
\widetilde{\mathcal V}_{\mathcal E}
-\mathrm{Ad}_{e^{-i(\pi/2)\mathsf H_{\mathcal E}}}
\right\Vert_{\diamond}\le\delta
```

for every unital $`\mathcal E`$. On the unitary family,

```math
e^{-i(\pi/2)\mathsf H_U}=-i\mathsf H_U.
```

Prepare the dilation flag in $`|0\rangle`$, place an arbitrary target state in the first $`d`$-dimensional register, and initialize the second in a fixed $`|0\rangle`$. For a pure target vector the ideal transformation is

```math
|0\rangle\otimes|\psi\rangle\otimes|0\rangle
\longmapsto
-i|1\rangle\otimes U^{\dagger}|\psi\rangle
\otimes U^{\mathsf T}|0\rangle.
```

Discarding the flag and the second register therefore implements $`\mathrm{Ad}_{U^{\dagger}}`$. The same statement holds with a target reference system: the discarded output is independent of the target and its reference. Diamond distance is contractive under this initialization and discarding, so the actual inverse channel has error at most $`\delta`$.

If a channel $`\mathcal R_U`$ has diamond distance at most $`\delta`$ from the desired unitary, its normalized Choi state $`\rho_U`$ satisfies

```math
1-F_{\mathrm{ch}}(\mathcal R_U,\mathrm{Ad}_{U^{\dagger}})
\le\frac12\left\Vert\rho_U-
|u^{-1}\rangle\langle u^{-1}|\right\Vert_1
\le\frac\delta2.
```

The first inequality is the variational characterization of trace distance applied to the projector onto the ideal Choi vector. Combining it with the inversion theorem yields the explicit lower bound

```math
q\ge d^2\left(1-\frac\delta2\right)-1.
```

Thus constant-time, constant-error coherent evolution of the unnormalized Hermitian dilation requires $`\Omega(d^2)`$ ordinary channel queries.

## A constant-normalization block is already sufficient

The same conclusion holds for the block-encoding output used by spectral algorithms. Fix a known constant $`0<c\le1`$. For each unital channel let $`W_{\mathcal E}`$ be any unitary whose designated ancilla block is exactly

```math
(\langle0^a|\otimes I)W_{\mathcal E}(|0^a\rangle\otimes I)
=c\mathsf H_{\mathcal E}.
```

The unspecified blocks of $`W_{\mathcal E}`$ may depend on the channel. Suppose an ordinary-query compiler produces $`\widetilde{\mathcal W}_{\mathcal E}`$ such that

```math
\left\Vert\widetilde{\mathcal W}_{\mathcal E}
-\mathrm{Ad}_{W_{\mathcal E}}\right\Vert_{\diamond}\le\delta.
```

Apply this output channel once, initializing its block ancilla in $`|0^a\rangle`$ and the remaining registers as in the previous construction. Measure whether the block ancilla returns to $`0^a`$. In the ideal channel this outcome has probability exactly $`c^2`$, independent of the target, because $`\mathsf H_U`$ is unitary. On this outcome the first data register is the desired $`U^{\dagger}`$ output. On failure discard the data and prepare an arbitrary fixed state. This completes the protocol to a deterministic channel without any further oracle call.

For the ideal block unitary, the completed inverse channel has the form

```math
\mathcal R_U^{\mathrm{ideal}}
=c^2\mathrm{Ad}_{U^{\dagger}}
+(1-c^2)\mathcal F_U
```

for some channel $`\mathcal F_U`$. Its channel fidelity with the desired inverse is at least $`c^2`$, since the contribution of the failure channel is nonnegative. The identical completion applied to the actual output channel stays within $`\delta`$ of this ideal completion. Testing the ideal inverse Choi projector therefore gives

```math
F_{\mathrm{ch}}(\mathcal R_U,\mathrm{Ad}_{U^{\dagger}})
\ge c^2-\frac\delta2.
```

The inversion fidelity theorem now implies

```math
\boxed{\quad q\ge d^2\left(c^2-\frac\delta2\right)-1.\quad}
```

This is informative whenever $`\delta<2c^2`$ and gives $`\Omega(d^2)`$ for every fixed positive $`c`$ and sufficiently small fixed error. For the normalization $`c=1/\pi`$, one may, for example, take $`\delta\le1/\pi^2`$ to obtain $`q\ge d^2/(2\pi^2)-1`$.

The reduction invokes neither $`W_{\mathcal E}^{\dagger}`$ nor an inverse of the physical compiler. A guarantee only for a heralded successful branch, with no accounted hard bound on retries, is a different interface and does not satisfy the premise above.

## What is matched, and what remains open

The construction's upper bound is $`\widetilde O(d^2/\delta)`$ for a constant-normalization block, whereas the lower bound above is $`\Omega(d^2)`$ at fixed sufficiently small $`\delta`$. These establish the optimal polynomial dependence on $`d`$ at fixed precision, up to the stated logarithmic overhead. They do not establish a jointly optimal $`\Theta(d^2/\delta)`$ law as $`d`$ and $`1/\delta`$ vary.

The hard cap is material: an unbounded repeat-until-success procedure cannot be inserted into this reduction by calling its expected query count a fixed budget. A bounded procedure obtained by truncation may be used after counting the cap and including its abort contribution in the error.

The precision gap cannot be removed by citing unitary inversion alone. Exact deterministic inversion is possible with $`O(d^2)`$ forward unitary queries, as shown by Chen, Mo, Liu, Zhang and Wang, [arXiv:2403.04704v3](https://arxiv.org/abs/2403.04704v3). Consequently that subclass supplies a dimension obstruction, while the additional precision cost of coherentizing general noisy unital channels requires separate analysis. The distinctions from specimen access, exact channel-adjoint transformation and low-noise channel purification are set out in [RELATED_WORK.md](../references/RELATED_WORK.md).
