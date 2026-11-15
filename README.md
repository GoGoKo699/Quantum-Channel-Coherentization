# Quantum Channel Coherentization

How expensive is converting ordinary access to an unknown quantum channel into a coherent operator for spectral quantum algorithms?

For an unknown unital channel on a d-dimensional system, the dimension dependence is quadratic at fixed accuracy. A collision construction simulates the Hermitian Liouville evolution using O(d² t²/δ) channel calls. At time π/2, any such universal simulator needs Ω(d²) calls at fixed sufficiently small diamond error, already on unitary channels. Constant-normalization block encodings have the same fixed-accuracy dimension order, with logarithmic precision factors in the constructive bound.

The output guarantee concerns the complete quantum operation, including reference-entangled inputs. The supplied interface is an ordinary memoryless channel: its dilation, inverse and controlled version are not provided. Every channel call used to prepare a Choi program is charged. Joint optimality in dimension and precision is not asserted.

The construction refines the Liouville compiler of Niwa, Rossi, Taranto and Murao, [arXiv:2506.24112v3](https://arxiv.org/abs/2506.24112v3). The converse transfers the robust unknown-unitary inversion bound of Chen, Yu and Zhang, [arXiv:2507.05736v4](https://arxiv.org/abs/2507.05736v4). The program-variance method and Hermitian-preserving map exponentiation are inherited ingredients.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
