# From Watrous to the coherent channel interface

The single background anchor is John Watrous, *The Theory of Quantum Information* (Cambridge University Press, 2018), available through [the author's book page](https://cs.uwaterloo.ca/~watrous/TQI/). The locators below refer to the author's standard-layout manuscript, whose section and equation numbers were checked against the author-hosted chapters. The book is linked, not redistributed.

The book supplies the language for channels, their matrix representations, and error on entangled inputs. This project asks an additional algorithmic question: how many ordinary uses of an unknown channel are needed to implement a coherent evolution containing its matrix? A representation theorem identifies the desired matrix; an access model determines what it costs to use that matrix in a circuit.

## The relevant parts of the book

| Book locator | Role in this project | Project destination |
| --- | --- | --- |
| §1.1.2, “The operator-vector correspondence,” Eqs. (1.127)–(1.134) | Fix tensor order, conjugation, and the operator-to-vector isometry. | [Model and conventions](../science/model.md) |
| §2.2.1 and §2.2.2, “Representations and characterizations of channels,” especially Eqs. (2.60)–(2.66) | Distinguish the physical channel, its natural representation, and its Choi representation. | [Model](../science/model.md), then [collision compiler](../science/collision-compiler.md) |
| §2.2.3, “Examples of channels and other mappings,” Eqs. (2.154)–(2.155) | Check the depolarizing channel in both representations. | The worked example below and [scientific examples](../science/examples.md) |
| §3.1.1 and §3.2, Definition 3.11 | Relate observable probabilities, trace distance, and the book's fidelity convention. | [Dimension lower bound](../science/dimension-lower-bound.md) |
| §3.3.2, Definition 3.43, and §3.3.3, “Distances between channels” | Understand the reference system and the completely bounded trace norm. | [Full channel error](../science/model.md#error-convention) |
| §4.2.2, “Fixed-points, spectra, and norms of unital channels,” Theorem 4.27 | Obtain the Hilbert–Schmidt contraction of a unital channel. | [Target normalization](../science/model.md#target-evolution-and-normalization) |

These are targeted entry points. Later sections on capacities, entropy, and entanglement theory are not prerequisites for this project's main proof. The [milestone map](MILESTONES.md) organizes the background and research argument separately.

## Translate the conventions before using the formulas

### Vectorization and the two representations

Watrous uses $`\mathrm{vec}(E_{ij})=|i\rangle\otimes|j\rangle`$. This project uses exactly that tensor convention:

```math
|X\rangle\!\rangle
=\mathrm{vec}(X)
=\sum_{i,j}X_{ij}|i\rangle|j\rangle,
\qquad
|AXB^\dagger\rangle\!\rangle
=(A\otimes\overline B)|X\rangle\!\rangle.
```

The explicit formula is the convention: software that flattens a matrix into a column can order its entries differently. In particular, the unitary channel $`X\mapsto UXU^\dagger`$ has matrix $`U\otimes\overline U`$ here. Watrous writes $`A^*`$ for the adjoint; this project writes $`A^\dagger`$.

| Object | Watrous | This project |
| --- | --- | --- |
| Natural/Liouville representation | $`K(\mathcal E)\mathrm{vec}(X)=\mathrm{vec}(\mathcal E(X))`$ | $`L_{\mathcal E}=K(\mathcal E)`$ |
| Entangled vector | $`\mathrm{vec}(I)`$, of squared norm $`d`$ | $`|\Phi_d\rangle=\mathrm{vec}(I)/\sqrt d`$ |
| Choi operator/state | $`J(\mathcal E)=(\mathcal E\otimes\mathrm{id})(\mathrm{vec}(I)\mathrm{vec}(I)^\dagger)`$ | $`J_{\mathcal E}=J(\mathcal E)/d`$ |
| Tensor legs of the Choi object | Output first, input second | The same |

For a trace-preserving map, the book's Choi operator has trace $`d`$; the project's Choi state has trace one. Thus a physical call on one half of $`|\Phi_d\rangle`$ prepares $`J_{\mathcal E}`$, with no extra factor of $`d`$. The normalized reconstruction formula is

```math
\mathcal E(X)
=d\,\mathrm{Tr}_{\mathrm{input}}
\!\left[J_{\mathcal E}(I_{\mathrm{output}}\otimes X^{\mathsf T})\right].
```

Trace preservation gives $`\mathrm{Tr}_{\mathrm{output}}J_{\mathcal E}=I/d`$. Unitality gives the other marginal, $`\mathrm{Tr}_{\mathrm{input}}J_{\mathcal E}=I/d`$. Both identities enter the compiler's second-moment calculation. Theorem 4.27 gives $`\VertL_{\mathcal E}\Vert_\infty=1`$ for a unital channel; this is the spectral norm of its matrix, corresponding to the induced Hilbert–Schmidt norm on operators, rather than the trace norm of its Choi state.

### Distance and fidelity

The project's $`\Vert\cdot\Vert_\diamond`$ is Watrous's completely bounded trace norm, without a factor of one half. For states, write $`D(\rho,\sigma)=\tfrac12\Vert\rho-\sigma\Vert_1`$. Consequently a compiler guarantee of unhalved diamond error $`\delta`$ implies output trace distance at most $`\delta/2`$, even with an untouched reference. Any specified measurement probability changes by at most $`\delta/2`$.

Watrous's Definition 3.11 uses the **unsquared** fidelity

```math
F_{\mathrm W}(\rho,\sigma)=\Vert\sqrt\rho\sqrt\sigma\Vert_1.
```

The lower bound instead uses overlap with the pure normalized Choi state of the ideal unitary:

```math
F_{\mathrm{ch}}(\mathcal R,\mathrm{Ad}_V)
=\langle\Phi_V|J_{\mathcal R}|\Phi_V\rangle
=F_{\mathrm W}\!\left(J_{\mathcal R},|\Phi_V\rangle\langle\Phi_V|\right)^2,
\qquad |\Phi_V\rangle=(V\otimes I)|\Phi_d\rangle.
```

Here $`F_{\mathrm{ch}}`$ is a squared fidelity, not the book's $`F_{\mathrm W}`$. Measuring the projector $`|\Phi_V\rangle\langle\Phi_V|`$ directly gives $`F_{\mathrm{ch}}\ge1-\delta/2`$ from diamond error $`\delta`$. This fixes the factor used in the lower-bound reduction.

## Where the book stops and the research task starts

The natural and Choi representations describe the same linear map, but the physical operations they make available differ. An ordinary channel call produces a state from an input state. It does not supply matrix entries, a controlled channel, an adjoint, or a reversible environment interface. The existence of a Stinespring representation in §2.2.2 does not make its dilation an accessible oracle. Likewise, an algebraic reshuffling or partial transpose of a Choi matrix is not automatically a physical operation on an unknown specimen.

The research target is a new unitary on a flag qubit and two data registers:

```math
U_{\mathcal E}(t)=e^{-it\mathsf H(L_{\mathcal E})},
\qquad
\mathsf H(A)=\begin{pmatrix}0&A\\A^\dagger&0\end{pmatrix}.
```

Its input is an arbitrary vector in the enlarged space, and its guarantee is a channel guarantee on arbitrary reference-entangled inputs. Repeated physical channel calls prepare fresh normalized Choi specimens; known interactions consume those specimens to approximate the target. Their preparation, collision error, circuit synthesis, and workspace need an explicit resource account. This conversion is the gap between knowing what $`L_{\mathcal E}`$ means and having a gate that coherently uses it.

Watrous supports the background statements above. The compiler itself depends on the later Liouville-program construction of Niwa and collaborators, marginal-sensitive Hamiltonian-mapping analysis, and a cited collision-variance lemma. The dimension lower bound depends on the later universal-unitary-inversion theorem of Chen, Yu, and Zhang. These are research dependencies, documented with their precise roles in [related work](../references/RELATED_WORK.md); they are not additional background anchors or results supplied by the book. For the direct evolution, the matching dimension bounds use the fixed time $`t=\pi/2`$ and fixed admissible accuracy. The block-encoding comparison fixes a constant normalization. Neither establishes a matching joint lower bound in dimension and inverse error.

## A complete qubit calculation

Take the known qubit channel

```math
\mathcal E(X)=\tfrac12X+\tfrac12\mathrm{Tr}(X)I/2.
```

This is the $`U=I,p=1/2`$ instance of [the depolarizing example](../science/examples.md#a-simple-qubit-noise-channel). Define two normalized operator vectors

```math
|e_0\rangle=|I\rangle\!\rangle/\sqrt2
=\frac{|00\rangle+|11\rangle}{\sqrt2},
\qquad
|e_z\rangle=|Z\rangle\!\rangle/\sqrt2
=\frac{|00\rangle-|11\rangle}{\sqrt2}.
```

The ordinary channel fixes the identity and halves every traceless operator. On a physical input qubit,

```math
|0\rangle\langle0|=\frac{I+Z}{2}
\quad\longmapsto\quad
\frac{I+Z/2}{2}
=\begin{pmatrix}3/4&0\\0&1/4\end{pmatrix}.
```

The corresponding Choi state and Liouville matrix are different objects:

```math
J_{\mathcal E}=\tfrac12|e_0\rangle\langle e_0|+\tfrac18 I_4,
\qquad
L_{\mathcal E}=\tfrac12 I_4+\tfrac12|e_0\rangle\langle e_0|.
```

The first has trace one and both marginals $`I_2/2`$. The second has eigenvalue one on $`e_0`$ and eigenvalue $`1/2`$ on $`e_z`$. Since $`L_{\mathcal E}`$ is Hermitian, its lift is $`X_C\otimes L_{\mathcal E}`$, giving

```math
U_{\mathcal E}(t)|0\rangle_C|e_z\rangle
=\left(\cos(t/2)|0\rangle_C-i\sin(t/2)|1\rangle_C\right)|e_z\rangle.
```

At $`t=\pi/2`$, the output is $`(|0\rangle-i|1\rangle)_C|e_z\rangle/\sqrt2`$. At the same time, $`|0\rangle_C|e_0\rangle`$ becomes $`-i|1\rangle_C|e_0\rangle`$. The channel's contraction coefficients have become coherent flag-rotation frequencies. No trace or norm is lost by this enlarged unitary.

Although $`Z/\sqrt2`$ is not a density operator, its vectorization $`|e_z\rangle`$ is a valid normalized two-qubit state. This is why the enlarged interface can act on data that are not physical channel inputs under the operator interpretation. The example has known parameters and a known small circuit; it illustrates the interface and is not the universal hard family or a claim of optimal noise purification.

