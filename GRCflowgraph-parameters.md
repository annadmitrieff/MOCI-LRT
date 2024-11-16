# GMSK Modulator Parameters
gmsk_mod = digital.gmsk_mod(
    samples_per_symbol=30000,
    bt=0.35,
    pulse_length=4,
    sampling_freq=2.88e6,
    bits_per_second=9600
)

# GMSK Demodulator Parameters
gmsk_demod = digital.gmsk_demod(
    samples_per_symbol=30000,
    gain_mu=0.175,
    mu=0.5,
    omega_relative_limit=0.005,
    freq_error=0.0,
    sampling_freq=2.88e6,
    bits_per_second=9600
)

# Throttle Block Parameters
throttle = blocks.throttle(
    type=gr.sizeof_gr_complex,
    samples_per_second=2.88e6
)

# Rational Resampler Parameters
resampler = filter.rational_resampler_ccc(
    interpolation=2880000,
    decimation=9600,
    taps=None,
    fractional_bw=0.4
)

# Low Pass Filter Parameters
lowpass = filter.fir_filter_ccf(
    1,
    firdes.low_pass(
        1,
        2.88e6,
        9600,
        1000,
        firdes.WIN_HAMMING,
        6.76
    )
)