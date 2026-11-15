# A complete unitary block encoding

The coherent evolution in [the collision compiler](collision-compiler.md) also provides a block encoding for spectral algorithms. The guarantee below concerns the entire implemented channel: it is close to one unitary with an exact designated block. A small error in a designated block alone would be a weaker statement.

The route from a short evolution to its sine, followed by an odd polynomial approximation to the inverse sine, is inherited from Gilyén, Su, Low, and Wiebe and from Niwa, Rossi, Taranto, and Murao. The role of the present collision bound is to reduce the ordinary-channel cost of the required controlled evolutions. The final completion argument makes the complete-channel guarantee explicit.

## Output and error guarantee

Use [the model's](model.md) Hermitian lift and put

```math
H_0=\frac12\mathsf H(L_{\mathcal E}),
\qquad
A=\frac2\pi H_0
=\frac1\pi\mathsf H(L_{\mathcal E}).
```

For every unital channel $`\mathcal E`$ on $`\mathbb C^d`$ and every $`0<\delta\le1`$, the construction produces a channel $`\widetilde{\mathcal V}_{\mathcal E}`$ and an exact unitary $`V_{\mathcal E}`$ on the same output registers such that

```math
(\langle0^a|\otimes I)V_{\mathcal E}
(|0^a\rangle\otimes I)=A,
\qquad
\left\Vert\widetilde{\mathcal V}_{\mathcal E}
-\mathrm{Ad}_{V_{\mathcal E}}\right\Vert_\diamond
\le\delta.
```

Here $`a=O(1)`$ is the number of block-encoding ancillary qubits, the data dimension is $`2d^2`$, and the diamond norm is unhalved. The exact unitary's unspecified blocks may depend on $`\mathcal E`$. No classical description of those blocks is required by the construction.

The number of ordinary forward calls to $`\mathcal E`$ is

```math
O\!\left(\frac{d^2}{\delta}
\left[1+\log\frac1\delta\right]^2\right).
```

The physical implementation additionally uses one disposable Choi-based program at a time, as in the collision compiler. Thus the constant block-ancilla count is distinct from the $`O(\log d)`$ qubits of program workspace. Known-gate implementation and synthesis are separate resources. The construction supplies no inverse or controlled access to the unknown channel as an input.

## An exact sine block

Unitality gives $`\Vert H_0\Vert_\infty\le1/2`$. Define

```math
U=e^{-iH_0},
\qquad
C_U=|0\rangle\langle0|\otimes I
+|1\rangle\langle1|\otimes U.
```

On a new block qubit and the data, the unitary

```math
B_0=C_U(Y\otimes I)C_U^\dagger
=\begin{pmatrix}0&-iU^\dagger\\iU&0\end{pmatrix}
```

is Hermitian and squares to the identity. Its designated block in the $`|+\rangle`$ basis is

```math
(\langle+|\otimes I)B_0(|+\rangle\otimes I)
=\frac{i}{2}(U-U^\dagger)
=\sin H_0.
```

Changing this block basis to $`|0\rangle`$ uses only known Hadamard gates. The controlled evolution $`C_U`$ is the collision compiler at time $`1/2`$ for $`\mathsf H(L_{\mathcal E})`$, with an extra control. Its adjoint uses time $`-1/2`$. Both are generated using ordinary forward channel calls and fresh programs.

## A bounded odd inverse-sine polynomial

For an integer $`m\ge0`$, take the explicit Taylor truncation

```math
P_m(x)=\frac2\pi
\sum_{j=0}^{m}
\frac{\binom{2j}{j}}{4^j(2j+1)}x^{2j+1}.
```

It is a real odd polynomial of degree $`q=2m+1`$. All its coefficients are nonnegative, and the infinite coefficient sum is $`(2/\pi)\arcsin(1)=1`$. Therefore

```math
|P_m(x)|\le1
\qquad (-1\le x\le1).
```

Since $`\binom{2j}{j}/4^j\le1`$, the tail on the smaller interval obeys

```math
\sup_{|x|\le1/2}
\left|P_m(x)-\frac2\pi\arcsin x\right|
\le\frac2\pi\sum_{j=m+1}^{\infty}2^{-(2j+1)}
=\frac4{3\pi}4^{-(m+1)}.
```

Set $`\zeta=\delta/8`$ and, for example,

```math
m=\left\lceil\log_4\frac1\zeta\right\rceil,
\qquad q=2m+1.
```

The displayed approximation error is then at most $`\zeta`$, and $`q=O(1+\log(1/\delta))`$. The coefficients can be evaluated directly or by their elementary recurrence. This is a concrete instance of the bounded odd inverse-sine approximation in Lemma 70 of [Gilyén et al., arXiv:1806.01838](https://arxiv.org/abs/1806.01838).

Real-polynomial singular value transformation, Corollary 18 of that work, applies to a real matching-parity polynomial bounded by one on the full signal interval. Its coherent combination of the two phase sequences uses one additional qubit and introduces no further factor $`1/2`$ in the designated polynomial block. Applied to $`B_0`$, it gives an ideal unitary $`V_P`$ whose designated block is

```math
B=P_m(\sin H_0).
```

For a Hermitian input and an odd polynomial, singular value transformation agrees with the Hermitian polynomial functional calculus. Thus $`B`$ is Hermitian and commutes with $`H_0`$ and $`A`$. Since $`\Vert\sin H_0\Vert\le\sin(1/2)<1/2`$ and $`\arcsin(\sin H_0)=H_0`$,

```math
\Vert B-A\Vert_\infty\le\zeta.
```

There is also a useful strict contraction bound. For $`0\le h\le1/2`$, positivity of the Taylor coefficients gives

```math
0\le P_m(\sin h)
\le\frac2\pi\arcsin(\sin h)
=\frac2\pi h.
```

Oddness handles negative $`h`$. Consequently $`\Vert A\Vert_\infty,\Vert B\Vert_\infty\le1/\pi<1/2`$. The ideal QSVT circuit uses $`O(q)`$ occurrences of controlled $`U`$ and its inverse, together with known operations.

## Stable completion of the whole unitary

We now replace the approximate designated block $`B`$ by $`A`$ while controlling the change in the entire unitary. The following argument is an existence proof for the comparison unitary; the implementation does not have to determine its complementary blocks.

Let $`\mathcal D`$ be the designated block subspace and write its orthogonal complement as $`\mathcal K`$. Decompose an arbitrary unitary with Hermitian designated block $`B`$ as

```math
V=\begin{pmatrix}B&C\\D&E\end{pmatrix}
\quad\text{on }\mathcal D\oplus\mathcal K.
```

Put $`S_B=\sqrt{I-B^2}`$. It is invertible because $`\Vert B\Vert<1`$. The unitary relations imply

```math
CC^\dagger=S_B^2,
\qquad D^\dagger D=S_B^2.
```

Hence

```math
C=S_B C_0^\dagger,
\qquad D=D_0S_B,
\qquad C_0^\dagger C_0=D_0^\dagger D_0=I_{\mathcal D},
```

where $`C_0,D_0:\mathcal D\to\mathcal K`$ are isometries. Complete them to unitaries on $`\mathcal K`$. In the resulting input and output complement bases, the cross relations of $`V^\dagger V=VV^\dagger=I`$ force the active lower-right block to be $`-B`$ and its couplings to the remaining complement to vanish. The unused lower-right block is itself unitary. Thus there are unitaries $`L,R,Q`$ such that

```math
V=(I\oplus L)(J_B\oplus Q)(I\oplus R),
\qquad
J_B=\begin{pmatrix}B&S_B\\S_B&-B\end{pmatrix}.
```

If the complement has no unused part, $`Q`$ is absent. This factorization is possible because the complement has dimension at least $`\dim\mathcal D`$, as also follows from invertibility of $`S_B`$.

Define $`S_A=\sqrt{I-A^2}`$ and replace only the active middle unitary:

```math
V_A=(I\oplus L)(J_A\oplus Q)(I\oplus R),
\qquad
J_A=\begin{pmatrix}A&S_A\\S_A&-A\end{pmatrix}.
```

The operator $`V_A`$ is unitary and its designated block is exactly $`A`$. Since $`A`$ and $`B`$ commute, simultaneous functional calculus reduces the norm of $`J_A-J_B`$ to scalar pairs $`a,b`$. On $`[-1/2,1/2]`$, the derivative of $`s(x)=\sqrt{1-x^2}`$ has magnitude at most $`1/\sqrt3`$. Therefore

```math
\begin{aligned}
\Vert V_A-V\Vert_\infty
&=\Vert J_A-J_B\Vert_\infty\\
&\le\max_{(a,b)\in\mathrm{joint\,spec}(A,B)}
\sqrt{(a-b)^2+
\left(\sqrt{1-a^2}-\sqrt{1-b^2}\right)^2}\\
&\le\frac2{\sqrt3}\Vert A-B\Vert_\infty
<2\zeta.
\end{aligned}
```

For any two unitaries $`W_1,W_2`$, adjoining an arbitrary reference and expanding the two conjugations gives

```math
\Vert\mathrm{Ad}_{W_1}-\mathrm{Ad}_{W_2}\Vert_\diamond
\le2\Vert W_1-W_2\Vert_\infty.
```

Apply this completion to $`V=V_P`$ and denote the resulting $`V_A`$ by $`V_{\mathcal E}`$. It follows that

```math
\Vert\mathrm{Ad}_{V_P}
-\mathrm{Ad}_{V_{\mathcal E}}\Vert_\diamond
\le4\zeta=\delta/2.
```

This comparison controls the full channel and fixes one exact comparison unitary for the rest of the construction.

## Ordinary-channel query count

Let $`r\le c_0q`$ be the number of controlled-evolution primitives in a fixed QSVT realization, for a numerical constant $`c_0`$. Implement each primitive to unhalved diamond error at most

```math
\eta=\frac{\delta}{2c_0q}.
```

The collision compiler at time $`1/2`$, with any needed extra controls, uses $`O(d^2/\eta)`$ ordinary calls per primitive. Contractivity and telescoping over the $`r`$ occurrences give

```math
\Vert\widetilde{\mathcal V}_{\mathcal E}
-\mathrm{Ad}_{V_P}\Vert_\diamond
\le r\eta\le\delta/2.
```

Combining this with stable completion proves the stated $`\delta`$ complete-channel error. The query total is

```math
O\!\left(q\frac{d^2}{\eta}\right)
=O\!\left(\frac{d^2q^2}{\delta}\right)
=O\!\left(\frac{d^2}{\delta}
\left[1+\log\frac1\delta\right]^2\right).
```

The programs are prepared using unconditional calls to $`\mathcal E`$. Coherent controls act only on the subsequent known collision interactions and known gates. Thus coherent control of the compiled primitive does not introduce a controlled unknown-channel oracle.

## Inverse and controlled versions

Reverse the ideal QSVT circuit and replace every ideal controlled evolution by the inverse-time collision construction. This produces a physical channel close to $`\mathrm{Ad}_{V_P^\dagger}`$ with the same error and query bounds. The same stable completion already fixed $`V_{\mathcal E}`$, and

```math
\Vert V_P^\dagger-V_{\mathcal E}^\dagger\Vert_\infty
=\Vert V_P-V_{\mathcal E}\Vert_\infty.
```

Therefore the inverse implementation is $`\delta`$-close to $`\mathrm{Ad}_{V_{\mathcal E}^\dagger}`$ for that same exact comparison unitary.

Likewise, coherently control the known ideal QSVT sequence and its constituent compiled evolutions. Since

```math
\Vert C_{V_P}-C_{V_{\mathcal E}}\Vert_\infty
=\Vert V_P-V_{\mathcal E}\Vert_\infty,
```

the resulting channel is $`\delta`$-close to the controlled version of the same $`V_{\mathcal E}`$. These controls and inverses are output capabilities of the compiler. They do not assert that an arbitrary approximate physical channel can be inverted or controlled after the fact.

## Relation to spectral algorithms and limits

Niwa et al., [arXiv:2506.24112v3](https://arxiv.org/html/2506.24112v3), Theorem 1 and its proof following Eq. (15), use this sine and inverse-sine route to obtain a complete unitary block-encoding interface from ordinary unknown-channel access. Gilyén et al., [arXiv:1806.01838](https://arxiv.org/abs/1806.01838), Corollary 18 and Lemma 70, supply the polynomial transformation tools. Those mechanisms are inherited. The collision second-moment evaluation supplies the improved dimension dependence, and the completion argument above records explicitly the full-channel interpretation needed here.

The output has the constant normalization $`1/\pi`$. The [dimension lower bound](dimension-lower-bound.md) therefore applies at fixed sufficiently small error. The upper bound's $`1/\delta`$ factor and logarithms are not asserted to be optimal. No precision converse follows from this compilation argument, and applying a further spectral transformation requires counting its additional calls and error budget.
