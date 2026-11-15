# The channel and the coherent target

An ordinary invocation of an unknown quantum channel gives a physical input-output operation. It does not give its Kraus operators, an accessible environment, or a unitary dilation that can be reversed. The task studied here is to turn repeated ordinary invocations into a coherent evolution whose Hamiltonian contains the channel's Liouville matrix.

## Fixed basis and vectorization

Fix a $`d`$-dimensional Hilbert space $`\mathcal H`$ with a known computational basis. Write $`\mathsf L(\mathcal H)`$ for its linear operators and $`\mathsf D(\mathcal H)`$ for its density operators. For an arbitrary operator $`X`$, use vectorization in the following explicit convention:

```math
|X\rangle\!\rangle
=\sum_{i,j=1}^d X_{ij}|i\rangle\otimes|j\rangle.
```

The input is a completely positive, trace-preserving, unital map $`\mathcal E:\mathsf L(\mathcal H)\to\mathsf L(\mathcal H)`$. Thus $`\mathcal E(I)=I`$. Its Liouville matrix $`L_{\mathcal E}`$ is the unique matrix satisfying

```math
|\mathcal E(X)\rangle\!\rangle
=L_{\mathcal E}|X\rangle\!\rangle,
\qquad
(L_{\mathcal E})_{ab,ij}
=\langle a|\mathcal E(|i\rangle\langle j|)|b\rangle.
```

In this convention, a unitary channel $`X\mapsto UXU^\dagger`$ has Liouville matrix $`U\otimes\overline U`$. Transposition and complex conjugation below always refer to the fixed computational basis.

The normalized maximally entangled vector and the normalized Choi state are

```math
|\Phi_d\rangle=\frac1{\sqrt d}\sum_{i=1}^d|i\rangle|i\rangle,
\qquad
J_{\mathcal E}
=(\mathcal E\otimes\mathrm{id})(|\Phi_d\rangle\langle\Phi_d|).
```

One ordinary call to $`\mathcal E`$ prepares one fresh $`J_{\mathcal E}`$: prepare the known entangled input, apply the channel to its first half, and retain the two visible output registers. No purification of $`J_{\mathcal E}`$ is assumed. Trace preservation and unitality give its two flat marginals,

```math
\mathrm{Tr}_1 J_{\mathcal E}=I/d,
\qquad
\mathrm{Tr}_2 J_{\mathcal E}=I/d.
```

## Target evolution and normalization

For a matrix $`A`$, define its Hermitian lift, on a flag qubit and the matrix's data space, by

```math
\mathsf H(A)
=|0\rangle\langle1|\otimes A
+|1\rangle\langle0|\otimes A^\dagger
=\begin{pmatrix}0&A\\A^\dagger&0\end{pmatrix}.
```

The requested coherent target is the channel

```math
\mathcal U_{\mathcal E,t}(X)
=U_{\mathcal E}(t)XU_{\mathcal E}(t)^\dagger,
\qquad
U_{\mathcal E}(t)=e^{-it\mathsf H(L_{\mathcal E})},
\qquad t\in\mathbb R.
```

There is no factor $`1/2`$, $`1/d`$, or hidden block normalization in this definition. The flag and the two vectorization registers have total dimension $`2d^2`$. The output must work on arbitrary data inputs, including inputs entangled with an untouched reference system.

For a unital channel, $`\Vert L_{\mathcal E}\Vert_\infty=1`$. Indeed, the Schwarz inequality for unital completely positive maps gives

```math
\mathcal E(X)^\dagger\mathcal E(X)
\preceq\mathcal E(X^\dagger X).
```

Taking the trace and using trace preservation proves Hilbert-Schmidt contraction, so $`\Vert L_{\mathcal E}\Vert_\infty\le1`$. The fixed vector $`|I\rangle\!\rangle`$ gives equality. Consequently $`\Vert\mathsf H(L_{\mathcal E})\Vert_\infty=1`$. This explains why the unnormalized target already has a dimension-independent Hamiltonian norm in the present class.

## Access and charged resources

A channel query is one forward use of $`\mathcal E`$ on a register that the protocol chooses. The channel is memoryless: different calls implement independent uses of the same completely positive, trace-preserving map. The compiler may retain quantum memory between calls and may use known operations, fresh ancillas, and discarding. Its construction uses the queries only to prepare fresh Choi states.

The supplied access contains no controlled-$`\mathcal E`$ operation, no adjoint channel, no inverse channel, no Stinespring unitary, and no ability to inspect or control the channel's environment. [The compiler](collision-compiler.md) generates positive-time, negative-time, and coherently controlled target evolutions using ordinary forward calls. The target inverse is therefore an output capability, rather than an input oracle.

The primary resource bound counts ordinary channel calls. Preparing the known entangled inputs, performing swaps, implementing the known collision interactions, and synthesizing their rotations are additional charged operations. They are kept separate from the query theorem. The construction needs a constant number of registers of dimension $`d`$, a constant number of flag qubits, and one fresh program at a time; it does not retain all program specimens simultaneously. For $`d=2^n`$, this register requirement is $`O(n)`$ qubits. No quantum random-access memory or free loading of classical matrix entries is used.

## Error convention

All diamond distances are **unhalved**. For a linear map $`\Lambda`$,

```math
\Vert\Lambda\Vert_\diamond
=\sup_{r\ge1}\sup_{X\ne0}
\frac{\Vert(\Lambda\otimes\mathrm{id}_r)(X)\Vert_1}{\Vert X\Vert_1}.
```

In particular, the diamond distance between two channels is at most $`2`$. The compiler's guarantee is $`\Vert\widetilde{\mathcal U}_{\mathcal E,t}-\mathcal U_{\mathcal E,t}\Vert_\diamond\le\epsilon`$, with this convention. It is a uniform channel guarantee, rather than a bound for one chosen input or one observable.

## Relation to the existing construction

The Liouville target, the Choi-state controlled-SWAP programs, and their partial-transpose collision construction are inherited from Niwa, Rossi, Taranto, and Murao, [*Singular value transformation for unknown quantum channels*, arXiv:2506.24112v3](https://arxiv.org/html/2506.24112v3), especially Eqs. (9)–(14) and Appendix B.1. The present compiler evaluates the program second moment before bounding the collision error. Both program marginals are flat for a unital channel, and this removes a dimension factor from the resulting query bound. The [proof](collision-compiler.md) gives the complete normalization, constants, and ordinary-query implementation.
