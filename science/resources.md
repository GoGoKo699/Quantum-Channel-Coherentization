# Calls, gates, memory, and error budgets

The query theorem counts uses of an unknown channel. Its construction also has a concrete known-gate implementation on qubits. This page accounts for those operations and distinguishes the small ancillary block in the output unitary from the disposable program used to synthesize that unitary.

## Ordinary channel access is the input

Every collision consumes one program state. Preparing it consists of making the known maximally entangled state, applying one ordinary call to the unknown channel to one half, preparing a flag, and applying a known controlled swap. The source environment is never accessed. The program is discarded after its collision and its registers are reused for the next fresh program. There is no preparation inverse, unknown-channel control, matrix-entry oracle, or QRAM input.

For the [evolution compiler](collision-compiler.md), let $`\epsilon_{\rm alg}`$ be the allowed algorithmic error. When $`t\ne0`$, the explicit budget is

```math
m=\left\lceil\frac{(4d^2+2)t^2}{\epsilon_{\rm alg}}\right\rceil,
\qquad Q_{\rm evol}=2m.
```

At zero time no call is needed. Thus a resource statement valid also at very small nonzero time is $`Q_{\rm evol}=O(1+d^2t^2/\epsilon_{\rm alg})`$; the additive ceiling is not suppressed in the finite theorem. This is a sufficient construction, not a time-optimality theorem.

The [block compiler](block-encoding.md) uses $`D=O(\log(1/\delta))`$ calls to sine-block primitives. Each primitive contains a constant number of controlled positive or negative target evolutions at a fixed known time. Allocating error $`O(\delta/D)`$ to each primitive gives

```math
Q_{\rm block}
=O\!\left(\frac{d^2D^2}{\delta}\right)
=O\!\left(\frac{d^2}{\delta}
\log^2\frac1\delta\right),
\qquad 0<\delta\le1/4.
```

The final physical channel is close to a complete unitary whose designated block is exactly $`\mathsf H(L_{\mathcal E})/\pi`$. It is not just a circuit with one accurate matrix element. Fresh programs are used throughout, so approximate oracle calls can be composed with the ordinary diamond-norm telescoping bound.

## A collision has a small known circuit

For this gate account take $`d=2^n`$, $`n\ge1`$, with logical all-to-all connectivity. The query theorem itself is stated for arbitrary finite $`d`$. Put $`A=CY`$ and $`B=Z`$ as in the compiler. The interaction is

```math
V=F_{AA'}\otimes d\Pi_{BB'},
\qquad
\Pi=|\Phi_d\rangle\langle\Phi_d|.
```

Let $`T_\Phi`$ be the known circuit with $`T_\Phi|0^{2n}\rangle=|\Phi_d\rangle`$. It consists of $`n`$ Hadamards and $`n`$ CNOTs. Conjugating by $`T_\Phi`$ turns the projector into the all-zero computational projector. It is then sufficient to perform $`e^{-idhF_{AA'}}`$ only when those $`2n`$ bits are zero.

The swap $`F_{AA'}`$ is a Hermitian involution. A clean sign ancilla, a Hadamard, a controlled swap, and a second Hadamard coherently record its eigenvalue $`s\in\{+1,-1\}`$ as the ancilla's $`Z`$ eigenvalue. A known $`Z`$ rotation through the corresponding angle applies phase $`e^{-idh s}`$. Uncomputing the sign circuit returns its ancilla exactly. Conditioning that rotation on the Bell-projector test therefore implements the desired collision, including its relative phases.

A controlled swap of the two $`n+1`$-qubit registers uses $`O(n)`$ Fredkin/Toffoli operations. The all-zero test and its uncomputation use $`O(n)`$ Toffolis with $`O(n)`$ clean work qubits. A doubly controlled rotation can be decomposed into a constant number of CNOTs and single-qubit rotations. Thus one collision requires $`O(n)`$ exact elementary Clifford/Toffoli gates and a constant number of arbitrary known rotations. The outer controlled swap and the program preparation have the same linear known-gate order.

For a coherently controlled target, compute the same swap sign and Bell flag, and condition the rotation additionally on the target control. Uncompute both tests on every branch. This does not require a controlled invocation of the unknown channel: the program is prepared with an ordinary call independently of the target control, and that physical call is counted even on its inactive branch.

## Finite gate synthesis

The preceding circuit is exact when its known rotations are exact. For a finite universal gate set, let $`S(\xi)`$ be a supplied synthesis bound for a single known rotation to operator-norm error at most $`\xi`$. Inverse and controlled gates must retain their known relative phases; an uncontrolled up-to-phase approximation cannot silently be substituted inside a controlled operation.

If $`R`$ synthesized rotations are used in the complete circuit, operator-norm errors telescope to at most $`R\xi`$. The induced channel error is at most $`2R\xi`$, including reference systems. Choosing

```math
\epsilon_{\rm alg}=\epsilon/2,
\qquad
\xi\le\frac{\epsilon}{4R}
```

therefore keeps the total evolution error at most $`\epsilon`$. Here $`R=O(Q_{\rm evol})`$; all exact gate preparations and uncomputations are included. A resulting conservative gate bound is

```math
G_{\rm evol}
=O\!\left(Q_{\rm evol}
\left[n+S\!\left(\frac{\epsilon}{O(Q_{\rm evol})}\right)\right]\right).
```

For the complete block compiler, include its $`O(D)`$ known phase/projection gates and use the same total-circuit allocation:

```math
G_{\rm block}
=O\!\left((Q_{\rm block}+D)
\left[n+S\!\left(\frac{\delta}{O(Q_{\rm block}+D)}\right)\right]\right).
```

These formulas can be used with a conservative Solovay–Kitaev polylogarithmic synthesis bound or with a more efficient verified synthesis algorithm. In particular, finite-precision compilation adds polylogarithmic factors rather than an uncharged exact-rotation oracle. [Ross and Selinger](https://arxiv.org/abs/1403.2975v3) give efficient practical Clifford+T synthesis and make the number-theoretic qualifications of their near-optimal classical-runtime claims explicit; no unconditional typical-case coefficient or optimal T-count is claimed here.

The target time and polynomial phases are known classical inputs. Computing rotation angles to the allocated precision is additional classical compilation work, using their finite descriptions; it requires no classical description of the unknown channel. The real-polynomial QSVT theorem provides classical phase synthesis to any requested accuracy. Phase computation, arithmetic precision and numerical conditioning are distinct from channel-query complexity. This account does not assert a concrete hardware runtime or an optimized fault-tolerant T-count.

## Memory and work return

The target data has $`2n+1`$ qubits. One program has a further $`2n+1`$ qubits. The Bell test, swap-sign extraction and linear-size reversible tests require $`O(n)`$ temporary qubits, all uncomputed before their known work is reused. A constant number of extra flag qubits suffice for the ideal block-encoding unitary itself. The total physical coherent workspace is consequently $`O(n)`$, not $`O(1)`$. Only one fresh mixed program need be present at a time; no bank of $`Q`$ programs is assumed.

Known clean work is returned after each collision. The unknown program is intentionally consumed and discarded; the theorem has no program-return or catalyst promise. Fresh preparation and discarding are allowed operations, with their gate and reset counts separate from the ordinary-query theorem. There is no protected unknown-channel environment or hidden record shared across calls.

## What the resource frontier means

At any fixed sufficiently small error and the fixed lower-bound time $`t=\pi/2`$, both the necessary and sufficient call orders are $`\Theta(d^2)`$. At $`d=2^n`$ this is exponential in the input qubit count. The known-gate implementation has the same dimension power times polynomial factors in $`n`$ and precision logarithms. No comparison with a classical algorithm for a separate scientific output task follows merely from this oracle conversion.

The upper's inverse-precision factor and its time dependence are not matched by the dimension converse. Unitality is a supplied promise, not a property learned for free; model mismatch and imperfect channel calls require their own error budget. If each ordinary call has diamond error at most $`\eta`$ relative to the promised memoryless channel, the whole $`Q`$-call protocol changes by at most $`Q\eta`$. This perturbation statement does not make an arbitrary nonunital channel satisfy the promised target theorem.
