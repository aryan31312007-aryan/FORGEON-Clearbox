#!/usr/bin/env python3
"""
FORGEON CLEARBOX v2.0 - World-Class Technical Benchmark & Frame Exporter.
Simulates Multi-Band Wiener DSP processing over time and generates high-resolution 6-Panel benchmark plots.
"""

import os
import time
import numpy as np
import matplotlib
matplotlib.use("Agg") # Non-interactive backend for generating static artifact images
import matplotlib.pyplot as plt

from forgebox_clearbox_demo import ClearBoxDSP

def run_test_and_export():
    dsp = ClearBoxDSP(sample_rate=16000, chunk_size=1024)
    
    # 1. Warmup DSP with 30 simulated frames to build accurate noise floor estimates
    sample_rate = 16000
    chunk_size = 1024
    dt = 1.0 / sample_rate
    
    spectrogram_history = []
    
    for f_idx in range(40):
        t = (f_idx * chunk_size / sample_rate) + np.arange(chunk_size) * dt
        
        # Heavy noise (white noise + 60Hz hum + 1.2kHz industrial whine)
        white_noise = np.random.normal(0, 0.18, chunk_size)
        hum_60hz = 0.14 * np.sin(2 * np.pi * 60 * t)
        whine_1200hz = 0.08 * np.sin(2 * np.pi * 1200 * t)
        
        # Voice envelope (speech active on frames 10 to 35)
        speech_env = 0.6 * (np.sin(2 * np.pi * 0.7 * t) ** 2) if 10 <= f_idx <= 35 else 0.0
        voice_harmonics = speech_env * (np.sin(2 * np.pi * 210 * t) + 0.6 * np.sin(2 * np.pi * 840 * t) + 0.3 * np.sin(2 * np.pi * 2400 * t))
        
        raw_signal = np.clip(voice_harmonics + white_noise + hum_60hz + whine_1200hz, -1.0, 1.0).astype(np.float32)
        
        raw_chunk, raw_db, clean_chunk, clean_db = dsp.process_chunk(raw_signal)
        spectrogram_history.append(clean_db)

    # 2. Setup 6-Panel Dark Benchmark Figure
    plt.style.use('dark_background')
    fig, axes = plt.subplots(3, 2, figsize=(14, 10.5), facecolor="#0B0F17")
    fig.subplots_adjust(hspace=0.42, wspace=0.20, left=0.06, right=0.96, top=0.93, bottom=0.06)
    
    (ax1, ax2), (ax3, ax4), (ax5, ax6) = axes
    
    def format_ax(ax, title, xlabel, ylabel, xlim=None, ylim=None):
        ax.set_facecolor("#161B22")
        ax.set_title(title, fontsize=10, fontweight="bold", color="#E6EDF3", pad=6)
        ax.set_xlabel(xlabel, fontsize=8.5, color="#8B949E", labelpad=2)
        ax.set_ylabel(ylabel, fontsize=8.5, color="#8B949E", labelpad=2)
        if xlim: ax.set_xlim(xlim)
        if ylim: ax.set_ylim(ylim)
        ax.tick_params(colors="#8B949E", labelsize=8)
        ax.grid(True, color="#21262D", linestyle="--", linewidth=0.6, alpha=0.7)
        for spine in ax.spines.values():
            spine.set_color("#30363D")

    time_ms = dsp.time_axis
    freq_hz = dsp.freqs

    # Panel 1: Top-Left: Raw Time Waveform
    format_ax(ax1, "1. BEFORE: Raw Input Waveform (Noisy Speech)", "Time (ms)", "Amplitude (-1 to 1)", (0, 64), (-1.0, 1.0))
    ax1.plot(time_ms, raw_chunk, color="#00F0FF", linewidth=1.1, alpha=0.9)

    # Panel 2: Top-Right: Raw FFT Spectrum & Noise Floor Track
    format_ax(ax2, "2. BEFORE: Frequency Spectrum & MCRA Noise Floor Estimate", "Frequency (Hz)", "Magnitude (dB)", (0, 8000), (-80, 10))
    ax2.plot(freq_hz, raw_db, color="#00D2FF", linewidth=1.1, label="Raw Input FFT")
    ax2.plot(freq_hz, 20.0 * np.log10(dsp.smooth_noise + 1e-6), color="#FF4D4D", linestyle="--", linewidth=1.3, label="Adaptive Noise Floor Track")
    ax2.legend(loc="upper right", fontsize=7.5, facecolor="#161B22", edgecolor="#30363D")

    # Panel 3: Mid-Left: Clean Time Waveform
    format_ax(ax3, "3. AFTER: Cleaned Audio Waveform (Noise Suppressed)", "Time (ms)", "Amplitude (-1 to 1)", (0, 64), (-1.0, 1.0))
    ax3.plot(time_ms, clean_chunk, color="#00FF66", linewidth=1.1, alpha=0.9)

    # Panel 4: Mid-Right: Clean FFT Spectrum & Formant Protection Zone
    format_ax(ax4, "4. AFTER: Clean Spectrum & Voice Formant Protection", "Frequency (Hz)", "Magnitude (dB)", (0, 8000), (-80, 10))
    ax4.plot(freq_hz, clean_db, color="#39FF14", linewidth=1.2, label="Cleaned Spectrum")
    ax4.axvspan(300, 3500, color="#FFB000", alpha=0.12, label="Protected Voice Band (300 - 3500 Hz)")
    ax4.legend(loc="upper right", fontsize=7.5, facecolor="#161B22", edgecolor="#30363D")

    # Panel 5: Bottom-Left: 2D Spectrogram Waterfall Heatmap
    format_ax(ax5, "5. REAL-TIME SPECTROGRAM (Time-Frequency Heatmap)", "Time Frames (0 to 40)", "Frequency (kHz)")
    spec_matrix = np.array(spectrogram_history).T # (513 bins x 40 frames)
    im = ax5.imshow(spec_matrix, aspect='auto', origin='lower', extent=[0, 40, 0, 8], cmap='inferno', vmin=-75, vmax=0)
    cbar = fig.colorbar(im, ax=ax5, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=7, colors="#8B949E")
    cbar.set_label("dBFS", color="#8B949E", fontsize=8)

    # Panel 6: Bottom-Right: Frequency Attenuation Profile & DSP Performance
    format_ax(ax6, "6. DSP PERFORMANCE & FREQUENCY GAIN ATTENUATION (dB)", "Frequency (Hz)", "Gain (dB Attenuation)", (0, 8000), (-40, 10))
    gain_db = clean_db - raw_db
    ax6.plot(freq_hz, gain_db, color="#FFB000", linewidth=1.2, label="Spectral Attenuation Mask")
    ax6.axhline(0, color="#8B949E", linestyle=":", linewidth=0.8)
    
    # Text box overlay on Panel 6 with performance breakdown
    metrics_text = (
        f"★ DSP BENCHMARK SUMMARY ★\n"
        f"• Noise Reduction: {dsp.suppression_level_db:.1f} dB\n"
        f"• SNR Gain: +{dsp.snr_gain_db:.1f} dB\n"
        f"• Processing Time: {dsp.last_proc_time_ms:.3f} ms / block\n"
        f"• Target HW Delay: < 1.5 ms (ESP32-S3 @ 240 MHz)\n"
        f"• VAD Status: {'ACTIVE' if dsp.vad_active else 'SILENCE'}"
    )
    ax6.text(0.04, 0.12, metrics_text, transform=ax6.transAxes, fontsize=8,
             fontfamily="monospace", color="#E6EDF3",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#161B22", edgecolor="#00F0FF", alpha=0.85))
    ax6.legend(loc="upper right", fontsize=7.5, facecolor="#161B22", edgecolor="#30363D")

    fig.suptitle("FORGEON CLEARBOX v2.0 - Technical Jury Demonstration & Benchmark Report", color="#00F0FF", fontsize=13, fontweight="bold", y=0.98)

    output_path = os.path.join(os.path.dirname(__file__), "clearbox_demo_output.png")
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    
    print(f"[CLEARBOX] Benchmark output report successfully generated and saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    run_test_and_export()
