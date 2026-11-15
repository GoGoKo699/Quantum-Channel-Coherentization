# Learn the channel-coherentization result

Imagine being given a device that applies an unknown quantum process. You can send a register through it and retain the visible output. The device may lose information into an environment that you cannot inspect. A spectral quantum algorithm can require a different interface: a unitary operation on a larger register whose designated matrix block contains the process's Liouville matrix.

The scientific question is how many ordinary device uses are needed to build that interface. For every unknown unital channel, the compiler has quadratic dimension cost at fixed accuracy. A matching worst-case obstruction already comes from noiseless unknown unitary channels. Error is measured on the whole output operation, including data entangled with an untouched reference; an accurate value of one observable would be a weaker task.

| Object | What it supplies |
| --- | --- |
| Ordinary channel call | One physical input-output use of the unknown process |
| Liouville matrix | A coefficient representation of the same linear map on operators |
| Coherent target | A compiled unitary operation acting on arbitrary vectors of an enlarged data space |

Writing down a matrix representation does not supply the corresponding quantum gate. In particular, the two vectorization registers are actual computational data registers in the compiled target; their input need not be the coefficients of a physical density matrix.

## Start with one source and the project map

The educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. The [Watrous bridge](WATROUS_BRIDGE.md) identifies the relevant sections, translates notation, and supplies the steps from textbook channel theory to this problem. It is a route into the science, rather than an instruction to read the whole book first.

The [30-milestone map](MILESTONES.md) is the common understanding route. Its 12 background milestones assemble individual objects into the complete input-output task. Its 18 narrative milestones assemble the compiler, the converse and their meaning. This allocation follows the project: understanding the representation is the starting point, while the main work is connecting the construction's resource accounting to an unrestricted dimension obstruction.

| Part of the route | Main question | Connected reading |
| --- | --- | --- |
| M01–M12: background | What is given, what is requested, and how is error measured? | [Watrous bridge](WATROUS_BRIDGE.md) and [model](../science/model.md) |
| M13–M23: construction | How do ordinary calls become a complete coherent operation? | [Collision compiler](../science/collision-compiler.md), [block encoding](../science/block-encoding.md) and [resources](../science/resources.md) |
| M24–M26: converse | Why must even the best universal compiler pay quadratically in dimension? | [Inverse extraction and lower bound](../science/dimension-lower-bound.md) |
| M27–M30: synthesis | What can the interface do, what was checked, and what is actually matched? | [Examples](../science/examples.md), [verification](../verification/README.md), [related work](../references/RELATED_WORK.md) and [interpretation](../science/interpretation.md) |

The map records each milestone's understanding target, dependencies and exact source pointers. The [scientific reading route](../science/README.md) provides a direct path through the proofs.

## Follow the causal chain

**Unitality enters twice.** A unital channel preserves the maximally mixed state. First, this makes its Liouville matrix a contraction, so a constant block normalization is possible. Second, it makes the relevant program marginal maximally mixed. These are different uses of the same promise; the second is what improves the collision cost.

**One ordinary call supplies one consumable program.** Prepare a known maximally entangled state, apply the unknown channel to one half, and use a known controlled swap. The resulting mixed program is not a purification or a reversible description of the channel. Its first collision moment is the average Hamiltonian seen by the data and contains the desired Liouville matrix. Its second moment controls fluctuations about that average; it is exactly the identity in the unital case. The inherited program-variance estimate turns these evaluated moments into a complete-channel error bound.

**Many small collisions build the target.** The two programs are paired with opposite known collision signs. Fresh programs let the errors be composed and every channel call counted. Changing the signs or controlling the known interactions generates inverse or controlled target evolutions; it does not require an inverse or controlled invocation of the unknown device.

**The block guarantee concerns the whole operation.** A sine block and a bounded inverse-sine polynomial produce an accurate designated block. Stable unitary completion then shows that the entire implemented channel is close to one exact block unitary with block $`\mathsf H(L_{\mathcal E})/\pi`$. This is stronger than checking that one submatrix is accurate on its own.

**The converse exposes an inverse capability.** For an unknown unitary channel, the doubled Liouville lift contains a sector acting as the inverse unitary on one data factor. A universal coherent compiler would therefore implement an unknown inverse. The established inversion fidelity bound supplies the quadratic dimension obstruction. This argument tests the capability of the output interface, rather than the variance analysis of the proposed construction.

## Read the conclusion with its conditions

The matched law holds when accuracy is fixed at a sufficiently small constant and the evolution time is fixed appropriately:

```math
Q(d)=\Theta(d^2).
```

Here $`d`$ is the unknown channel's input dimension. For $`n`$ input qubits, $`d=2^n`$, so the worst-case conversion costs $`\Theta(4^n)`$ ordinary calls. This is a statement about building a coherent interface, not an application-level quantum–classical speedup.

The construction's dependence on precision and time is an upper bound; the dimension converse does not make those dependences optimal. The supplied channel is unital and memoryless, and known gates, finite synthesis, disposable programs and workspace remain charged separately. The [known-noise example](../science/examples.md) is an achievable recovery construction with a calibrated noise parameter, not an optimal purification law.

The learning route uses the same definitions and scope as the proofs. Finite diagnostics help check conventions and examples; they do not replace the analytical all-channel guarantee.
