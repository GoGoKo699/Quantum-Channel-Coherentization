# Thirty milestones for Quantum Channel Coherentization

This is a common understanding map for the scientific contribution. It has exactly 30 milestones: **12 background/preliminary milestones** and **18 narrative/innovation milestones**. The background joins channel theory, matrix representations, coherent operations and error measures into one input-output problem. The narrative builds the compiler, derives its cost, reconstructs the inversion obstruction, and then integrates the scope and significance of the result. Each phase moves from local objects to a global account.

The sole educational anchor is John Watrous, *The Theory of Quantum Information* (2018), abbreviated **[W]**. The [Watrous bridge](WATROUS_BRIDGE.md) explains the relevant sections, notation translations and locally supplied steps. Sections cited below refer to that edition; they are entry points, not a requirement to read whole chapters. Niwa et al. (**[N]**), Gilyén et al. (**[G]**) and Chen–Yu–Zhang (**[C]**) are primary research dependencies, not additional educational anchors. The local proofs remain the authoritative statements of this project's assumptions and claims.

The map records understanding targets and dependencies. It contains no learner assessments or personal coaching procedure, and does not claim to cover every technical lemma or neighboring problem.

## Background and preliminaries — M01–M12

### M01 — States, vectors and linear operators

- **ID and phase:** M01; background/preliminaries.
- **Central question:** What mathematical objects describe a quantum input and an operation acting on it?
- **Understanding target:** Distinguish a state vector, a density operator and a linear map on operators; explain why a coherent matrix algorithm acts on vectors even when its matrix originated from a channel.
- **Dependencies and story role:** No earlier milestone; establishes the objects that the rest of the map connects.
- **Conceptual connection:** Separating these object types prevents confusing a physical channel output with a vectorized operator.
- **Source pointers:** [W] §§1.1, 2.1; [model: fixed basis and vectorization](../science/model.md#fixed-basis-and-vectorization).

### M02 — An ordinary call to an unknown channel

- **ID and phase:** M02; background/preliminaries.
- **Central question:** What does black-box access to a physical channel actually supply?
- **Understanding target:** Explain complete positivity, trace preservation and a memoryless ordinary invocation; distinguish that invocation from supplied Kraus operators, a reversible dilation, a controlled channel or environmental access.
- **Dependencies and story role:** M01; turns the mathematical map into the concrete resource available to the compiler.
- **Conceptual connection:** A representation can describe a channel without being an accessible quantum oracle for that representation.
- **Source pointers:** [W] §2.2; [model: access and charged resources](../science/model.md#access-and-charged-resources).

### M03 — Composite data and untouched references

- **ID and phase:** M03; background/preliminaries.
- **Central question:** Why must the compiled operation work when its input is entangled with another register?
- **Understanding target:** Explain tensor-product registers, reduced states and discarding; identify which register carries the requested output and which registers may be consumed or ignored.
- **Dependencies and story role:** M01–M02; expands a single input-output operation into the setting needed for a composable guarantee.
- **Conceptual connection:** Partial trace is a permitted physical operation, while a guarantee for one input does not imply a guarantee on reference-entangled data.
- **Source pointers:** [W] §§2.1, 2.1.3, 2.2; [model: target evolution](../science/model.md#target-evolution-and-normalization), [error convention](../science/model.md#error-convention).

### M04 — The Liouville matrix and its basis convention

- **ID and phase:** M04; background/preliminaries.
- **Central question:** How does a map on operators become a matrix acting on vectors?
- **Understanding target:** Use the stated vectorization convention to explain the Liouville matrix and derive the unitary-channel form $`U\otimes\overline U`$; distinguish adjoint, transpose and complex conjugation.
- **Dependencies and story role:** M01–M03; supplies the particular matrix whose coherent use is the research target.
- **Conceptual connection:** Fixing the basis and index order determines which factor later contains the actual unknown inverse.
- **Source pointers:** [W] §§1.1.2, 2.2.2; [model: fixed basis and vectorization](../science/model.md#fixed-basis-and-vectorization).

### M05 — A normalized Choi state from one query

- **ID and phase:** M05; background/preliminaries.
- **Central question:** What program specimen can one ordinary channel call prepare?
- **Understanding target:** Explain preparation of $`J_{\mathcal E}`$ from a normalized maximally entangled input, its normalization, and the marginal fixed by trace preservation; distinguish this mixed specimen from an accessible purification.
- **Dependencies and story role:** M02–M04; connects the physical oracle to the disposable program used in the construction.
- **Conceptual connection:** Channel-state correspondence provides a one-query resource without supplying a reversible preparation oracle.
- **Source pointers:** [W] §§2.1.3, 2.2.2; [model: normalized Choi state](../science/model.md#fixed-basis-and-vectorization).

### M06 — What unitality changes

- **ID and phase:** M06; background/preliminaries.
- **Central question:** Why is preservation of the identity a consequential promise here?
- **Understanding target:** Explain the second flat Choi marginal and Hilbert–Schmidt contraction; connect these to a dimension-independent norm for the Liouville matrix without assuming every unital channel is a mixture of unitaries.
- **Dependencies and story role:** M02, M04–M05; identifies the promise that will support both constant normalization and the improved collision bound.
- **Conceptual connection:** A channel property has one consequence for its matrix norm and another for the state used to program the matrix.
- **Source pointers:** [W] §§4.1.1, 4.2.2; [model: target normalization](../science/model.md#target-evolution-and-normalization).

### M07 — Swaps and entangled contractions

- **ID and phase:** M07; background/preliminaries.
- **Central question:** How can known interactions turn a program state's entries into a data Hamiltonian?
- **Understanding target:** Explain the swap operator and maximally entangled projector, and follow the partial-trace identities that produce an ordinary or partially transposed program moment.
- **Dependencies and story role:** M03–M05; introduces the two concrete contractions needed for the collision interaction.
- **Conceptual connection:** Transposition can appear in a derived Hamiltonian coefficient without being performed as a standalone physical transposition map.
- **Source pointers:** [W] §§1.1.2, 2.1, 2.2.2; [compiler: programs and first moments](../science/collision-compiler.md#programs-and-their-first-moments).

### M08 — Hermitian lifts and coherent evolution

- **ID and phase:** M08; background/preliminaries.
- **Central question:** How can a generally non-Hermitian channel matrix define a unitary target?
- **Understanding target:** Explain the flag-qubit Hermitian lift, its two off-diagonal blocks and the evolution it generates; distinguish this enlarged-space unitary from applying the original channel to a density operator.
- **Dependencies and story role:** M04, M06–M07; completes the target object independently of the later implementation.
- **Conceptual connection:** The adjoint block makes the lift Hermitian and later enables the inversion reduction.
- **Source pointers:** [W] §1.1; [model: target evolution and normalization](../science/model.md#target-evolution-and-normalization), [interpretation](../science/interpretation.md).

### M09 — Error for a complete quantum operation

- **ID and phase:** M09; background/preliminaries.
- **Central question:** What does it mean to approximate the requested output uniformly?
- **Understanding target:** Explain the unhalved diamond norm, reference systems and contractivity under initialization, discarding and composition; distinguish an operator-norm bound, a normalized Choi diagnostic and a full-channel guarantee.
- **Dependencies and story role:** M03, M08; supplies the error language used by both construction and converse.
- **Conceptual connection:** The same composable error measure permits local collision errors to be summed and an inverse to be extracted safely.
- **Source pointers:** [W] §§3.2, 3.3.2–3.3.3; [model: error convention](../science/model.md#error-convention), [verification limits](../verification/README.md#limits-of-this-report).

### M10 — Known control and relative phase

- **ID and phase:** M10; background/preliminaries.
- **Central question:** When can a coherent control be implemented without controlling the unknown channel?
- **Understanding target:** Explain the Hamiltonian $`|1\rangle\langle1|\otimes H`$, the significance of relative phase between active and inactive branches, and why controlling known post-preparation interactions is an operationally different task from a controlled unknown-channel call.
- **Dependencies and story role:** M02, M05, M08–M09; resolves the control distinction before it is used in block encoding.
- **Conceptual connection:** A mixed program can be prepared unconditionally while the subsequent known interaction carries the data control coherently.
- **Source pointers:** [W] §§1.1, 2.2; [compiler: coherent control and negative time](../science/collision-compiler.md#coherent-control-and-negative-time), [resources: finite synthesis](../science/resources.md#finite-gate-synthesis).

### M11 — Designated blocks and polynomial transformations

- **ID and phase:** M11; background/preliminaries.
- **Central question:** What coherent interface does a matrix-based quantum algorithm need?
- **Understanding target:** Explain a designated ancilla block, its normalization and its complementary unitary blocks; distinguish an accurate block from approximation to a complete unitary, and understand what a polynomial functional calculus requests.
- **Dependencies and story role:** M01, M08–M10; introduces the output interface whose resource cost the project will characterize.
- **Conceptual connection:** The locally supplied block-encoding explanation joins Watrous's operator theory to the research-level QSVT dependency.
- **Source pointers:** [W] §1.1; [block compiler: output guarantee](../science/block-encoding.md#output-and-error-guarantee); [G], Corollary 18, as a research dependency.

### M12 — The whole ordinary-access conversion problem

- **ID and phase:** M12; background/preliminaries.
- **Central question:** What precisely must be converted, produced and paid for?
- **Understanding target:** Give one consistent account of ordinary memoryless unital-channel access, one-query Choi programs, the Liouville-lift target, complete-channel error, controls, normalization and charged resources; identify stronger supplied interfaces as different problems.
- **Dependencies and story role:** M01–M11; synthesizes the background into the scientific question rather than adding another isolated prerequisite.
- **Conceptual connection:** This input-output contract explains why a matrix representation is not already a free coherent oracle.
- **Source pointers:** [W] §§2.2, 3.3, 4.2.2; [model](../science/model.md), [resource account](../science/resources.md).

## Narrative and innovation — M13–M30

### M13 — Two mixed controlled-SWAP programs

- **ID and phase:** M13; narrative/innovation.
- **Central question:** Which physical states expose the desired off-diagonal channel matrix?
- **Understanding target:** Explain the roles of $`J_{\mathcal E}`$, the known controlled swap and the two program flag signs; account for one ordinary query per disposable program.
- **Dependencies and story role:** M05, M07, M12; begins the construction with its actual physical ingredients.
- **Conceptual connection:** Opposite flag coherences allow common diagonal blocks to cancel in a difference of first moments.
- **Source pointers:** [W] §§2.1–2.2; [compiler: programs and first moments](../science/collision-compiler.md#programs-and-their-first-moments); [N], Eqs. (9)–(14).

### M14 — The first moment, the twist and the time scale

- **ID and phase:** M14; narrative/innovation.
- **Central question:** Why does the program difference encode the intended Liouville lift rather than a transposed or misnormalized matrix?
- **Understanding target:** Follow the partial-transpose identities, the known controlled-SWAP twist and its removal; explain why collision time must total $`dt`$ to obtain target time $`t`$.
- **Dependencies and story role:** M04, M07–M08, M13; identifies the exact generator before estimating implementation error.
- **Conceptual connection:** Index conventions, the normalized Choi factor and the final conjugation jointly determine the operational target.
- **Source pointers:** [W] §§1.1.2, 2.2.2; [compiler: first moments](../science/collision-compiler.md#programs-and-their-first-moments).

### M15 — The inherited variance bound

- **ID and phase:** M15; narrative/innovation.
- **Central question:** Which property of a program controls its reduced collision error?
- **Understanding target:** Explain the first moment $`K`$, second moment $`M`$, and variance $`M-K^2`$; reconstruct how compression and leakage yield an all-time diamond bound, while recognizing that the proof's purification is not supplied access.
- **Dependencies and story role:** M03, M07, M09, M14; isolates the inherited error mechanism that the project specializes.
- **Conceptual connection:** An evaluated program moment can be much smaller than a bound using only the joint interaction norm.
- **Source pointers:** [W] §§2.1.3, 3.3; [compiler: program-variance bound](../science/collision-compiler.md#the-inherited-program-variance-bound), [related work: moment-sensitive exponentiation](../references/RELATED_WORK.md#moment-sensitive-exponentiation-and-the-inherited-variance-estimate).

### M16 — The flat marginal removes a dimension factor

- **ID and phase:** M16; narrative/innovation.
- **Central question:** Where does the improved dimension dependence actually enter?
- **Understanding target:** Derive the relevant marginal of each mixed program and its exact collision second moment $`M=I`$; explain why unitality retains useful information that a worst-case interaction-norm estimate discards.
- **Dependencies and story role:** M06, M13–M15; supplies the construction's decisive unital-case specialization.
- **Conceptual connection:** The same flat-marginal promise that supported normalization now bounds the physical collision variance independently of dimension.
- **Source pointers:** [W] §4.2.2; [compiler: exact second moment](../science/collision-compiler.md#flat-marginal-and-exact-second-moment), [related work](../references/RELATED_WORK.md#moment-sensitive-exponentiation-and-the-inherited-variance-estimate).

### M17 — From one pair to a finite global compiler

- **ID and phase:** M17; narrative/innovation.
- **Central question:** How do the two local collisions produce the complete finite-budget theorem?
- **Understanding target:** Explain the opposite collision signs, chronological product, partial-transpose norm bound, commutator error and telescoping; recover the (2m)-query guarantee and its integer ceiling without hiding a small-step remainder.
- **Dependencies and story role:** M09, M14–M16; assembles the first full constructive result.
- **Conceptual connection:** The first-moment time scale and second-moment error must be combined before reading off the dimension cost.
- **Source pointers:** [W] §§1.1, 3.3; [compiler: pairing and total error](../science/collision-compiler.md#pairing-product-formula-and-total-error), [finite-budget theorem](../science/collision-compiler.md#finite-budget-theorem).

### M18 — Controls and inverses as generated outputs

- **ID and phase:** M18; narrative/innovation.
- **Central question:** How are coherent control and negative-time evolution obtained from forward channel calls?
- **Understanding target:** Track the controlled interaction's moments and the reversal of known collision angles; explain why fresh ordinary program preparations suffice and why an arbitrary noisy output channel is not being inverted after the fact.
- **Dependencies and story role:** M10, M15–M17; upgrades the evolution result to the interface required by the next construction.
- **Conceptual connection:** Controlling the physical synthesis preserves the chosen target phase, which ordinary channel-distance information alone would not provide.
- **Source pointers:** [W] §§2.2, 3.3; [compiler: control and negative time](../science/collision-compiler.md#coherent-control-and-negative-time), [resources: controlled collision](../science/resources.md#a-collision-has-a-small-known-circuit).

### M19 — Turning a short evolution into its generator

- **ID and phase:** M19; narrative/innovation.
- **Central question:** How can controlled evolution supply a matrix block proportional to the generator?
- **Understanding target:** Derive the sine block with its correct sign and explain why a bounded odd inverse-sine polynomial recovers the generator on the promised spectral interval.
- **Dependencies and story role:** M08, M11, M18; begins the inherited evolution-to-block route with explicit normalization.
- **Conceptual connection:** A small generator norm keeps the inverse-sine approximation away from its difficult endpoints.
- **Source pointers:** [W] §1.1; [block compiler: sine block](../science/block-encoding.md#an-exact-sine-block), [inverse-sine polynomial](../science/block-encoding.md#a-bounded-odd-inverse-sine-polynomial); [G], Lemma 70.

### M20 — The exact polynomial block

- **ID and phase:** M20; narrative/innovation.
- **Central question:** Which block does real-polynomial QSVT produce, including its normalization?
- **Understanding target:** Explain why odd singular-value transformation agrees with Hermitian polynomial calculus here, why the designated block has no additional factor one-half, and how its approximation to the Hermitian lift divided by pi is bounded.
- **Dependencies and story role:** M11, M19; fixes the exact ideal polynomial circuit before physical approximation is introduced.
- **Conceptual connection:** Matching parity and the strict contraction interval are material hypotheses, not interchangeable versions of a generic QSVT statement.
- **Source pointers:** [W] §1.1; [block compiler: inverse-sine polynomial](../science/block-encoding.md#a-bounded-odd-inverse-sine-polynomial); [G], Corollary 18.

### M21 — Completing one common comparison unitary

- **ID and phase:** M21; narrative/innovation.
- **Central question:** Why does an accurate polynomial block imply proximity to a complete unitary with the exact target block?
- **Understanding target:** Explain the active unitary completion, its strict-contraction stability bound and the role of commuting Hermitian blocks; show why forward, inverse and controlled implementations refer to the same exact comparison unitary.
- **Dependencies and story role:** M09–M11, M18–M20; closes the complete-operation gap that a block-only statement would leave.
- **Conceptual connection:** Existence of complementary blocks is sufficient for the comparison guarantee; their classical reconstruction is not an input resource.
- **Source pointers:** [W] §1.1; [block compiler: stable completion](../science/block-encoding.md#stable-completion-of-the-whole-unitary), [inverse and controlled versions](../science/block-encoding.md#inverse-and-controlled-versions).

### M22 — The block compiler's ordinary-query budget

- **ID and phase:** M22; narrative/innovation.
- **Central question:** How does the complete block construction translate into a channel-query count?
- **Understanding target:** Combine logarithmic polynomial degree, fixed-time evolution cost and per-primitive error allocation to obtain $`O(d^2\delta^{-1}[1+\log(1/\delta)]^2)`$; distinguish this sufficient precision dependence from the later dimension converse.
- **Dependencies and story role:** M09, M17–M21; integrates the constructive query frontier.
- **Conceptual connection:** Fresh program specimens and diamond-norm telescoping make the compositional error budget operational.
- **Source pointers:** [W] §3.3; [block compiler: ordinary-channel query count](../science/block-encoding.md#ordinary-channel-query-count), [resources: ordinary access](../science/resources.md#ordinary-channel-access-is-the-input).

### M23 — Gates, synthesis, memory and work return

- **ID and phase:** M23; narrative/innovation.
- **Central question:** Which costs remain after counting channel queries?
- **Understanding target:** Explain the Bell-projector test, swap-sign extraction, controlled rotation and uncomputation; distinguish constant block flags from logarithmic program/workspace, and account for known-gate precision, disposable programs and returned clean work.
- **Dependencies and story role:** M07, M10, M17–M22; completes the constructive resource account beyond the oracle count.
- **Conceptual connection:** A dimension-optimal query conversion need not be cheap in input qubit count or furnish an application-level advantage.
- **Source pointers:** [W] §§1.1, 2.2; [resources: collision circuit](../science/resources.md#a-collision-has-a-small-known-circuit), [finite synthesis](../science/resources.md#finite-gate-synthesis), [memory and work return](../science/resources.md#memory-and-work-return).

### M24 — Extracting the actual unknown inverse

- **ID and phase:** M24; narrative/innovation.
- **Central question:** What extra capability does coherent Liouville access expose even for a noiseless channel?
- **Understanding target:** Use the unitary subclass and time $`\pi/2`$ to select $`U^\dagger\otimes U^{\mathsf T}`$; explain why preparing and discarding a dummy factor yields the inverse on arbitrary reference-entangled data, rather than a transpose or complex conjugate.
- **Dependencies and story role:** M03–M04, M08, M17; starts the converse from a concrete operational reduction.
- **Conceptual connection:** The enlarged coherent output is harder than one ordinary forward invocation because it can act on an arbitrary live input with the inverse.
- **Source pointers:** [W] §§1.1.2, 2.2.2; [lower bound: direct coherent evolution](../science/dimension-lower-bound.md#direct-coherent-evolution), [unitary example](../science/examples.md#an-unknown-unitary).

### M25 — The robust inversion obstruction

- **ID and phase:** M25; narrative/innovation.
- **Central question:** Why does the dimension obstruction survive a fixed nonzero implementation error?
- **Understanding target:** Explain normalized Choi fidelity, its projector test, the unhalved-diamond factor and the Haar-averaged inversion bound; derive the direct-evolution lower bound under a hard query cap and recognize the imported theorem's scope.
- **Dependencies and story role:** M09, M24; converts the extraction into a robust dimension converse.
- **Conceptual connection:** An exact-only inversion theorem would not justify the approximate compiler lower bound.
- **Source pointers:** [W] §§3.2, 3.3; [lower bound: inversion theorem](../science/dimension-lower-bound.md#the-inversion-theorem-used), [direct evolution](../science/dimension-lower-bound.md#direct-coherent-evolution); [C], Theorem 3.7.

### M26 — A forward block is already enough

- **ID and phase:** M26; narrative/innovation.
- **Central question:** Does the block compiler need an accessible inverse before the lower bound applies?
- **Understanding target:** Explain constant-probability inverse extraction from one forward designated block, complete failure to a deterministic channel, and derive the fidelity lower bound $`c^2-\delta/2`$ and its useful error regime.
- **Dependencies and story role:** M11, M21–M22, M24–M25; aligns the converse with the exact interface constructed above.
- **Conceptual connection:** A successful branch contributes positive inverse fidelity even when the failure output is unrelated to the inverse.
- **Source pointers:** [W] §§2.3, 3.2–3.3; [lower bound: constant-normalization block](../science/dimension-lower-bound.md#a-constant-normalization-block-is-already-sufficient); [C], Theorem 3.7.

### M27 — Recovery with a known depolarizing component

- **ID and phase:** M27; narrative/innovation.
- **Central question:** What concrete finite-noise capability follows from the same compiler?
- **Understanding target:** Decompose the noisy-unitary Liouville matrix, explain the known commuting correction and time rescaling, and recover the clean unitary or inverse; identify known (p<1) as a supplied calibration promise and the bound as sufficient rather than optimal.
- **Dependencies and story role:** M04, M08, M17–M18, M24; demonstrates the operational meaning beyond the noiseless hard family.
- **Conceptual connection:** The maximally entangled identity direction makes the depolarizing correction independent of the unknown unitary.
- **Source pointers:** [W] §§2.2, 4.1–4.2; [examples: known depolarizing noise](../science/examples.md#depolarizing-noise-around-an-unknown-unitary), [related work: noisy-unitary purification](../references/RELATED_WORK.md#noisy-unitary-purification-and-the-open-precision-dependence).

### M28 — What the finite checks establish

- **ID and phase:** M28; narrative/innovation.
- **Central question:** Which consequential mistakes can the numerical diagnostics detect, and which claims still require proof?
- **Understanding target:** Explain the roles of complex nonsymmetric fixtures, nonunital boundaries, control checks, collision reconstruction and inverse negative controls; distinguish a normalized Choi-distance diagnostic from a diamond-norm upper certificate or general proof.
- **Dependencies and story role:** M09, M14–M18, M24, M27; connects the analytical claims to reproducible evidence without upgrading finite tests into universal guarantees.
- **Conceptual connection:** Verification is selected around orientation, normalization and operational failure modes, rather than treated as a test-count argument for correctness.
- **Source pointers:** [W] §§2.2.2, 3.3; [verification account](../verification/README.md), [verification report](../verification/report.json).

### M29 — Attribution, closest work and scope boundaries

- **ID and phase:** M29; narrative/innovation.
- **Central question:** What remains after the inherited constructions and material restrictions are stated?
- **Understanding target:** Separate the inherited Liouville programs, marginal-sensitive variance, QSVT and inversion theorem from the supported unital-case compiler and operational dimension frontier; explain the superseded preprint exponent, nonunital earlier hard family, and why virtual adjoints and ordered low-noise results are different claims.
- **Dependencies and story role:** M12–M28; evaluates the assembled contribution against its actual antecedents and neighboring tasks.
- **Conceptual connection:** Correct attribution and matched operational models determine the surviving scientific consequence.
- **Source pointers:** [W] §§2.2, 3.3, 4.2.2; [related work](../references/RELATED_WORK.md), [interpretation](../science/interpretation.md).

### M30 — The complete fixed-accuracy frontier

- **ID and phase:** M30; narrative/innovation.
- **Central question:** What can now be concluded about converting physical channel access into coherent matrix access?
- **Understanding target:** Connect the flat-marginal construction, complete block guarantee, robust inverse extraction and charged resources into the fixed-accuracy quadratic dimension law; preserve the suitable-time qualification, exponential qubit dependence, and open joint precision/time frontier while explaining the result's operational significance.
- **Dependencies and story role:** M12–M29; synthesizes the whole contribution and its limits without introducing a separate final curriculum.
- **Conceptual connection:** The constructive and converse mechanisms meet on one interface: ordinary unital-channel calls must pay for the coherent capability they generate.
- **Source pointers:** [W] §§2.2, 3.3, 4.2.2; [principal result](../README.md#principal-result), [resource frontier](../science/resources.md#what-the-resource-frontier-means), [matching regime and open questions](../science/dimension-lower-bound.md#what-is-matched-and-what-remains-open).

[W]: https://cs.uwaterloo.ca/~watrous/TQI/
[N]: https://arxiv.org/html/2506.24112v3
[G]: https://arxiv.org/abs/1806.01838
[C]: https://arxiv.org/abs/2507.05736v4
