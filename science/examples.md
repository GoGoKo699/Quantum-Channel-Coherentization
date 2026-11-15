# What the compiled interface enables

The compiler acts on vectorized data, rather than applying the original channel to a density matrix. The distinction is visible already for unitary channels, and it remains useful when known depolarizing noise is present.

## An unknown unitary

For $`\mathcal E_U=\mathrm{Ad}_U`$,

```math
L_U=U\otimes\overline U,
\qquad
\mathsf H(L_U)^2=I,
\qquad
e^{-i(\pi/2)\mathsf H(L_U)}=-i\mathsf H(L_U).
```

One flag sector therefore applies $`U^\dagger\otimes U^{\mathsf T}`$ to arbitrary vectorized data. Preparing the second factor in a fixed state and discarding it implements the inverse on the first factor. This is the exact extraction used in the [lower bound](dimension-lower-bound.md). A known pure input or a reference system entangled with that first factor makes no difference to the extraction.

The conclusion is worst case over arbitrary unknown unitaries. For a promised diagonal qubit unitary $`U_\theta=\mathrm{diag}(1,e^{i\theta})`$, for example, the known Pauli $`X`$ gives $`XU_\theta X=e^{i\theta}U_\theta^\dagger`$. One ordinary query then suffices for the inverse channel. Such additional structure changes the task and does not contradict a universal lower bound.

## Depolarizing noise around an unknown unitary

Suppose the unknown channel has the stronger supplied promise

```math
\mathcal E_{U,p}=(1-p)\mathrm{Ad}_U+p\mathcal D,
\qquad
\mathcal D(X)=\mathrm{Tr}(X)I/d,
\qquad 0\le p<1,
```

where $`p`$ is known and $`U`$ is unknown. Put $`a=1-p`$, $`V=U\otimes\overline U`$, and $`P=|\Phi_d\rangle\langle\Phi_d|`$. Vectorization gives

```math
L_{U,p}=aV+pP,
\qquad VP=PV=V^\dagger P=PV^\dagger=P.
```

The last equalities express that conjugation preserves the identity operator. With $`X_C`$ the Pauli $`X`$ on the Hermitian-lift flag,

```math
\mathsf H(L_{U,p})
=a\mathsf H(V)+pX_C\otimes P,
\qquad
[\mathsf H(V),X_C\otimes P]=0.
```

The commuting correction is known: it depends on $`p`$ and the computational-basis maximally entangled projector, not on $`U`$. Therefore

```math
e^{-i(t/a)\mathsf H(L_{U,p})}
\,e^{+i(tp/a)X_C\otimes P}
=e^{-it\mathsf H(V)}.
```

Compile the first factor with [the ordinary-query construction](collision-compiler.md), and implement the second using known gates. At $`t=\pi/2`$, the corrected operation gives either $`V`$ or $`V^\dagger`$, according to the input flag. Discarding one factor produces an approximation to the clean unknown channel $`\mathrm{Ad}_U`$ or its inverse on an arbitrary input. Diamond error is unchanged by the known correction, initialization and discarding.

In the ideal-known-gate convention, an explicit sufficient ordinary-query budget for unhalved error $`\epsilon`$ is

```math
Q_{\rm purify}
\le2\left\lceil
\frac{(4d^2+2)\pi^2}{4(1-p)^2\epsilon}
\right\rceil.
```

Known correction gates and finite synthesis are charged separately as in [the resource account](resources.md). This is an achievable finite-noise consequence of the same compiler. It is not an optimal purification theorem, and it has no favorable factor proportional to small $`p`$. At $`p=1`$, the physical channel is independent of $`U`$, so universal recovery is impossible; the stated construction excludes that endpoint and its bound diverges as it is approached.

The known $`p`$ is a calibration promise. A wrong value changes both the effective time and the correction. The theorem does not obtain that calibration for free or establish a robust finite-sample calibration protocol.

Niwa, Yoshida and Murao, [arXiv:2608.26061v1](https://arxiv.org/abs/2608.26061v1), establish optimal leading-noise purification and conjugation laws under specified ordered limits. Their result is distinct from this direct, all-$`p<1`$ sufficient bound. The ordered low-noise statement does not supply a uniform joint precision lower bound for channel coherentization.

## A simple qubit noise channel

For the depolarizing channel itself, $`U=I`$ and

```math
L_{I,p}=(1-p)I+pP,
\qquad
\mathsf H(L_{I,p})=X_C\otimes[(1-p)I+pP].
```

The identity direction has Liouville eigenvalue one, while all traceless directions have eigenvalue $`1-p`$. An ordinary invocation contracts those traceless components. The compiled coherent evolution instead uses those numbers as Hamiltonian coefficients and acts unitarily on arbitrary vectors of the enlarged data space. This is why the two interfaces are not interchangeable.

When $`p`$ is known, this example already has a known small circuit; it is an illustration, not a hard family. The universal compiler is useful as a guarantee for every unknown unital channel, without a supplied diagonalization or a specified noise decomposition.
