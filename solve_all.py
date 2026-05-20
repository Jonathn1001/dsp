"""
DSP Giua ky - Bien doi Fourier - Giai 7 cau
Ma de: DSP-FOURIER-2026-01
"""
import os
import numpy as np
import scipy.fftpack as sfft
import scipy.signal
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import timeit

matplotlib.rcParams['figure.dpi'] = 100
OUTDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(os.path.dirname(OUTDIR), 'Fourier_apps')

# ============================================================
# CAU 1: DFT vong lap + chuan hoa bien do
# ============================================================
def cau1():
    print("\n=== CAU 1: DFT vong lap ===")
    fs = 1000
    t = np.arange(0, 2, 1/fs)
    N = len(t)
    signal = 3*np.sin(2*np.pi*5*t) + 1.2*np.sin(2*np.pi*9*t + np.pi/4)

    # DFT vong lap
    fourTime = np.arange(N) / N
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        csw = np.exp(-1j * 2*np.pi * k * fourTime)
        X[k] = np.sum(signal * csw)

    ampl = np.abs(X) / N
    ampl[1:N//2] *= 2
    hz = np.linspace(0, fs/2, N//2 + 1)

    fig, ax = plt.subplots(2, 1, figsize=(11, 6))
    ax[0].plot(t, signal)
    ax[0].set_xlabel('Thoi gian (s)'); ax[0].set_ylabel('Bien do')
    ax[0].set_title('Tin hieu thoi gian x(t)=3sin(2π·5t)+1.2sin(2π·9t+π/4)')
    ax[0].set_xlim([0, 1]); ax[0].grid(alpha=0.3)

    ax[1].stem(hz, ampl[:len(hz)], basefmt=' ')
    ax[1].set_xlim([0, 15])
    ax[1].set_xlabel('Tan so (Hz)'); ax[1].set_ylabel('Bien do')
    ax[1].set_title('Pho bien do — ky vong dinh 5 Hz=3.0 va 9 Hz=1.2')
    ax[1].grid(alpha=0.3)
    for f_peak in [5.0, 9.0]:
        idx = np.argmin(np.abs(hz - f_peak))
        ax[1].annotate(f'{ampl[idx]:.3f}', (hz[idx], ampl[idx]),
                       xytext=(hz[idx]+0.3, ampl[idx]+0.1), color='red', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau1_pho.png'), dpi=150, bbox_inches='tight')
    plt.close()
    idx5 = np.argmin(np.abs(hz - 5))
    idx9 = np.argmin(np.abs(hz - 9))
    print(f"Bien do tai 5Hz = {ampl[idx5]:.4f} (KV 3.0)")
    print(f"Bien do tai 9Hz = {ampl[idx9]:.4f} (KV 1.2)")
    return ampl[idx5], ampl[idx9]


# ============================================================
# CAU 2: So sanh DFT vs FFT
# ============================================================
def dft_loop(x):
    N = len(x)
    fourTime = np.arange(N) / N
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        X[k] = np.sum(x * np.exp(-1j*2*np.pi*k*fourTime))
    return X


def cau2():
    print("\n=== CAU 2: So sanh DFT vs FFT ===")
    Ns = [500, 1000, 2000, 4000, 8000]
    times_dft, times_fft = [], []
    np.random.seed(2026)
    for N in Ns:
        signal = np.random.randn(N)
        tic = timeit.default_timer()
        X_dft = dft_loop(signal)
        times_dft.append(timeit.default_timer() - tic)
        tic = timeit.default_timer()
        X_fft = sfft.fft(signal)
        times_fft.append(timeit.default_timer() - tic)
        err = np.max(np.abs(X_dft - X_fft))
        print(f'N={N}: DFT={times_dft[-1]*1000:.1f}ms, FFT={times_fft[-1]*1000:.3f}ms, err={err:.2e}')

    alpha_dft = np.polyfit(np.log(Ns), np.log(times_dft), 1)[0]
    alpha_fft = np.polyfit(np.log(Ns), np.log(np.maximum(times_fft, 1e-9)), 1)[0]
    print(f'Do phuc tap DFT: O(N^{alpha_dft:.2f}) — ly thuyet O(N^2)')
    print(f'Do phuc tap FFT: O(N^{alpha_fft:.2f}) — ly thuyet O(N logN)')

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    ax[0].loglog(Ns, times_dft, 'b-o', label=f'DFT vong lap ~ N^{alpha_dft:.2f}')
    ax[0].loglog(Ns, times_fft, 'r-s', label=f'FFT scipy ~ N^{alpha_fft:.2f}')
    ax[0].set_xlabel('N (so mau)'); ax[0].set_ylabel('Thoi gian (s)')
    ax[0].set_title('Do phuc tap thuc nghiem (log-log)')
    ax[0].legend(); ax[0].grid(True, which='both', alpha=0.3)

    ax[1].bar(['DFT vong lap', 'FFT scipy'],
              [times_dft[2]*1000, max(times_fft[2]*1000, 0.001)],
              color=['gray', 'steelblue'])
    ax[1].set_ylabel('Thoi gian (ms)'); ax[1].set_yscale('log')
    ax[1].set_title(f'So sanh tai N={Ns[2]}')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau2_tocdo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return alpha_dft, alpha_fft


# ============================================================
# CAU 3: Nyquist & aliasing
# ============================================================
def cau3():
    print("\n=== CAU 3: Nyquist & aliasing ===")
    f_analog = 5000
    t = np.arange(0, 1, 1/f_analog)
    f_signal = 35
    d = np.sin(2*np.pi*f_signal*t)
    fs_list = [40, 60, 100, 500]

    fig, axes = plt.subplots(len(fs_list), 2, figsize=(13, 10))
    for i, fs in enumerate(fs_list):
        step = int(round(f_analog / fs))
        d_sub = d[::step]
        t_sub = t[::step]
        N_sub = len(d_sub)
        f_alias_candidates = [abs(f_signal - k*fs) for k in range(-3, 4)]
        f_alias = min([f for f in f_alias_candidates if f <= fs/2])

        axes[i, 0].plot(t, d, 'k-', alpha=0.3, label='Analog 35 Hz')
        axes[i, 0].plot(t_sub, d_sub, 'ro-', markersize=4, label=f'fs={fs} Hz')
        axes[i, 0].set_xlim([0, 0.3]); axes[i, 0].set_ylabel('Bien do')
        nyq = fs / 2
        status = 'DU (khong alias)' if nyq > f_signal else f'THIEU, alias={f_alias:.1f} Hz'
        axes[i, 0].set_title(f'fs={fs} Hz, Nyquist={nyq:.1f} Hz — {status}')
        axes[i, 0].legend(loc='upper right', fontsize=8); axes[i, 0].grid(alpha=0.3)
        print(f"fs={fs} Hz: Nyquist={nyq} Hz, {status}")

        X = np.abs(sfft.fft(d_sub)) / N_sub
        hz = np.linspace(0, fs/2, N_sub//2 + 1)
        axes[i, 1].stem(hz, 2*X[:len(hz)], basefmt=' ')
        axes[i, 1].set_xlabel('Tan so (Hz)'); axes[i, 1].set_ylabel('|X|')
        axes[i, 1].set_xlim([0, fs/2]); axes[i, 1].set_title(f'Pho FFT, fs={fs} Hz')
        axes[i, 1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau3_aliasing.png'), dpi=150, bbox_inches='tight')
    plt.close()


# ============================================================
# CAU 4: Loc Gauss bandpass
# ============================================================
def cau4():
    print("\n=== CAU 4: Loc Gauss bandpass 14 Hz ===")
    fs = 500; T = 4
    t = np.arange(0, T, 1/fs); N = len(t)
    np.random.seed(2026)
    signal_clean = np.sin(2*np.pi*14*t)
    signal = (np.sin(2*np.pi*6*t)
              + 0.8*np.sin(2*np.pi*14*t)
              + 1.2*np.sin(2*np.pi*40*t)
              + 0.5*np.random.randn(N))

    def snr(s, ref):
        return 10*np.log10(np.var(ref) / np.var(s - ref))

    snr_truoc = snr(signal, 0.8*signal_clean)
    X = sfft.fft(signal) / N
    hz_full = np.linspace(0, fs, N)
    f0 = 14; sigma = 2
    H = (np.exp(-((hz_full - f0)/sigma)**2)
         + np.exp(-((hz_full - (fs - f0))/sigma)**2))
    Y = X * H
    y = 2 * np.real(sfft.ifft(Y)) * N / 2  # rescale (X da chia N o tren)
    # Reconstruct properly: nhan lai N de tra bien do
    y = np.real(sfft.ifft(sfft.fft(signal) * H))

    snr_sau = snr(y, 0.8*signal_clean)
    print(f'SNR truoc loc: {snr_truoc:.2f} dB')
    print(f'SNR sau loc:   {snr_sau:.2f} dB')
    print(f'Cai thien SNR: {snr_sau - snr_truoc:.2f} dB')

    hz_half = np.linspace(0, fs/2, N//2 + 1)
    fig, ax = plt.subplots(3, 1, figsize=(11, 9))
    ax[0].plot(t, signal, label='Goc (nhieu)', alpha=0.7)
    ax[0].plot(t, y, 'r', label='Sau loc', linewidth=1.5)
    ax[0].plot(t, 0.8*signal_clean, 'g--', label='14 Hz ly tuong', alpha=0.7)
    ax[0].set_xlim([0, 1]); ax[0].set_xlabel('Thoi gian (s)')
    ax[0].set_title(f'Mien thoi gian — SNR: {snr_truoc:.1f}→{snr_sau:.1f} dB')
    ax[0].legend(); ax[0].grid(alpha=0.3)

    ax[1].plot(hz_half, 2*np.abs(X[:len(hz_half)]))
    ax[1].set_xlim([0, 60]); ax[1].set_xlabel('Tan so (Hz)')
    ax[1].set_title('Pho tin hieu goc'); ax[1].grid(alpha=0.3)

    Y_disp = sfft.fft(signal) * H / N
    ax[2].plot(hz_half, 2*np.abs(Y_disp[:len(hz_half)]), 'r', label='Pho sau loc')
    ax[2].plot(hz_half, H[:len(hz_half)] * np.max(2*np.abs(X[:len(hz_half)])),
               'g--', label='Bo loc Gauss')
    ax[2].set_xlim([0, 60]); ax[2].set_xlabel('Tan so (Hz)')
    ax[2].set_title('Pho sau loc va duong cong bo loc'); ax[2].legend(); ax[2].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau4_loc.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return snr_truoc, snr_sau


# ============================================================
# CAU 5: STFT
# ============================================================
def cau5():
    print("\n=== CAU 5: STFT chirp ===")
    fs = 1000; T = 6
    t = np.arange(0, T, 1/fs); N = len(t)
    f_chirp = np.linspace(5, 50, N)
    # Phase phai tich phan; cho chirp tuyen tinh: phi(t)=2*pi*(f0*t + (f1-f0)/(2T) * t^2)
    f0_ch, f1_ch = 5, 50
    phase = 2*np.pi*(f0_ch*t + (f1_ch - f0_ch)/(2*T) * t**2)
    signal = np.sin(phase)
    inst_freq = f0_ch + (f1_ch - f0_ch)/T * t

    def stft_loop(x, L, hop):
        win = 0.5*(1 - np.cos(2*np.pi*np.arange(L)/(L-1)))
        M = (len(x) - L) // hop + 1
        STFT = np.zeros((L, M), dtype=complex)
        for m in range(M):
            seg = x[m*hop : m*hop + L]
            STFT[:, m] = sfft.fft(win * seg) / L
        return STFT

    # Theo de: L=256, hop=32. Giu Δ=32 cho ca 3 truong hop de so sanh cong bang.
    fig, axes = plt.subplots(3, 1, figsize=(11, 11))
    L_list = [64, 256, 1024]
    hop_list = [32, 32, 32]
    for i, (L, hop) in enumerate(zip(L_list, hop_list)):
        STFT = stft_loop(signal, L, hop)
        hz = np.linspace(0, fs/2, L//2 + 1)
        t_axis = (np.arange(STFT.shape[1])*hop + L/2) / fs
        spectro = 2 * np.abs(STFT[:L//2+1, :])
        pcm = axes[i].pcolormesh(t_axis, hz, spectro, shading='auto', cmap='viridis')
        axes[i].plot(t, inst_freq, 'white', linestyle='--', linewidth=1, alpha=0.7,
                     label='Tan so that')
        axes[i].set_ylim([0, 60])
        axes[i].set_xlabel('Thoi gian (s)'); axes[i].set_ylabel('Tan so (Hz)')
        axes[i].set_title(f'STFT L={L}, hop={hop}  Δt={L/fs*1000:.0f} ms, Δf={fs/L:.1f} Hz')
        axes[i].legend(loc='upper left')
        plt.colorbar(pcm, ax=axes[i])
        print(f"L={L}: Δt={L/fs*1000:.0f}ms, Δf={fs/L:.2f}Hz")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau5_stft.png'), dpi=150, bbox_inches='tight')
    plt.close()


# ============================================================
# CAU 6: EEG phổ
# ============================================================
def cau6():
    print("\n=== CAU 6: EEG phổ ===")
    PATH = os.path.join(DATADIR, 'EEGrestingState.mat')
    m = sio.loadmat(PATH)
    eeg = m['eegdata'].flatten().astype(float)
    fs = int(m['srate'][0, 0])
    N = len(eeg)
    t = np.arange(N) / fs
    print(f'So mau: {N}, fs={fs} Hz, thoi luong={N/fs:.1f} s')

    X = sfft.fft(eeg) / N
    hz = np.linspace(0, fs/2, N//2 + 1)
    ampl = 2 * np.abs(X[:len(hz)])
    ampl[0] /= 2

    f_w, Pxx_w = scipy.signal.welch(eeg, fs, nperseg=fs, noverlap=fs//2)

    bands = {
        'Delta': (0.5, 4, '#9ecae1'),
        'Theta': (4, 8, '#a1d99b'),
        'Alpha': (8, 13, '#fdd0a2'),
        'Beta':  (13, 30, '#fdae6b'),
        'Gamma': (30, 70, '#fc9272'),
    }
    print('Nang luong tuong doi cac bang tan:')
    total = np.sum(ampl**2)
    band_energy = {}
    for name, (lo, hi, _) in bands.items():
        mask = (hz >= lo) & (hz < hi)
        E = np.sum(ampl[mask]**2)
        band_energy[name] = 100*E/total
        print(f'  {name:6s} ({lo:5.1f}-{hi:5.1f} Hz): {100*E/total:5.2f}%')
    max_band = max(band_energy, key=band_energy.get)
    print(f'Bang tan nang luong lon nhat: {max_band} ({band_energy[max_band]:.2f}%)')

    fig, axes = plt.subplots(3, 1, figsize=(11, 10))
    axes[0].plot(t[:10*fs], eeg[:10*fs])
    axes[0].set_xlabel('Thoi gian (s)'); axes[0].set_ylabel('Bien do (uV)')
    axes[0].set_title('(a) EEG nghi — 10 giay dau'); axes[0].grid(alpha=0.3)

    for name, (lo, hi, c) in bands.items():
        axes[1].axvspan(lo, hi, alpha=0.3, color=c, label=name)
    axes[1].plot(hz, ampl, 'k', linewidth=1)
    axes[1].set_xlim([0, 70]); axes[1].set_xlabel('Tan so (Hz)')
    axes[1].set_ylabel('Bien do'); axes[1].set_title('(b) Pho FFT toan cuc')
    axes[1].legend(ncol=5, fontsize=9); axes[1].grid(alpha=0.3)

    for name, (lo, hi, c) in bands.items():
        axes[2].axvspan(lo, hi, alpha=0.3, color=c)
    axes[2].semilogy(f_w, Pxx_w)
    axes[2].set_xlim([0, 70]); axes[2].set_xlabel('Tan so (Hz)')
    axes[2].set_ylabel('PSD (Welch, log)')
    axes[2].set_title('(c) Pho Welch — on dinh hon FFT don')
    axes[2].grid(alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau6_eeg.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return band_energy, max_band


# ============================================================
# CAU 7: Loc anh Gauss 2D
# ============================================================
def cau7():
    print("\n=== CAU 7: Loc anh Gauss 2D ===")
    from scipy import stats
    PATH = os.path.join(DATADIR, 'Lenna.png')
    # Doc anh, chuyen grayscale bang trung binh 3 kenh (theo yeu cau de)
    img_rgb = np.array(Image.open(PATH).convert('RGB'), dtype=float)
    img = img_rgb.mean(axis=2)
    print(f'Anh shape: {img.shape}')

    F = sfft.fftshift(sfft.fft2(img))
    log_mag = np.log(np.abs(F) + 1)
    phase = np.angle(F)

    # Panel 1: anh goc + log|FFT2| + pha
    fig1, ax1 = plt.subplots(1, 3, figsize=(15, 5))
    ax1[0].imshow(img, cmap='gray'); ax1[0].set_title('Anh goc (grayscale, mean 3 kenh)'); ax1[0].axis('off')
    ax1[1].imshow(log_mag, cmap='gray'); ax1[1].set_title('log|FFT2| (DC o tam)'); ax1[1].axis('off')
    ax1[2].imshow(phase, cmap='hsv'); ax1[2].set_title('Pha FFT2'); ax1[2].axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau7_pho_anh.png'), dpi=150, bbox_inches='tight')
    plt.close()

    xr = stats.zscore(np.arange(img.shape[1]))
    yr = stats.zscore(np.arange(img.shape[0]))
    X, Y = np.meshgrid(xr, yr)

    # Panel 2: bang 3x2 (low-pass + high-pass) cho 3 sigma — dung yeu cau de
    sigmas = [0.05, 0.10, 0.20]
    fig, axes = plt.subplots(len(sigmas), 2, figsize=(10, 4*len(sigmas)))
    rmse_list = []
    info_list = []
    total_energy = np.sum(np.abs(F)**2)
    for i, sigma in enumerate(sigmas):
        G = np.exp(-(X**2 + Y**2) / (2*sigma**2))
        F_lp = F * G
        img_lp = np.real(sfft.ifft2(sfft.ifftshift(F_lp)))
        F_hp = F * (1 - G)
        img_hp = np.real(sfft.ifft2(sfft.ifftshift(F_hp)))
        rmse_lp = np.sqrt(np.mean((img - img_lp)**2))
        # % nang luong giu lai
        retain = np.sum(np.abs(F_lp)**2) / total_energy * 100
        rmse_list.append(rmse_lp)
        info_list.append((sigma, rmse_lp, retain))
        print(f'σ={sigma}: RMSE(low-pass) = {rmse_lp:.3f}, giu lai {retain:.2f}% nang luong')

        axes[i, 0].imshow(img_lp, cmap='gray')
        axes[i, 0].set_title(f'Low-pass σ={sigma}  RMSE={rmse_lp:.2f}, giu {retain:.1f}% E')
        axes[i, 1].imshow(img_hp, cmap='gray')
        axes[i, 1].set_title(f'High-pass σ={sigma}')
        for a in axes[i]:
            a.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'cau7_loc_anh.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return info_list


if __name__ == '__main__':
    cau1()
    cau2()
    cau3()
    cau4()
    cau5()
    cau6()
    cau7()
    print("\n=== HOAN TAT — Tat ca PNG da luu trong", OUTDIR)
