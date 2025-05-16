import numpy as np
import scipy.signal
import scipy.fftpack as fft
import socket
import joblib
from collections import deque
from scipy.stats import skew, kurtosis
import pywt
import traceback

# ====== Feature Extraction Functions (MATCHING TRAINING EXACTLY) ======
def hjorth_parameters(data):
    """Modified to match training implementation exactly"""
    data = data.astype(np.float64)  # μV conversion added
    first_derivative = np.diff(data, axis=1)
    second_derivative = np.diff(first_derivative, axis=1)
    var_zero = np.var(data, axis=1)
    var_d1 = np.var(first_derivative, axis=1)
    var_d2 = np.var(second_derivative, axis=1)
    mobility = np.sqrt(var_d1 / var_zero)
    complexity = np.sqrt(var_d2 / var_d1) / mobility
    return np.vstack((var_zero/1e4, mobility, complexity)).T  # Additional scaling matches training

def shannon_entropy(signal):
    """Unchanged"""
    pdf = np.histogram(signal, bins=10, density=True)[0]
    pdf = pdf[pdf > 0]
    return -np.sum(pdf * np.log2(pdf))

def spectral_entropy(signal_data, fs):
    """Fixed version that avoids naming conflict"""
    f, Pxx = scipy.signal.welch(signal_data, fs=fs, nperseg=min(fs//4, len(signal_data)))
    Pxx_norm = Pxx / (np.sum(Pxx) + 1e-12)
    return -np.sum(Pxx_norm * np.log2(Pxx_norm + 1e-12))

def higuchi_fd(signal, kmax=10):
    """More robust implementation with error handling"""
    N = len(signal)
    L = np.zeros(kmax)
    
    for k in range(1, kmax+1):
        Lk = np.zeros(k)
        for m in range(k):
            idx = np.arange(m, N, k)
            if len(idx) < 2:  # Handle case where we don't have enough points
                Lk[m] = 0
                continue
                
            diff = np.abs(np.diff(signal[idx]))
            with np.errstate(divide='ignore', invalid='ignore'):
                denominator = len(diff) * k
                Lk[m] = np.sum(diff) * (N-1) / denominator if denominator > 0 else 0
                
        L[k-1] = np.mean(Lk[Lk > 0]) if np.any(Lk > 0) else 0
        
    # Handle case where all L values are zero
    if np.all(L == 0):
        return 0.0
        
    coeffs = np.polyfit(np.log(np.arange(1,kmax+1)), np.log(L + 1e-10), 1)
    return abs(coeffs[0])

def wavelet_features(signal):
    """Matches training exactly"""
    coeffs = pywt.wavedec(signal, 'db4', level=3)
    return np.hstack([np.mean(abs(c)) for c in coeffs])

def phase_locking_value(signal1, signal2):
    """Unchanged"""
    phase_diff = np.angle(scipy.signal.hilbert(signal1)) - np.angle(scipy.signal.hilbert(signal2))
    return np.abs(np.mean(np.exp(1j * phase_diff)))

def zero_crossing_rate(signal):
    """Modified to match training's 2D handling"""
    return np.array([np.sum(np.abs(np.diff(np.sign(ch)))) / (2 * len(ch)) 
                    for ch in signal])[:, np.newaxis]

def root_mean_square(signal):
    """Modified to match training's 2D handling"""
    return np.sqrt(np.mean(signal**2, axis=1))

def peak_frequency(signal, fs):
    """Calculate peak frequency for each channel in a 2D array"""
    peak_freqs = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        peak_freqs.append(f[np.argmax(Pxx)])
    return np.array(peak_freqs)[:, np.newaxis]

def spectral_edge_frequency(signal, fs, edge=0.95):
    """Modified to match training's 2D handling"""
    sefs = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        cumsum = np.cumsum(Pxx)
        sefs.append(f[np.where(cumsum >= edge * cumsum[-1])[0][0]])
    return np.array(sefs)[:, np.newaxis]

def spectral_skewness(signal, fs):
    """Modified to match training's 2D handling"""
    skews = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        skews.append(skew(Pxx))
    return np.array(skews)[:, np.newaxis]

def spectral_kurtosis(signal, fs):
    """Modified to match training's 2D handling"""
    kurtoses = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        kurtoses.append(kurtosis(Pxx))
    return np.array(kurtoses)[:, np.newaxis]

def cross_correlation(signal1, signal2):
    """Unchanged"""
    return np.corrcoef(signal1, signal2)[0, 1]

def fractal_dimension(signal):
    """Matches training"""
    return higuchi_fd(signal, kmax=10)

# ====== Main Processing Class ======
class EEGMovementClassifier:
    def __init__(self, model_path):
        """Load the saved model package"""
        self.model_package = joblib.load(model_path)
        self.model = self.model_package['model']
        self.scaler = self.model_package['scaler']
        self.selected_indices = self.model_package['selected_indices']
        self.optimal_thresholds = self.model_package['optimal_thresholds']
        self.class_labels = self.model_package['class_labels']
        self.feature_labels = self.model_package['feature_labels']
        
        # Reconstruct filter
        self.b_filter = np.array(self.model_package['filters']['b'])
        self.a_filter = np.array(self.model_package['filters']['a'])
        
        # Get expected parameters
        self.fs = 500
        self.num_channels = 8
        self.window_size = 1.0  # seconds
        self.samples_per_window = int(self.fs * self.window_size)
        
        print(f"✅ Model loaded with {len(self.class_labels)} classes")
        print(f"Using {len(self.selected_indices)} selected features")

    def preprocess(self, raw_eeg_data):
        """Match training preprocessing exactly"""
        processed_data = raw_eeg_data.astype(np.float64)
        processed_data = np.clip(processed_data, -22.5, 22.5)
        filtered = scipy.signal.filtfilt(self.b_filter, self.a_filter, processed_data)
        return filtered

    def _calc_bandpower(self, data, band):
        """Matches EXACTLY how bandpower was calculated during training"""
        # 1. Same μV conversion and precision
        data = data.astype(np.float64)
        
        # 2. Same Welch parameters as training
        f, Pxx = scipy.signal.welch(data, 
                            fs=self.fs, 
                            nperseg=min(self.fs//4, data.shape[1]),  # Exactly as in training
                            axis=1)  # Process all channels at once
        
        # 3. Same bandpower calculation logic
        mask = (f >= band[0]) & (f <= band[1])
        band_power = np.sum(Pxx[:, mask], axis=1) / (np.sum(Pxx, axis=1) + 1e-12)
        
        return band_power.reshape(-1, 1)  # Return as column vector to match feature extraction

    def extract_features(self, window_data):
        """EXACTLY matches training feature extraction pipeline"""
        # 1. Preprocessing (must match training)
        processed_data = window_data.astype(np.float64) # Same conversion
        processed_data = np.clip(processed_data, -22.5, 22.5)  # Same clipping
        
        # 2. Filtering (using the saved filter coefficients)
        filtered = scipy.signal.filtfilt(self.b_filter, self.a_filter, processed_data)
        
        # Initialize feature list in EXACT SAME ORDER as training
        features = []
        
        # 3. Time-domain features (identical to training)
        features.append(np.mean(filtered, axis=1, keepdims=True))
        features.append(np.log1p(np.var(filtered, axis=1, keepdims=True)))
        features.append(skew(filtered, axis=1, keepdims=True))
        features.append(kurtosis(filtered, axis=1, keepdims=True))
        features.append(np.median(filtered, axis=1, keepdims=True))
        features.append(np.max(filtered, axis=1, keepdims=True))
        features.append(np.min(filtered, axis=1, keepdims=True))
        features.append(np.log1p(np.sum((filtered)**2, axis=1, keepdims=True)))
        
        # 4. Frequency-domain features (careful with welch!)
        fft_mag = np.abs(fft.rfft(filtered, axis=1))
        features.append(np.log1p(np.mean(fft_mag, axis=1, keepdims=True)))
        features.append(np.log1p(np.var(fft_mag, axis=1, keepdims=True)))
        
        # 5. Bandpower features (critical - must match training exactly)
        features.append(self._calc_bandpower(filtered, [5, 8]).reshape(-1, 1))
        features.append(self._calc_bandpower(filtered, [8, 13]).reshape(-1, 1)) 
        features.append(self._calc_bandpower(filtered, [13, 30]).reshape(-1, 1))
        features.append(self._calc_bandpower(filtered, [30, 60]).reshape(-1, 1))
        
        # 6. Non-linear features
        features.append(hjorth_parameters(filtered))
        features.append(np.apply_along_axis(shannon_entropy, 1, filtered)[:, np.newaxis])
        features.append(np.apply_along_axis(lambda x: spectral_entropy(x, self.fs), 1, filtered)[:, np.newaxis])
        features.append(np.apply_along_axis(fractal_dimension, 1, filtered)[:, np.newaxis])
        features.append(np.vstack([wavelet_features(ch) for ch in filtered]))
        
        # 7. Other features
        features.append(zero_crossing_rate(filtered))
        features.append(root_mean_square(filtered)[:, np.newaxis])
        features.append(peak_frequency(filtered, self.fs))
        features.append(spectral_edge_frequency(filtered, self.fs))
        features.append(spectral_skewness(filtered, self.fs))
        features.append(spectral_kurtosis(filtered, self.fs))
        
        # 8. Connectivity features - MUST MATCH TRAINING
        plv_features = []
        cross_corr_features = []
        
        for i in range(self.num_channels):
            for j in range(i+1, self.num_channels):
                plv_features.append(phase_locking_value(filtered[i], filtered[j]))
                cross_corr_features.append(cross_correlation(filtered[i], filtered[j]))
        
        # Tile connectivity features to match training (8x replication)
        plv_tiled = np.tile(plv_features, (self.num_channels, 1))  # Shape (8, 28)
        cross_corr_tiled = np.tile(cross_corr_features, (self.num_channels, 1))  # Shape (8, 28)
        
        features.append(plv_tiled)
        features.append(cross_corr_tiled)
        
        # Combine all features and verify count
        feature_vector = np.concatenate([f for f in features], axis=1).flatten()
        
        if len(feature_vector) != 688:  # Must match training dimension
            raise ValueError(f"Feature dimension mismatch! Expected 688, got {len(feature_vector)}")
        
        return feature_vector


    def predict(self, raw_eeg_window):
        """Make prediction with dynamic thresholding, returns only class name"""
        # Validate input
        if raw_eeg_window.shape != (self.num_channels, self.samples_per_window):
            raise ValueError(f"Expected shape {(self.num_channels, self.samples_per_window)}, got {raw_eeg_window.shape}")
        
        # Preprocess
        filtered = self.preprocess(raw_eeg_window)
        
        # Extract features
        features = self.extract_features(filtered)
        
        # Scale and select features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        features_selected = features_scaled[:, self.selected_indices]
        
        # Get probabilities
        proba = self.model.predict_proba(features_selected)[0]
        
        # Get thresholds in same order as proba
        thresholds = np.array([self.optimal_thresholds[label] for label in self.class_labels])

        thresholds *= 0.5
        
        # Apply thresholding
        adjusted_probs = np.where(proba > thresholds, proba, 0)

        print("🔍 Probabilities:", dict(zip(self.class_labels, np.round(proba, 3))))
        print("📏 Thresholds:", dict(zip(self.class_labels, np.round(thresholds, 3))))
        print("✅ Adjusted probs:", dict(zip(self.class_labels, np.round(adjusted_probs, 3))))

        # Check if any class meets threshold
        if np.any(adjusted_probs > 0):
            return self.class_labels[np.argmax(adjusted_probs)]
        else:
            # Find which class was closest to meeting its threshold
            return "StopThoughts"

# ====== Main Execution ======
if __name__ == "__main__":
    # Initialize classifier
    classifier = EEGMovementClassifier(r"C:\Users\e203gtec\Desktop\EEG Robot Control Code\eeg_model_20250407_152309-20250410T170236Z-001\eeg_model_20250407_152309\model_package.joblib")
    
    # UDP setup
    UDP_IP = "127.0.0.1"
    UDP_PORT_RECEIVE = 50000
    UDP_PORT_SEND = 60000
    
    WINDOW_SLIDE = 0.5  # seconds

    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_receive.bind((UDP_IP, UDP_PORT_RECEIVE))
    sock_receive.settimeout(1)

    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Buffer for overlapping windows
    buffer = deque(maxlen=classifier.samples_per_window + int(WINDOW_SLIDE * classifier.fs))
    
    print("🎧 Listening for EEG data...")
    while True:
        try:
            # Receive data
            data, _ = sock_receive.recvfrom(classifier.num_channels * 8 * 125)
            if len(data) == 0:
                continue

            # Extract timestamp
            raw_values = np.frombuffer(data, dtype=np.float64)

            # Parse EEG data
            eeg_data = np.frombuffer(data, dtype=np.float64).reshape((classifier.num_channels, -1))
            for sample in eeg_data.T:
                buffer.append(sample)
                
            # Process when we have enough samples
            if len(buffer) >= classifier.samples_per_window:
                window = np.array(buffer)[-classifier.samples_per_window:].T

                prediction = classifier.predict(window)
                print("Predicted class:", prediction)
                sock_send.sendto(prediction.encode(), (UDP_IP, UDP_PORT_SEND))

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            traceback.print_exc()
            continue