#!/usr/bin/env python3
"""Finite floating-point diagnostics for the coherentization construction.

The collision channel is reconstructed from a full matrix exponential and Kraus
operators. Its normalized Choi trace distance is a diagnostic, NOT a diamond-norm
upper certificate. The analytic proof owns the dimension-uniform diamond bound.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import block_diag, expm


SEED = 20261115
TOL = 5e-11


def fro(a):
    return float(np.linalg.norm(a, "fro"))


def op(a):
    return float(np.linalg.norm(a, 2))


def trace_norm_hermitian(a):
    return float(np.abs(np.linalg.eigvalsh((a + a.conj().T) / 2)).sum())


def haar(d, rng):
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    phase = np.diag(r) / np.abs(np.diag(r))
    return q @ np.diag(phase.conj())


def swap(d):
    s = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            s[i * d + j, j * d + i] = 1
    return s


def choi_from_kraus(kraus):
    d = kraus[0].shape[1]
    # Row-major vectorization: output index first, input index second.
    return sum(np.outer(k.ravel(), k.ravel().conj()) for k in kraus) / d


def liouville_from_kraus(kraus):
    return sum(np.kron(k, k.conj()) for k in kraus)


def partial_transpose_b(rho, a, b):
    return rho.reshape(a, b, a, b).transpose(0, 3, 2, 1).reshape(a * b, a * b)


def marginal_b(rho, a, b):
    return np.einsum("abac->bc", rho.reshape(a, b, a, b))


def marginal_a(rho, a, b):
    return np.einsum("abcb->ac", rho.reshape(a, b, a, b))


def programs(j, d):
    f = swap(d)
    c = np.zeros((2 * d * d, 2 * d * d), dtype=complex)
    c[:d*d, :d*d] = np.eye(d*d)
    c[d*d:, d*d:] = f
    out = []
    for sign in (1, -1):
        ket = np.array([1, sign], dtype=complex) / np.sqrt(2)
        out.append(c @ np.kron(np.outer(ket, ket.conj()), j) @ c.conj().T)
    return out, c


def collision_hamiltonian(a, b):
    # Tensor order after permutation: (program A,B; target A',B').
    bell = np.eye(b).ravel()
    raw = np.kron(swap(a), np.outer(bell, bell.conj()))
    dims = (a, a, b, b, a, a, b, b)
    return raw.reshape(dims).transpose(0, 2, 1, 3, 4, 6, 5, 7).reshape((a*b)**2, (a*b)**2)


def reduced_moment(v, rho):
    p = rho.shape[0]
    return np.einsum("iajb,ji->ab", v.reshape(p, p, p, p), rho)


def collision_choi(unitary, rho):
    """Full output Choi state via a program eigenbasis and environment trace."""
    p = rho.shape[0]
    vals, vecs = np.linalg.eigh((rho + rho.conj().T) / 2)
    vals = np.maximum(vals, 0)
    # U[e,a,p,b], where e,p are program and a,b target indices.
    u = unitary.reshape(p, p, p, p)
    kraus = np.einsum("eapb,ps,s->esab", u, vecs, np.sqrt(vals))
    flat = kraus.reshape(p*p, p*p)
    return flat.T @ flat.conj() / p


def unitary_choi(u):
    return np.outer(u.ravel(), u.ravel().conj()) / u.shape[0]


def check_case(d, kraus, label, full_collision=False):
    j = choi_from_kraus(kraus)
    l = liouville_from_kraus(kraus)
    e_i = sum(k @ k.conj().T for k in kraus)
    nu = op(e_i)
    lam = (1 + nu) / 2
    (rp, rm), c = programs(j, d)
    hp = partial_transpose_b(rp, 2*d, d)
    hm = partial_transpose_b(rm, 2*d, d)
    f = swap(d)
    zero = np.zeros_like(l)
    h_twist = np.block([[zero, l @ f], [f @ l.conj().T, zero]])
    h = np.block([[zero, l], [l.conj().T, zero]])
    expected_b = (np.eye(d) + e_i) / (2*d)
    residuals = {
        "trace_preservation": fro(sum(k.conj().T @ k for k in kraus) - np.eye(d)),
        "choi_trace": abs(float(np.trace(j).real) - 1),
        "plus_program_trace": abs(float(np.trace(rp).real) - 1),
        "minus_program_trace": abs(float(np.trace(rm).real) - 1),
        "plus_marginal_formula": fro(marginal_b(rp, 2*d, d) - expected_b),
        "minus_marginal_formula": fro(marginal_b(rm, 2*d, d) - expected_b),
        "partial_transpose_difference": fro(hp - hm - h_twist/d),
        "controlled_swap_untwisting": fro(c @ h_twist @ c - h),
    }
    bounds = {
        "nu_equals_norm_E_identity": nu,
        "lambda_equals_one_plus_nu_over_two": lam,
        "program_pt_norm_plus": op(hp),
        "program_pt_norm_minus": op(hm),
        "program_pt_bound_lambda_over_d": lam/d,
        "pt_bound_passed": max(op(hp), op(hm)) <= lam/d + TOL,
    }
    moments = []
    collisions = []
    paired = None
    if d <= 3:
        v = collision_hamiltonian(2*d, d)
        v2 = v @ v
        for sign, rho, hrho in [("plus", rp, hp), ("minus", rm, hm)]:
            second = reduced_moment(v2, rho)
            expected_second = np.kron(np.eye(2*d), ((np.eye(d) + e_i)/2).T)
            variance = (second - hrho @ hrho)
            variance = (variance + variance.conj().T)/2
            variance_norm = op(variance)
            row = {
                "program": sign,
                "first_moment_pt_residual": fro(reduced_moment(v, rho) - hrho),
                "second_moment_formula_residual": fro(second - expected_second),
                "second_moment_norm": op(second),
                "expected_second_moment_norm": lam,
                "program_variance_norm": variance_norm,
                "program_variance_minimum_eigenvalue": float(np.linalg.eigvalsh(variance).min()),
            }
            moments.append(row)
            if full_collision:
                for step in [-0.07, 0.02, 0.05]:
                    actual_u = expm(-1j * v * step)
                    q = v/d
                    p = v2/(d*d)
                    exact_u = np.eye(v.shape[0]) + (np.cos(d*step)-1)*p - 1j*np.sin(d*step)*q
                    actual_j = collision_choi(actual_u, rho)
                    ideal_j = unitary_choi(expm(-1j * hrho * step))
                    distance = trace_norm_hermitian(actual_j - ideal_j)
                    collisions.append({
                        "program": sign,
                        "step": step,
                        "matrix_exponential_trigonometric_identity_residual": fro(actual_u - exact_u),
                        "collision_choi_trace_residual": abs(float(np.trace(actual_j).real)-1),
                        "normalized_choi_trace_norm_error": distance,
                        "error_over_step_squared": distance/(step*step),
                        "analytic_diamond_upper_used_only_as_diagnostic_threshold": 2*variance_norm*step*step,
                        "diagnostic_below_analytic_threshold": distance <= 2*variance_norm*step*step + TOL,
                        "scope": "Normalized Choi trace distance is a lower bound on diamond distance, not an upper certificate.",
                    })
        residuals["collision_hermiticity"] = fro(v-v.conj().T)
        residuals["collision_cubic_identity"] = fro(v @ v2 - d*d*v)
        if full_collision:
            step = 0.04
            # Chronological pair: plus at h, then minus at -h. Convert the
            # independently reconstructed Choi states to superoperators.
            jp = collision_choi(expm(-1j*v*step), rp)
            jm = collision_choi(expm(1j*v*step), rm)
            size = rp.shape[0]
            sp = (size*jp).reshape(size, size, size, size).transpose(0, 2, 1, 3).reshape(size*size, size*size)
            sm = (size*jm).reshape(size, size, size, size).transpose(0, 2, 1, 3).reshape(size*size, size*size)
            pair_j = (sm@sp).reshape(size, size, size, size).transpose(0, 2, 1, 3).reshape(size*size, size*size)/size
            pair_target = unitary_choi(expm(-1j*step*(hp-hm)))
            pair_error = trace_norm_hermitian(pair_j-pair_target)
            commutator_norm = op(hp@hm-hm@hp)
            threshold = (2*sum(r["program_variance_norm"] for r in moments)+commutator_norm)*step*step
            paired = {
                "step": step,
                "chronology": "plus(h), then minus(-h)",
                "normalized_choi_trace_norm_error": pair_error,
                "error_over_step_squared": pair_error/(step*step),
                "analytic_diamond_upper_used_only_as_diagnostic_threshold": threshold,
                "diagnostic_below_analytic_threshold": pair_error <= threshold+TOL,
                "scope": "Normalized Choi trace distance is not a diamond upper certificate.",
            }
    # Attaching the known control to the program gives the controlled mean.
    ctrl = np.array([[0, 0], [0, 1]], dtype=complex)
    controlled = np.kron(ctrl, rp)
    controlled_pt = partial_transpose_b(controlled, 4*d, d)
    residuals["known_control_pt_extension"] = fro(controlled_pt-np.kron(ctrl, hp))
    residuals["known_control_marginal_unchanged"] = fro(marginal_b(controlled, 4*d, d)-expected_b)
    if d == 2:
        cv = collision_hamiltonian(4*d, d)
        residuals["known_control_second_moment"] = fro(reduced_moment(cv@cv, controlled)-np.kron(np.eye(4*d), ((np.eye(d)+e_i)/2).T))
    residuals["inverse_target_is_adjoint"] = fro(expm(0.13j*hp)-expm(-0.13j*hp).conj().T)
    passed = (
        all(value < TOL for value in residuals.values())
        and bounds["pt_bound_passed"]
        and all(r["first_moment_pt_residual"] < TOL and r["second_moment_formula_residual"] < TOL and abs(r["second_moment_norm"]-lam) < TOL and r["program_variance_minimum_eigenvalue"] >= -TOL and r["program_variance_norm"] <= lam+TOL for r in moments)
        and all(r["matrix_exponential_trigonometric_identity_residual"] < TOL and r["collision_choi_trace_residual"] < TOL and r["diagnostic_below_analytic_threshold"] for r in collisions)
        and (paired is None or paired["diagnostic_below_analytic_threshold"])
    )
    return {"label": label, "dimension": d, "kraus_count": len(kraus), "passed": bool(passed), "residuals": residuals, "bounds": bounds, "moments": moments, "full_collision_diagnostics": collisions, "paired_collision_diagnostic": paired}


def inversion_case(d, u, rng):
    l = np.kron(u, u.conj())
    z = np.zeros_like(l)
    expected_h = np.block([[z, l], [l.conj().T, z]])
    # Reconstruct the generator through Choi preparation, controlled SWAP and
    # partial transpose, independently of the direct Liouville formula.
    (rp, rm), c = programs(choi_from_kraus([u]), d)
    h = d*c @ (partial_transpose_b(rp, 2*d, d)-partial_transpose_b(rm, 2*d, d)) @ c
    evolved = expm(-0.5j*np.pi*h)
    branch = evolved[d*d:, :d*d]
    dummy = np.zeros((d, 1), dtype=complex)
    dummy[0, 0] = 1
    embedding = np.kron(np.eye(d), dummy)
    isometry = branch @ embedding
    kraus = [isometry.reshape(d, d, d)[:, j, :] for j in range(d)]
    actual_j = choi_from_kraus(kraus)
    intended_j = unitary_choi(u.conj().T)
    wrong_conjugation_j = unitary_choi(u.conj())
    wrong_transpose_j = unitary_choi(u.T)
    psi = rng.normal(size=d) + 1j*rng.normal(size=d)
    psi /= np.linalg.norm(psi)
    expected_vector = -1j*np.kron(u.conj().T@psi, u.T@dummy[:, 0])
    residuals = {
        "unitarity_of_fixture": fro(u.conj().T@u-np.eye(d)),
        "program_derived_generator": fro(h-expected_h),
        "hermitized_square_identity": fro(h@h-np.eye(2*d*d)),
        "pi_over_two_exponential": fro(evolved+1j*h),
        "flag_zero_to_one_branch": fro(branch+1j*l.conj().T),
        "wrong_flag_probability_zero": fro(evolved[:d*d, :d*d]),
        "extracted_vector": float(np.linalg.norm(isometry@psi-expected_vector)),
        "inversion_channel_normalized_choi": fro(actual_j-intended_j),
        "extracted_isometry_return": fro(isometry.conj().T@isometry-np.eye(d)),
    }
    controls = {
        "complex_nonsymmetric_fixture": fro(u-u.T),
        "distance_to_wrong_complex_conjugation_channel": trace_norm_hermitian(actual_j-wrong_conjugation_j),
        "distance_to_wrong_transpose_channel": trace_norm_hermitian(actual_j-wrong_transpose_j),
    }
    passed = all(x<TOL for x in residuals.values()) and min(controls.values())>1e-3
    return {"dimension": d, "passed": bool(passed), "residuals": residuals, "negative_controls": controls}


def depolarizing_correction_case(d, u, probability):
    a = 1-probability
    kraus = [np.sqrt(a)*u]
    for i in range(d):
        for j in range(d):
            k = np.zeros((d, d), dtype=complex)
            k[i, j] = np.sqrt(probability/d)
            kraus.append(k)
    # All signal-dependent information enters through the noisy Choi state.
    (rp, rm), c = programs(choi_from_kraus(kraus), d)
    noisy_h = d*c @ (partial_transpose_b(rp, 2*d, d)-partial_transpose_b(rm, 2*d, d)) @ c
    v = np.kron(u, u.conj())
    zero = np.zeros_like(v)
    clean_h = np.block([[zero, v], [v.conj().T, zero]])
    bell = np.eye(d).ravel()/np.sqrt(d)
    p_bell = np.outer(bell, bell.conj())
    x_flag = np.array([[0, 1], [1, 0]], dtype=complex)
    known_correction_generator = np.kron(x_flag, p_bell)
    time = np.pi/2
    corrected = expm(-1j*(time/a)*noisy_h) @ expm(1j*(time*probability/a)*known_correction_generator)
    clean = expm(-1j*time*clean_h)
    branch = corrected[d*d:, :d*d]
    dummy = np.zeros((d, 1), dtype=complex)
    dummy[0, 0] = 1
    isometry = branch @ np.kron(np.eye(d), dummy)
    extracted_kraus = [isometry.reshape(d, d, d)[:, j, :] for j in range(d)]
    actual_j = choi_from_kraus(extracted_kraus)
    intended_j = unitary_choi(u.conj().T)
    # Reference-entangled input: output order is (system, dummy, reference).
    actual_purification = np.kron(isometry, np.eye(d)) @ bell
    expected_purification = -1j*np.einsum("sr,a->sar", u.conj().T/np.sqrt(d), u.T[:, 0]).ravel()
    residuals = {
        "noisy_channel_trace_preservation": fro(sum(k.conj().T@k for k in kraus)-np.eye(d)),
        "noisy_channel_unitality": fro(sum(k@k.conj().T for k in kraus)-np.eye(d)),
        "choi_derived_generator_decomposition": fro(noisy_h-a*clean_h-probability*known_correction_generator),
        "bell_invariance_left": float(np.linalg.norm(v@bell-bell)),
        "bell_invariance_right": float(np.linalg.norm(v.conj().T@bell-bell)),
        "known_correction_commutator": fro(noisy_h@known_correction_generator-known_correction_generator@noisy_h),
        "corrected_matrix_exponential": fro(corrected-clean),
        "corrected_pi_over_two_identity": fro(corrected+1j*clean_h),
        "wrong_flag_probability_zero": fro(corrected[:d*d, :d*d]),
        "reference_entangled_purification_extraction": float(np.linalg.norm(actual_purification-expected_purification)),
        "corrected_inversion_channel_normalized_choi": fro(actual_j-intended_j),
        "corrected_isometry_return": fro(isometry.conj().T@isometry-np.eye(d)),
    }
    return {
        "dimension": d,
        "known_depolarizing_probability": probability,
        "simulation_time_amplification": 1/a,
        "passed": bool(all(value<TOL for value in residuals.values())),
        "residuals": residuals,
        "scope": "Exact-model finite matrix identity only; no noisy-compiler query lower bound, calibration analysis or precision optimality is tested.",
    }


def positive_square_root(a):
    values, vectors = np.linalg.eigh((a+a.conj().T)/2)
    if float(values.min()) < -TOL:
        raise ValueError("Square-root input is not positive within tolerance")
    return (vectors*np.sqrt(np.maximum(values, 0))) @ vectors.conj().T


def normalized_unitary_choi_distance(u, v):
    """Stable pure-state Choi trace norm, without constructing a large matrix."""
    size = u.shape[0]
    overlap = np.vdot(u, v)/size
    phase = overlap.conjugate()/abs(overlap)
    difference = fro(u-phase*v)/np.sqrt(size)
    return float(difference*np.sqrt(max(0, 4-difference*difference)))


def block_compiler_case(d, kraus, label, rng):
    (rp, rm), c = programs(choi_from_kraus(kraus), d)
    lifted = d*c @ (partial_transpose_b(rp, 2*d, d)-partial_transpose_b(rm, 2*d, d)) @ c
    h0 = lifted/2
    data = h0.shape[0]
    identity = np.eye(data)
    u = expm(-1j*h0)
    cu = block_diag(identity, u)
    pauli_y = np.array([[0, -1j], [1j, 0]])
    sine_unitary = cu @ np.kron(pauli_y, identity) @ cu.conj().T
    plus = np.kron(np.array([[1], [1]])/np.sqrt(2), identity)
    sine = plus.conj().T @ sine_unitary @ plus
    a = lifted/np.pi
    eigs, vectors = np.linalg.eigh(h0)
    analytic_sine = (vectors*np.sin(eigs)) @ vectors.conj().T
    base_residuals = {
        "h0_hermiticity": fro(h0-h0.conj().T),
        "sine_unitary_hermiticity": fro(sine_unitary-sine_unitary.conj().T),
        "sine_unitary_square_identity": fro(sine_unitary@sine_unitary-np.eye(2*data)),
        "compressed_sine_matches_functional_calculus": fro(sine-analytic_sine),
        "inverse_sine_branch_identity": fro((vectors*np.arcsin(np.sin(eigs)))@vectors.conj().T-h0),
    }
    rows = []
    full_grid = np.linspace(-1, 1, 20001)
    half_grid = np.linspace(-0.5, 0.5, 10001)
    for m in (2, 5, 9):
        coefficients = np.zeros(2*m+2)
        for j in range(m+1):
            coefficients[2*j+1] = (2/np.pi)*math.comb(2*j, j)/(4**j*(2*j+1))
        values_full = np.polynomial.polynomial.polyval(full_grid, coefficients)
        values_half = np.polynomial.polynomial.polyval(half_grid, coefficients)
        # Matrix Horner evaluation is separate from scalar/eigenvalue evaluation.
        b = np.zeros_like(a)
        for coefficient in coefficients[::-1]:
            b = b@sine+coefficient*identity
        scalar_b = np.polynomial.polynomial.polyval(np.sin(eigs), coefficients)
        spectral_b = (vectors*scalar_b)@vectors.conj().T
        sa = positive_square_root(identity-a@a)
        sb = positive_square_root(identity-b@b)
        ja = np.block([[a, sa], [sa, -a]])
        jb = np.block([[b, sb], [sb, -b]])
        # Test the completion in arbitrary complement bases, with an unused
        # two-dimensional unitary block as in the existence proof.
        left = block_diag(identity, haar(data+2, rng))
        right = block_diag(identity, haar(data+2, rng))
        unused = haar(2, rng)
        va = left@block_diag(ja, unused)@right
        vb = left@block_diag(jb, unused)@right
        block_error = op(a-b)
        completion_error = op(va-vb)
        completion_bound = 2/np.sqrt(3)*block_error
        choi_error = normalized_unitary_choi_distance(va, vb)
        tail_bound = 4/(3*np.pi)*4**(-(m+1))
        residuals = {
            "matrix_polynomial_matches_spectral_evaluation": fro(b-spectral_b),
            "polynomial_block_hermiticity": fro(b-b.conj().T),
            "a_b_commutator": fro(a@b-b@a),
            "julia_a_unitarity": fro(ja.conj().T@ja-np.eye(2*data)),
            "julia_b_unitarity": fro(jb.conj().T@jb-np.eye(2*data)),
            "completed_a_unitarity": fro(va.conj().T@va-np.eye(2*data+2)),
            "completed_b_unitarity": fro(vb.conj().T@vb-np.eye(2*data+2)),
            "completed_exact_top_a": fro(va[:data, :data]-a),
            "completed_original_top_b": fro(vb[:data, :data]-b),
            "unitary_basis_change_preserves_completion_norm": abs(completion_error-op(ja-jb)),
        }
        inequalities = {
            "coefficient_sum": float(coefficients.sum()),
            "global_grid_max_abs_polynomial": float(np.abs(values_full).max()),
            "half_interval_grid_tail_error": float(np.abs(values_half-(2/np.pi)*np.arcsin(half_grid)).max()),
            "analytic_half_interval_tail_bound": tail_bound,
            "actual_operator_block_error": block_error,
            "a_operator_norm": op(a),
            "b_operator_norm": op(b),
            "strict_contraction_bound_one_over_pi": 1/np.pi,
            "completed_unitary_operator_difference": completion_error,
            "stable_completion_operator_bound": completion_bound,
            "normalized_choi_trace_norm_difference": choi_error,
            "twice_operator_difference_bound": 2*completion_error,
        }
        passed = (
            all(value<TOL for value in residuals.values())
            and coefficients.sum()<=1+TOL
            and np.abs(values_full).max()<=1+TOL
            and inequalities["half_interval_grid_tail_error"]<=tail_bound+TOL
            and block_error<=tail_bound+TOL
            and max(op(a), op(b))<=1/np.pi+TOL
            and completion_error<=completion_bound+TOL
            and choi_error<=2*completion_error+TOL
        )
        rows.append({"m": m, "degree": 2*m+1, "passed": bool(passed), "residuals": residuals, "inequalities": inequalities})
    return {
        "dimension": d,
        "label": label,
        "passed": bool(all(value<TOL for value in base_residuals.values()) and all(r["passed"]for r in rows)),
        "base_residuals": base_residuals,
        "polynomial_and_completion_cases": rows,
        "full_interval_grid_points": len(full_grid),
        "half_interval_grid_points": len(half_grid),
        "scope": "Polynomial and comparison-unitary diagnostics only. No QSVT phase synthesis/circuit execution or diamond-norm upper certification is performed.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    cases = []
    inversions = []
    depolarizing = []
    block_compiler = []
    block_rng = np.random.default_rng(SEED+1)
    for d in (2, 3, 4):
        us = [haar(d, rng) for _ in range(4)]
        weights = rng.random(4)
        weights /= weights.sum()
        mixture = [np.sqrt(w)*u for w, u in zip(weights, us)]
        cases.append(check_case(d, mixture, "complex_random_unital_mixture", full_collision=d<=3))
        inversions.append(inversion_case(d, us[0], rng))
        if d <= 3:
            block_compiler.append(block_compiler_case(d, [us[0]], "complex_unitary_channel", block_rng))
            block_compiler.append(block_compiler_case(d, mixture, "complex_random_unital_mixture", block_rng))
            for probability in (0.2, 0.8):
                depolarizing.append(depolarizing_correction_case(d, us[0], probability))
            reset = []
            for j in range(d):
                k = np.zeros((d, d), dtype=complex)
                k[0, j] = 1
                reset.append(k)
            cases.append(check_case(d, reset, "nonunital_pure_reset_boundary", full_collision=d==2))
    report = {
        "passed": all(c["passed"] for c in cases) and all(c["passed"] for c in inversions) and all(c["passed"] for c in depolarizing) and all(c["passed"] for c in block_compiler),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "numpy": np.__version__, "scipy": scipy.__version__, "seed": SEED, "absolute_residual_tolerance": TOL},
        "channel_cases": cases,
        "unitary_inversion_extraction": inversions,
        "known_depolarizing_correction": depolarizing,
        "block_encoding_polynomial_and_completion": block_compiler,
        "scope": [
            "Finite floating-point diagnostics, not interval arithmetic or a proof certificate.",
            "d=2,3 use explicit collision Hamiltonians; d=4 checks only program, marginal, PT, and extraction identities.",
            "Full collision channels are reconstructed from scipy matrix exponentials and an explicit Kraus/environment trace.",
            "Normalized Choi trace distance is NOT a diamond-norm upper bound; no diamond SDP or general theorem is numerically certified.",
            "Complex nonsymmetric unitary fixtures distinguish adjoint inversion from transpose or complex conjugation.",
            "No hosted rendering or hardware execution is included.",
        ],
    }
    encoded = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded+"\n", encoding="utf-8")
    print(encoded)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
