# Quantum Channel Coherentization

**How many uses of an unknown physical channel are needed before a spectral quantum algorithm can use its matrix coherently?**

For unknown unital channels, this repository establishes the optimal dimension order at fixed accuracy. An explicit compiler uses quadratically many ordinary channel calls. A matching lower bound holds already for unknown unitary channels, because coherent Liouville access can expose the unitary's inverse.

## Principal result

Let $`\mathcal E`$ be a memoryless unital channel on $`\mathbb C^d`$, let $`L_{\mathcal E}`$ be its Liouville matrix in the [stated vectorization convention](science/model.md), and define

```math
\mathsf H(L_{\mathcal E})
=\begin{pmatrix}0&L_{\mathcal E}\\L_{\mathcal E}^\dagger&0\end{pmatrix}.
```

The input interface is ordinary forward channel access. The output guarantees are in the **unhalved diamond norm**, including arbitrary reference-entangled data.

| Requested quantum output | Constructive ordinary-channel cost | Necessary cost |
| --- | --- | --- |
| Evolution $`e^{-it\mathsf H(L_{\mathcal E})}`$ | $`2m`$ calls with error at most $`(4d^2+2)t^2/m`$ | At $`t=\pi/2`$ and error $`\epsilon`$: $`q\ge d^2(1-\epsilon/2)-1`$ |
| Complete unitary with exact designated block $`\mathsf H(L_{\mathcal E})/\pi`$ | $`O(d^2\delta^{-1}[1+\log(1/\delta)]^2)`$ calls for full-channel error $`\delta`$ | $`q\ge d^2(\pi^{-2}-\delta/2)-1`$ |

At any fixed sufficiently small accuracy, the necessary and sufficient call order is therefore

```math
\boxed{Q(d)=\Theta(d^2).}
```

For $`n`$ input qubits this is $`\Theta(4^n)`$. The matching statement fixes accuracy and a suitable evolution time; it does not establish optimal joint dependence on dimension, precision or time.

The construction generates coherent controls and inverses of its output operations with the same query order. It does not require controlled or inverse access to the unknown channel, a Stinespring dilation, a Kraus description or QRAM. The [resource account](science/resources.md) charges every Choi-program preparation and separates queries from known gates, finite synthesis and workspace.

## Mechanism and consequence

A fresh Choi state and a known controlled swap form one mixed program. Its partially transposed first moment contains the desired Liouville matrix. For unital channels, the relevant program marginal is maximally mixed, so the collision second moment is exactly the identity. The inherited program-variance estimate then gives the quadratic construction.

For a unitary channel, $`L_U=U\otimes\overline U`$. The Hermitian lift also contains $`U^\dagger\otimes U^{\mathsf T}`$. A single forward use of a designated block can consequently herald the inverse of $`U`$ with constant probability. The known robust inversion fidelity bound forces the quadratic dimension cost even when the compiler's inverse is unavailable.

The Liouville construction, Hermitian-preserving map exponentiation, variance estimate, polynomial transformation and inversion theorem are credited in [related work](references/RELATED_WORK.md). The contribution is the valid unital-case compiler together with the matching fixed-accuracy operational frontier. The original Liouville preprint already advertised the improved exponent before its generic error bound was corrected; that version history is stated explicitly rather than treated as a new numerical scaling alone.

With the additional promise of a known depolarizing probability below one, the same compiler and a known commuting correction also approximate a clean unknown unitary from its noisy channel. The [worked channel examples](science/examples.md) derive that finite-noise upper bound and its calibration and precision limits.

## Read the scientific account

| Question | Authoritative page |
| --- | --- |
| What is supplied, counted and produced? | [Model and normalization](science/model.md) |
| Why does the program marginal improve the full-channel bound? | [Collision compiler and proof](science/collision-compiler.md) |
| How is an exact designated block obtained with complete-unitary error control? | [Block-encoding compiler](science/block-encoding.md) |
| Why must every ordinary-query compiler pay the dimension cost? | [Inversion reduction and lower bound](science/dimension-lower-bound.md) |
| What do known gates, precision, memory and work return cost? | [Resources](science/resources.md) |
| What happens for unitary and noisy-unitary channels? | [Examples](science/examples.md) |
| What is matched and what remains open? | [Interpretation](science/interpretation.md) |
| Which results and methods are inherited? | [Related work](references/RELATED_WORK.md) and [bibliography](references/references.bib) |
| Which finite identities and channels were checked? | [Verification](verification/README.md) |

The [science guide](science/README.md) connects the proof dependencies, and [llms.txt](llms.txt) maps reader intentions to the same authoritative files.

## Reproduce the finite checks

```bash
python3 -m pip install -r verification/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 verification/verify.py
```

The checked-in [report](verification/report.json) records complex unital fixtures, nonunital boundaries, complete collision diagnostics, controlled extensions, inverse extraction and the known-noise correction. Choi-distance diagnostics are labeled as finite consistency checks, rather than diamond-norm upper certificates. The general results follow from the analytical proofs.

## Scope

The channel is promised unital and memoryless; that promise is not learned for free. The lower bound permits arbitrary known controls, memory and causal adaptation under a hard query cap. The output is an actual approximate quantum operation on vectorized data, rather than a classical estimate or a virtual expectation-value reconstruction. Physical implementation uses $`O(\log d)`$ program and work qubits even though the ideal output block needs only a constant number of extra flags.

The full precision frontier, optimal long-time dependence, optimal synthesis constants, hardware noise thresholds and an application-level classical comparison remain outside the matched theorem. Structured channel families and stronger supplied access can have lower costs.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
