# Compiling a unital channel into Liouville evolution

The controlled-SWAP programs of Niwa, Rossi, Taranto, and Murao already contain the desired Liouville matrix in the difference of their partially transposed first moments. The useful additional observation is that their transposed program register is maximally mixed for a unital channel. Its collision second moment is then exactly the identity. Applying the known program-variance bound to that moment gives a quadratic, rather than cubic, dimension dependence.

The construction below implements the full target from [the model](model.md), with an unhalved diamond guarantee and a finite integer budget. It uses ordinary forward calls to the unknown channel throughout.

## Finite-budget theorem

Let $`\mathcal E`$ be any unital channel on a $`d`$-dimensional system, and let $`m\ge1`$ be an integer. For every real $`t`$, there is a circuit using exactly $`2m`$ ordinary calls to $`\mathcal E`$ whose output channel $`\widetilde{\mathcal U}_{\mathcal E,t}^{(m)}`$ satisfies

```math
\left\Vert
\widetilde{\mathcal U}_{\mathcal E,t}^{(m)}
-\mathrm{Ad}_{e^{-it\mathsf H(L_{\mathcal E})}}
\right\Vert_\diamond
\le
\min\!\left\{2,\frac{(4d^2+2)t^2}{m}\right\}.
```

Here $`\mathrm{Ad}_W(X)=WXW^\dagger`$. The known gates in this theorem are exact. For $`t\ne0`$ and $`0<\epsilon<2`$, the choice

```math
m=\left\lceil\frac{(4d^2+2)t^2}{\epsilon}\right\rceil
```

therefore suffices, giving $`2\lceil(4d^2+2)t^2/\epsilon\rceil`$ ordinary calls. At $`t=0`$, the identity circuit uses zero calls. Negative $`t`$ requires no inverse-channel access. The same call bound applies to coherent control of the target evolution.

The constant is not asserted to be optimal. Its role is to make the finite-budget guarantee explicit. No small-step assumption or suppressed higher-order remainder is needed.

## The inherited program-variance bound

We use the following general reduced-unitary estimate. It is the program-variance lemma stated and proved in [*A reduced-unitary bound from the program variance*](https://github.com/GoGoKo699/Collective-Quantum-Programming/blob/0fefb607599f9c864918ed1ab58a778fe5b50cf1/science/collision_bound.md). Moment-sensitive error analysis also appears in Wei et al., [*Simulating non-completely positive actions via exponentiation of Hermitian-preserving maps*, arXiv:2308.07956](https://arxiv.org/abs/2308.07956), Appendix C.2, Eq. (C17). The lemma is reproduced here to keep the compiler's guarantee self-contained; it is not claimed as a new general estimate.

Let $`\rho`$ be a program state, let $`V`$ be a known Hermitian interaction between the program and the data, and define its first two program moments by

```math
K=\mathrm{Tr}_{\mathrm{prog}}[V(\rho\otimes I)],
\qquad
M=\mathrm{Tr}_{\mathrm{prog}}[V^2(\rho\otimes I)].
```

The partial-trace expressions agree with sandwiching $`V`$ or $`V^2`$ by $`\rho^{1/2}\otimes I`$ and then tracing out the program. In particular, the program expectation is a unital completely positive map and $`M-K^2\succeq0`$. Define

```math
\mathcal C_{\rho,h}(X)
=\mathrm{Tr}_{\mathrm{prog}}
\left[e^{-ihV}(\rho\otimes X)e^{ihV}\right],
\qquad
v=\VertM-K^2\Vert_\infty.
```

For every real $`h`$,

```math
\Vert\mathcal C_{\rho,h}-\mathrm{Ad}_{e^{-ihK}}\Vert_\diamond
\le2h^2v.
```

To prove this, purify $`\rho`$ to a vector $`|s\rangle`$ on an enlarged environment. This is an analytical purification; the circuit does not receive it. Let $`W|x\rangle=|s\rangle\otimes|x\rangle`$ be the embedding of the data into the joint space, extend $`V`$ by the identity on the purifying register, and write $`P=WW^\dagger`$, $`Q=I-P`$. Then

```math
W^\dagger VW=K,
\qquad
W^\dagger V^2W=M,
\qquad
\VertQVW\Vert_\infty^2=v.
```

It is enough to take $`h\ge0`$; changing $`V`$ to $`-V`$ handles negative time. Put

```math
A_s=W^\dagger e^{-isV}W,
\qquad
B_s=Qe^{-isV}W.
```

The projected Schrödinger equations and variation of constants give

```math
B_s=-i\int_0^s e^{-i(s-r)QVQ}QVWA_r\,dr,
\qquad
\VertB_s\Vert_\infty\le s\sqrt v,
```

because $`A_r`$ is a compression of a unitary and is a contraction. The equation for $`A_s`$ then gives

```math
A_h-e^{-ihK}
=-i\int_0^h e^{-i(h-r)K}W^\dagger VQB_r\,dr,
\qquad
\VertA_h-e^{-ihK}\Vert_\infty\le\frac{h^2v}{2}.
```

In a basis of the enlarged environment beginning with $`|s\rangle`$, tracing out that environment removes the cross terms between $`P`$ and $`Q`$. Thus

```math
\mathcal C_{\rho,h}(X)=A_hXA_h^\dagger+\mathcal B_h(X),
\qquad
\mathcal B_h(X)=\mathrm{Tr}_{\mathrm{env}}[B_hXB_h^\dagger].
```

The leakage map $`\mathcal B_h`$ is completely positive, so $`\Vert\mathcal B_h\Vert_\diamond=\VertB_h^\dagger B_h\Vert_\infty\le h^2v`$. The compressed term differs from $`\mathrm{Ad}_{e^{-ihK}}`$ by at most $`(\VertA_h\Vert_\infty+1)\VertA_h-e^{-ihK}\Vert_\infty\le h^2v`$ in diamond norm. These product bounds remain valid after adjoining an arbitrary reference. Adding the two contributions proves the lemma for all real $`h`$.

## Programs and their first moments

Let $`Y,Z`$ be $`d`$-dimensional program registers, let $`C`$ be a flag qubit, and write $`F=F_{YZ}`$ for the swap. Define the known controlled swap

```math
S=|0\rangle\langle0|\otimes I_{YZ}
+|1\rangle\langle1|\otimes F.
```

Prepare the two mixed programs

```math
\rho_\pm
=S\left(|\pm\rangle\langle\pm|_C\otimes J_{\mathcal E,YZ}\right)S^\dagger,
\qquad
|\pm\rangle=(|0\rangle\pm|1\rangle)/\sqrt2.
```

Each program uses one ordinary query to prepare $`J_{\mathcal E}`$ and then only known gates. This is the controlled-SWAP program from [Niwa et al., arXiv:2506.24112v3](https://arxiv.org/html/2506.24112v3), Eq. (10).

Group the program registers as $`A=CY`$ and $`B=Z`$, and let $`A',B'`$ be their matching data registers. The collision interaction is

```math
V=F_{AA'}\otimes d|\Phi_d\rangle\langle\Phi_d|_{BB'}.
```

The swap identity on $`AA'`$ and the maximally entangled identity on $`BB'`$ give, for either program,

```math
\mathrm{Tr}_{AB}[V(\rho_\pm\otimes I_{A'B'})]
=\rho_\pm^{T_B}
=:K_\pm.
```

The transpose is only over $`B=Z`$. To check the Liouville orientation, the Choi entries satisfy $`(J_{\mathcal E})_{ai,bj}=(L_{\mathcal E})_{ab,ij}/d`$, which implies

```math
(J_{\mathcal E}F)^{T_Z}=L_{\mathcal E}F/d,
\qquad
(FJ_{\mathcal E})^{T_Z}=FL_{\mathcal E}^\dagger/d.
```

The diagonal flag blocks cancel in the difference of the two programs. Consequently,

```math
K_+-K_-
=\frac1d
\begin{pmatrix}
0&L_{\mathcal E}F\\
FL_{\mathcal E}^\dagger&0
\end{pmatrix}
=\frac1d S\mathsf H(L_{\mathcal E})S.
```

The last $`S`$ acts on the data flag and data pair. This identity fixes the final time scale: $`m`$ pairs with collision step $`h=dt/m`$ implement the target time $`t`$ after an outer conjugation by $`S`$.

## Flat marginal and exact second moment

Tracing out the flag removes the program's off-diagonal blocks, so

```math
(\rho_\pm)_B
=\frac12\left(\mathrm{Tr}_YJ_{\mathcal E}
+\mathrm{Tr}_Y[FJ_{\mathcal E}F]\right)
=\frac{I+\mathcal E(I)}{2d}
=I/d.
```

This is the point where unitality enters the error bound. Since $`F_{AA'}^2=I`$ and $`(|\Phi_d\rangle\langle\Phi_d|)^2=|\Phi_d\rangle\langle\Phi_d|`$,

```math
V^2=I_{AA'}\otimes d^2|\Phi_d\rangle\langle\Phi_d|_{BB'}.
```

The program expectation is therefore

```math
M_\pm
=\mathrm{Tr}_{AB}[V^2(\rho_\pm\otimes I)]
=I_{A'}\otimes d(\rho_\pm)_B^T
=I_{A'B'}.
```

It follows that $`v_\pm=\VertI-K_\pm^2\Vert_\infty\le1`$. The inherited variance lemma now gives the uniform local guarantee

```math
\Vert\mathcal C_{\rho_\pm,h}
-\mathrm{Ad}_{e^{-ihK_\pm}}\Vert_\diamond
\le2h^2
```

for every real step $`h`$. Replacing this evaluated moment by a worst-case interaction bound would discard the flat-marginal information.

For the product-formula constant, we also use $`\VertK_\pm\Vert_\infty\le1/d`$. Here is a direct reason. For any bipartite state $`\rho_{AB}`$, the maps $`X\mapsto\mathrm{Tr}(X)I\pm X^T`$ are completely positive because their Choi matrices are $`I\pm F`$. Applying either map on $`A`$ to the positive matrix $`\rho^{T_{AB}}`$ proves

```math
-I_A\otimes\rho_B^T
\preceq\rho^{T_B}
\preceq I_A\otimes\rho_B^T.
```

Thus $`\Vert\rho^{T_B}\Vert_\infty\le\Vert\rho_B\Vert_\infty`$. Substituting $`\rho_B=I/d`$ gives the required bound for both programs.

## Pairing, product formula, and total error

One physical pair is

```math
\mathcal P_h
=\mathcal C_{\rho_-,-h}\circ\mathcal C_{\rho_+,h}.
```

Its ideal product is the unitary channel of $`e^{ihK_-}e^{-ihK_+}`$. Channel composition and contractivity give a total collision error at most $`4h^2`$ for the pair.

For Hermitian $`A,B`$, the first-order unitary product formula obeys

```math
\Verte^{-ihA}e^{-ihB}-e^{-ih(A+B)}\Vert_\infty
\le\frac{h^2}{2}\Vert[A,B]\Vert_\infty.
```

This follows by differentiating an interpolating product and integrating the commutator once more; the surrounding factors are unitary, so the estimate holds for all real $`h`$. Passing to channels multiplies this operator bound by at most $`2`$. With $`A=-K_-`$ and $`B=K_+`$,

```math
\Vert[K_+,K_-]\Vert_\infty
\le2\VertK_+\Vert_\infty\VertK_-\Vert_\infty
\le2/d^2.
```

Combining collision and product-formula errors gives

```math
\left\Vert\mathcal P_h
-\mathrm{Ad}_{e^{-ih(K_+-K_-)}}\right\Vert_\diamond
\le(4+2/d^2)h^2.
```

Take $`h=dt/m`$, prepare fresh programs for every collision, and set

```math
\widetilde{\mathcal U}_{\mathcal E,t}^{(m)}
=\mathrm{Ad}_S\circ\mathcal P_{dt/m}^{\,m}
\circ\mathrm{Ad}_S.
```

Telescoping the $`m`$ channel differences gives

```math
\left\Vert\mathcal P_{dt/m}^{\,m}
-\mathrm{Ad}_{e^{-idt(K_+-K_-)}}\right\Vert_\diamond
\le m(4+2/d^2)\frac{d^2t^2}{m^2}
=\frac{(4d^2+2)t^2}{m}.
```

The first-moment identity and $`S^2=I`$ turn the ideal channel after the two outer conjugations into $`\mathrm{Ad}_{e^{-it\mathsf H(L_{\mathcal E})}}`$. There are two fresh one-query programs per pair, proving the stated $`2m`$-query theorem.

## Coherent control and negative time

To control the target on an additional data qubit $`Q`$, replace the known interaction by

```math
V_{\mathrm c}=|1\rangle\langle1|_Q\otimes V.
```

Its program moments are $`K_{\pm,\mathrm c}=|1\rangle\langle1|_Q\otimes K_\pm`$ and $`M_{\pm,\mathrm c}=|1\rangle\langle1|_Q\otimes I`$, so the variance norm remains at most $`1`$. The commutator bound is unchanged. Coherently controlling the two outer known swaps then implements the controlled target with the same number of ordinary channel calls. The control acts on known gates after the programs have been prepared; the unknown channel itself is never controlled.

Negative time is obtained by changing the signs of the known collision angles. All moment and product-formula bounds depend on $`h^2`$ and remain valid. In particular, preparing the programs still uses forward $`\mathcal E`$ calls, even when the requested output is the inverse of the positive-time coherent evolution.

## Known-gate precision

The query theorem separates oracle calls from known-gate approximation. If the $`j`$th implemented known operation differs from its ideal channel by at most $`\eta_j`$ in unhalved diamond norm, contractivity and telescoping add at most $`\sum_j\eta_j`$ to the theorem's error. One can therefore allocate part of a total target error to the finite collision budget and the remainder to known-gate synthesis. No channel inversion, environmental access, or hidden matrix-entry loading is introduced by this allocation.
