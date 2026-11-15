# Finite verification

The numerical checks below concern finite algebraic consistency. The separate
[hosted mathematics workflow](../.github/workflows/hosted-math.yml) visits every
tracked Markdown page at its exact pull-request head revision, using a fresh
anonymous Chromium context at widths 1440 and 760. Its
[collector](hosted-tools/capture_hosted_math.cjs) and
[text checker](hosted-tools/check_rendered_math.py) compare complete source and
hosted MathML, counts, relations and bounded display geometry. Reports, HTML and
screenshots are retained as temporary workflow artifacts. A structural pass
still requires visual inspection and does not certify the scientific proofs.
The job has only `contents: read`, persists no checkout credentials, and uses
neither repository secrets nor account or certificate-setting changes.

Run from the repository root:

```bash
python3 verification/verify.py --output verification/report.json
```

The script exits with status zero only when every declared diagnostic passes.
It uses a fixed seed and records Python, NumPy, SciPy, platform, timestamp and
residual tolerance in the JSON report. The script requires NumPy and SciPy.

## What is reconstructed

For dimensions 2, 3 and 4, four generic complex Haar unitaries are combined with
nonuniform positive weights. These give unital channels with complex,
generally nonsymmetric Kraus operators. The script constructs each normalized
Choi state directly from its Kraus operators, prepares both controlled-SWAP
program states, and checks:

- trace preservation and program normalization;
- the exact program marginal `(I + E(I))/(2d)`;
- the partially transposed program difference and its Liouville/SWAP form;
- removal of the twist by the known controlled SWAP;
- the bound `||rho_±^(T_Z)|| <= lambda/d`, with
  `lambda = (1 + ||E(I)||)/2`;
- extension by a known control and reversal of the target evolution.

For dimensions 2 and 3, the full collision Hamiltonian is built as a matrix in
the physical tensor order. Its first moment is compared with the program
partial transpose. Its second moment is compared with
`I_A' tensor (I + E(I)^T)/2`; the unital fixtures therefore have second moment
equal to identity. Pure-reset channels in dimensions 2 and 3 test the
nonunital boundary, including the factor `(1+d)/2`.

For both program signs, dimensions 2 and 3 use actual matrix exponentials at
three positive/negative step sizes. The reduced collision channel is then
reconstructed through an explicit environment trace and Kraus operators.
Its normalized Choi trace distance from the ideal unitary channel is recorded,
together with the error divided by the squared step size and the inherited
analytic threshold `2 h^2 ||M-K^2||`. Dimension 2 also
runs these full-channel diagnostics for the nonunital reset boundary.
The chronological plus/minus collision pair is reconstructed separately at one
step size and compared with the exponential of the program difference, checking
the inverse sign, composition order and product-formula target together.

## Inversion extraction and negative controls

Independent complex nonsymmetric unitary fixtures in dimensions 2, 3 and 4
test the complete algebraic extraction chain. The generator is reconstructed
through the Choi/program/partial-transpose construction, rather than inserted
from the desired answer. Matrix exponentiation at time `pi/2` is checked
against `-i Herm(L)`, where `L = U tensor conjugate(U)`.

Starting the flag in zero selects `L^dagger`. Starting the second system in
zero and discarding it gives the `U^dagger` channel on the first system. The
script checks the complete normalized Choi matrix of this output channel.
Comparisons against the transpose and complex-conjugation channels are
required to be visibly nonzero, so a convention error cannot pass on a real
or symmetric fixture.

## Known depolarizing correction

For dimensions 2 and 3, the complex unitary fixtures are mixed with a known
depolarizing component at probabilities `p=0.2` and `p=0.8`. The noisy generator
is reconstructed from its noisy Choi state and the program construction. The
script checks its decomposition as
`(1-p) Herm(U tensor conjugate(U)) + p X_flag tensor Phi`, invariance of the
maximally entangled vector, and commutation with the known correction term.
Actual matrix exponentials verify the time-rescaled correction at `t=pi/2`.
The extracted inversion is checked both as a complete Choi matrix and on an
explicit reference-entangled purification, including the discarded dummy
system. These checks concern the exact known-noise model; they do not establish
noise calibration, a noisy-query lower bound or precision optimality.

## Polynomial and stable-completion diagnostics

Unitary channels and generic complex unital mixtures in dimensions 2 and 3
also test the explicit odd Taylor inverse-sine polynomial at truncation indices
`m=2,5,9`. A 20,001-point grid samples the full interval `[-1,1]` for the
bounded-polynomial claim; a 10,001-point grid samples `[-1/2,1/2]` for the stated
Taylor-tail bound. The positive coefficient sum is recorded separately.

The actual sine block is constructed from controlled matrix exponentials and
compared with spectral functional calculus. Matrix Horner evaluation then
checks `B=P_m(sin(H_0))` against the exact target `A=H(L)/pi`, including
Hermiticity, commutation, the tail bound and the strict contraction bound.

The Julia comparison unitaries `J_B` and `J_A` are built by spectral positive
square roots. They are embedded in arbitrary input/output complement bases,
with an additional unused unitary block, to test the completion argument beyond
one chosen basis. Checks cover full unitarity, the exact designated top block,
the operator bound `(2/sqrt(3)) ||A-B||`, and consistency of the induced
normalized Choi trace distance with twice the operator difference. Pure-state
Choi distance is evaluated stably without allocating a large Choi matrix.

These are polynomial and comparison-unitary diagnostics. They do **not**
execute a phase-synthesized QSVT circuit or numerically certify a diamond-norm
upper bound. A sampled grid is not a proof of an interval-wide inequality.

## Limits of this report

These are finite floating-point diagnostics. They are not interval
certificates, an independent proof of the general theorem, a physical device
benchmark, or a hosted-rendering review.

In particular, normalized Choi trace distance is a **lower bound** on diamond
distance. Its being below the analytic diamond bound is a necessary
consistency check, not a numerical upper certificate for that norm. No
diamond-norm semidefinite program is performed. The proof of the uniform
diamond bound must include arbitrary reference systems separately.

Dimension 4 omits the large full collision matrix and collision-channel
diagnostics. Its program identities and inversion extraction are still
checked explicitly. The report records the coverage of each case.
