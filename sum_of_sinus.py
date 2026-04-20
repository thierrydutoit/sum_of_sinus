import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sinusoid and Phasor Sum", layout="centered")

st.title("Summing Sinusoids with same f0")
st.markdown(
    """
What is the sum of two sinusoids $x_1(t) = A_1 \sin(\omega t + \phi_1)$ and $x_2(t) = A_2 \sin(\omega t + \phi_2)$ with **identical frequency** but different amplitudes and phases?

Try by yourself
"""
)

# Fixed frequency
f = 1.0  # Hz
omega = 2 * np.pi * f

slider_col1, slider_col2, slider_col3, slider_col4 = st.columns(4)
with slider_col1:
    A1 = st.slider("Amplitude A1", 0.0, 5.0, 5.0, 0.1)
with slider_col2:
    phi1_deg = st.slider("Phase φ1 (degrees)", -180.0, 180.0, 0.0, 1.0)
with slider_col3:
    A2 = st.slider("Amplitude A2", 0.0, 5.0, 5.0, 0.1)
with slider_col4:
    phi2_deg = st.slider("Phase φ2 (degrees)", -180.0, 180.0, 90.0, 1.0)

phi1 = np.deg2rad(phi1_deg)
phi2 = np.deg2rad(phi2_deg)

# Time-domain signals
t = np.linspace(0, 2 / f, 1000)
x1 = A1 * np.sin(omega * t + phi1)
x2 = A2 * np.sin(omega * t + phi2)
x_sum = x1 + x2

# Phasors
P1 = A1 * np.exp(1j * phi1)
P2 = A2 * np.exp(1j * phi2)
P_sum = P1 + P2

A_sum = np.abs(P_sum)
phi_sum = np.angle(P_sum)
phi_sum_deg = np.rad2deg(phi_sum)

x_sum_from_phasor = A_sum * np.sin(omega * t + phi_sum)

plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    fig_time, ax_time = plt.subplots(figsize=(5, 5))
    ax_time.plot(t, x1, label=fr"$x_1(t)={A1:.2f}\sin(\omega t + {phi1_deg:.1f}^\circ)$")
    ax_time.plot(t, x2, label=fr"$x_2(t)={A2:.2f}\sin(\omega t + {phi2_deg:.1f}^\circ)$")
    ax_time.plot(t, x_sum, linewidth=2.5, label=r"$x_1(t)+x_2(t)$")
    ax_time.set_xlabel("Time (s)")
    ax_time.set_ylabel("Amplitude")
    ax_time.set_ylim(-11, 11)
    ax_time.set_title("Two sinusoids with identical frequency and their sum")
    ax_time.grid(True, alpha=0.3)
    ax_time.legend(loc="upper right")
    st.pyplot(fig_time)

with plot_col2:
    fig_phasor, ax_phasor = plt.subplots(figsize=(10, 5))

    vals_x = [0, P1.real, P2.real, P_sum.real]
    vals_y = [0, P1.imag, P2.imag, P_sum.imag]
    max_extent = max(1.0, np.max(np.abs(vals_x + vals_y))) * 1.25

    ax_phasor.axhline(0, color="black", linewidth=1)
    ax_phasor.axvline(0, color="black", linewidth=1)

    ax_phasor.arrow(0, 0, P1.real, P1.imag, head_width=0.08 * max_extent, length_includes_head=True)
    ax_phasor.arrow(0, 0, P2.real, P2.imag, head_width=0.08 * max_extent, length_includes_head=True)
    ax_phasor.arrow(0, 0, P_sum.real, P_sum.imag, head_width=0.08 * max_extent, length_includes_head=True)

    ax_phasor.plot([P1.real, P_sum.real], [P1.imag, P_sum.imag], "--", alpha=0.6)
    ax_phasor.plot([P2.real, P_sum.real], [P2.imag, P_sum.imag], "--", alpha=0.6)

    ax_phasor.text(P1.real, P1.imag, "  P1", fontsize=11)
    ax_phasor.text(P2.real, P2.imag, "  P2", fontsize=11)
    ax_phasor.text(
        P_sum.real,
        P_sum.imag,
        f"  P1 + P2\n  A = {A_sum:.1f}\n  φ = {phi_sum_deg:.0f}°",
        fontsize=11,
        weight="bold",
    )
    ax_phasor.set_xlim(-11, 11)
    ax_phasor.set_ylim(-11, 11)
    ax_phasor.set_aspect("equal", adjustable="box")
    ax_phasor.set_xlabel("Real")
    ax_phasor.set_ylabel("Imaginary")
    ax_phasor.set_title("Phasor addition")
    ax_phasor.grid(True, alpha=0.3)
    st.pyplot(fig_phasor)

with st.expander("Open for comments"):
    st.markdown(
        rf"""
Because the two sinusoids have the **same frequency**, their sum is also a sinusoid at that frequency:

$$x_1(t)+x_2(t) = A_\Sigma \sin(\omega t + \phi_\Sigma)$$

where:

- $A_\Sigma = |P_1 + P_2| = {A_sum:.3f}$
- $\phi_\Sigma = \angle(P_1 + P_2) = {phi_sum_deg:.3f}^\circ$

This can be easily obtained by phasor sum.

If each sinusoid is represented by a phasor:

- $P_1 = A_1 e^{{j\phi_1}} = {A1:.2f} e^{{j {phi1_deg:.1f}^\circ}}$
- $P_2 = A_2 e^{{j\phi_2}} = {A2:.2f} e^{{j {phi2_deg:.1f}^\circ}}$

their vector sum is:

$$P_\Sigma = P_1 + P_2$$

The **magnitude** of $P_\Sigma$ is the amplitude of the summed sinusoid, and the **angle** of $P_\Sigma$ is its phase:

$$A_\Sigma = |P_\Sigma|, \qquad \phi_\Sigma = \angle P_\Sigma$$

This is why phasor addition is a convenient way to add same-frequency sinusoids.

"""
    )
    st.caption("[See other iDSP apps](https://thierrydutoit.github.io/iDSP/)")

