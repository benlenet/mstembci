import os
import numpy as np
import scipy.io
import scipy.signal
import joblib
import json
import itertools
from datetime import datetime
from scipy.stats import skew, kurtosis
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight
from skopt import BayesSearchCV, gp_minimize
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_curve
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pywt
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# --- Feature Extraction Functions ---
def hjorth_parameters(data):
    data = data.astype(np.float64)
    first_derivative = np.diff(data, axis=1)
    second_derivative = np.diff(first_derivative, axis=1)
    var_zero = np.var(data, axis=1)
    var_d1 = np.var(first_derivative, axis=1)
    var_d2 = np.var(second_derivative, axis=1)
    mobility = np.sqrt(var_d1 / var_zero)
    complexity = np.sqrt(var_d2 / var_d1) / mobility
    return np.vstack((var_zero/1e4, mobility, complexity)).T

def shannon_entropy(signal):
    pdf = np.histogram(signal, bins=10, density=True)[0]
    pdf = pdf[pdf > 0]
    return -np.sum(pdf * np.log2(pdf))

def spectral_entropy(signal, fs):
    f, Pxx = scipy.signal.welch(signal, fs=fs, nperseg=fs//4)
    Pxx_norm = Pxx / np.sum(Pxx)
    return -np.sum(Pxx_norm * np.log2(Pxx_norm))

def higuchi_fd(signal, kmax=10):
    L = np.zeros((kmax,))
    x = np.asarray(signal)
    N = x.size
    for k in range(1, kmax + 1):
        Lk = np.zeros((k,))
        for m in range(k):
            Lmk = 0
            count = 0
            for i in range(1, (N - m) // k):
                Lmk += abs(x[m + i * k] - x[m + (i - 1) * k])
                count += 1
            Lmk /= count
            norm_factor = (N - 1) / (k * count)
            Lk[m] = Lmk * norm_factor
        L[k - 1] = np.mean(Lk)
    k_vals = np.log(np.arange(1, kmax + 1))
    L_vals = np.log(L + 1e-10)
    coeffs = np.polyfit(k_vals, L_vals, 1)
    return abs(coeffs[0])

def fractal_dimension(signal):
    return higuchi_fd(signal, kmax=10)

def wavelet_features(signal):
    coeffs = pywt.wavedec(signal, 'db4', level=3)
    return np.hstack([np.mean(np.abs(c)) for c in coeffs])

def phase_locking_value(signal1, signal2):
    phase_diff = np.angle(scipy.signal.hilbert(signal1)) - np.angle(scipy.signal.hilbert(signal2))
    return np.abs(np.mean(np.exp(1j * phase_diff)))

def zero_crossing_rate(signal):
    return np.array([np.sum(np.abs(np.diff(np.sign(ch)))) / (2 * len(ch)) for ch in signal])[:, np.newaxis]

def root_mean_square(signal):
    return np.sqrt(np.mean(signal**2, axis=1))

def peak_frequency(signal, fs):
    peak_freqs = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        peak_freqs.append(f[np.argmax(Pxx)])
    return np.array(peak_freqs)[:, np.newaxis]

def spectral_edge_frequency(signal, fs, edge=0.95):
    sefs = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        cumsum = np.cumsum(Pxx)
        sefs.append(f[np.where(cumsum >= edge * cumsum[-1])[0][0]])
    return np.array(sefs)[:, np.newaxis]

def spectral_skewness(signal, fs):
    skews = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        skews.append(skew(Pxx))
    return np.array(skews)[:, np.newaxis]

def spectral_kurtosis(signal, fs):
    kurtoses = []
    for ch in signal:
        f, Pxx = scipy.signal.welch(ch, fs=fs, nperseg=min(fs//4, len(ch)))
        kurtoses.append(kurtosis(Pxx))
    return np.array(kurtoses)[:, np.newaxis]

def cross_correlation(signal1, signal2):
    return np.corrcoef(signal1, signal2)[0, 1]

def bandpower(data, fs, band):
    data = data.astype(np.float64)
    f, Pxx = scipy.signal.welch(data, fs=fs, nperseg=min(fs//4, data.shape[1]))
    return np.sum(Pxx[:, (f >= band[0]) & (f <= band[1])], axis=1) / (np.sum(Pxx, axis=1) + 1e-12)

# --- Data Loading and Feature Extraction ---
def load_data(base_dir, fs, window_size=1.0, step_size=1.0, files_per_class=0, trim_seconds=5):
    X, y = [], []
    class_labels = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    b, a = scipy.signal.butter(4, [5, 60], btype='bandpass', fs=fs)
    printout_count = 0
    window_samples = int(window_size * fs)
    step_samples = int(step_size * fs)
    
    for class_idx, class_label in enumerate(class_labels):
        class_files = [f for f in os.listdir(os.path.join(base_dir, class_label)) if f.endswith('.mat')]
        if files_per_class > 0:
            class_files = class_files[:files_per_class]
        for file in class_files:
            mat_data = scipy.io.loadmat(os.path.join(base_dir, class_label, file))
            # Assume first row is time vector; rows 1-8 are EEG channels
            raw_data = mat_data[list(mat_data.keys())[-1]][1:,:].astype(np.float64)
            trim_samples = int(trim_seconds * fs)
            if trim_samples > 0 and raw_data.shape[1] > trim_samples:
                raw_data = raw_data[:, trim_samples:]
            full_data = raw_data[:, :]
            full_data = np.clip(full_data, -22.50, 22.50)
            filtered = scipy.signal.filtfilt(b, a, full_data, axis=1)
            num_windows = (filtered.shape[1] - window_samples) // step_samples + 1
            for i in range(num_windows):
                start = i * step_samples
                end = start + window_samples
                window_data = filtered[:, start:end]
                # Extract features (including wavelet features via np.vstack)
                hjorth_feats = hjorth_parameters(window_data)
                shannon_feats = np.apply_along_axis(shannon_entropy, 1, window_data)[:, np.newaxis]
                spectral_feats = np.apply_along_axis(spectral_entropy, 1, window_data, fs)[:, np.newaxis]
                wavelet_feats = np.vstack([wavelet_features(ch) for ch in window_data])
                fractal_feats = np.apply_along_axis(fractal_dimension, 1, window_data)[:, np.newaxis]
                zcr_feats = zero_crossing_rate(window_data)
                rms_feats = root_mean_square(window_data)[:, np.newaxis]
                peak_freq_feats = peak_frequency(window_data, fs)
                sef_feats = spectral_edge_frequency(window_data, fs)
                spectral_skew_feats = spectral_skewness(window_data, fs)
                spectral_kurt_feats = spectral_kurtosis(window_data, fs)
                features = np.hstack([
                    np.mean(window_data, axis=1, keepdims=True),
                    np.log1p(np.var(window_data, axis=1, keepdims=True)),
                    skew(window_data, axis=1, keepdims=True),
                    kurtosis(window_data, axis=1, keepdims=True),
                    np.median(window_data, axis=1, keepdims=True),
                    np.max(window_data, axis=1, keepdims=True),
                    np.min(window_data, axis=1, keepdims=True),
                    np.log1p(np.sum((window_data)**2, axis=1, keepdims=True)),
                    np.log1p(np.mean(np.abs(np.fft.rfft(window_data, axis=1)), axis=1, keepdims=True)),
                    np.log1p(np.var(np.abs(np.fft.rfft(window_data, axis=1)), axis=1, keepdims=True)),
                    bandpower(window_data, fs, [5,8]).reshape(-1,1),
                    bandpower(window_data, fs, [8,13]).reshape(-1,1),
                    bandpower(window_data, fs, [13,30]).reshape(-1,1),
                    bandpower(window_data, fs, [30,60]).reshape(-1,1),
                    hjorth_feats,
                    shannon_feats,
                    spectral_feats,
                    fractal_feats,
                    wavelet_feats,
                    zcr_feats,
                    rms_feats,
                    peak_freq_feats,
                    sef_feats,
                    spectral_skew_feats,
                    spectral_kurt_feats
                ])
                # Connectivity features
                num_channels = window_data.shape[0]
                pli_matrix = np.zeros((num_channels, num_channels))
                cross_corr_matrix = np.zeros((num_channels, num_channels))
                for i_ch in range(num_channels):
                    for j_ch in range(i_ch+1, num_channels):
                        pli_matrix[i_ch, j_ch] = phase_locking_value(window_data[i_ch], window_data[j_ch])
                        cross_corr_matrix[i_ch, j_ch] = cross_correlation(window_data[i_ch], window_data[j_ch])
                pli_features = pli_matrix[np.triu_indices(num_channels, k=1)]
                cross_corr_features = cross_corr_matrix[np.triu_indices(num_channels, k=1)]
                pli_features_expanded = np.tile(pli_features, (features.shape[0], 1))
                cross_corr_features_expanded = np.tile(cross_corr_features, (features.shape[0], 1))
                features = np.hstack([features, pli_features_expanded, cross_corr_features_expanded])
                if printout_count < 1:
                    print(f"Final feature vector shape: {features.shape}")
                    printout_count += 1
                features = features.flatten()
                X.append(features)
                y.append(class_idx)
    X = np.array(X)
    y = np.array(y)
    if len(X) > 0:
        print("\nFinal feature verification:")
        print(f"Dataset shape: X={X.shape}, y={y.shape}")
        print(f"Max variance: {np.max(X[:,1]):.1f} (should be <22.5)")
        print(f"Max skewness: {np.max(X[:,2]):.1f} (should be <10)")
        print(f"Mean bandpower: {np.mean(X[:,10:14]):.3f} (should be 0-1)")
        plt.figure(figsize=(12,6))
        plt.plot(np.max(np.abs(X), axis=0))
        plt.title("Maximum Absolute Feature Values")
        plt.xlabel("Feature Index")
        plt.ylabel("Value")
        plt.axhline(y=10, color='r', linestyle='--', label='Expected Max')
        plt.legend()
        plt.show()
    return X, y, class_labels, b, a

def plot_selected_features(X, y, class_labels, feature_indices):
    feature_names = [f"Feature {i+1}" for i in range(X.shape[1])]
    selected_features = [feature_names[i] for i in feature_indices]
    data = []
    for i in range(len(y)):
        for feature_idx, feature_name in zip(feature_indices, selected_features):
            data.append((feature_name, X[i, feature_idx], class_labels[y[i]]))
    df_plot = pd.DataFrame(data, columns=["Feature", "Value", "Class"])
    plt.figure(figsize=(12,6))
    sns.boxplot(x="Feature", y="Value", hue="Class", data=df_plot)
    plt.xticks(rotation=45, ha='right')
    plt.title("Feature Distributions by Class (Subset)")
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def plot_class_probability_distributions(y_proba, class_labels):
    plt.figure(figsize=(12,6))
    for i, class_label in enumerate(class_labels):
        sns.histplot(y_proba[:, i], bins=50, kde=True, label=class_label, alpha=0.5)
    plt.xlabel("Predicted Probability")
    plt.ylabel("Frequency")
    plt.title("Class Probability Distributions")
    plt.legend()
    plt.show()

def find_optimal_thresholds(y_proba, y_test, class_labels, balance_factor=0.5):
    optimal_thresholds = {}
    performance_metrics = {}
    for i, class_name in enumerate(class_labels):
        precision, recall, thresholds = precision_recall_curve((y_test == i).astype(int), y_proba[:, i])
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
        gmean_scores = np.sqrt(precision * recall)
        class_ratio = np.mean(y_test == i)
        balanced_scores = gmean_scores * (1 + balance_factor * (1 - class_ratio))
        valid_idx = np.where(precision >= 0.5)[0]
        if len(valid_idx) > 0:
            best_idx = valid_idx[np.argmax(balanced_scores[valid_idx])]
        else:
            best_idx = np.argmax(balanced_scores)
        best_idx = min(best_idx, len(thresholds)-1)
        optimal_threshold = thresholds[best_idx]
        optimal_thresholds[class_name] = optimal_threshold
        performance_metrics[class_name] = {
            'gmean': gmean_scores[best_idx],
            'f1': f1_scores[best_idx],
            'precision': precision[best_idx],
            'recall': recall[best_idx],
            'threshold': optimal_threshold
        }
    return optimal_thresholds, performance_metrics

def get_class_specific_feature_importance(X_train, y_train, class_labels, n_estimators=50):
    class_importances = []
    for class_idx in range(len(class_labels)):
        binary_y = (y_train == class_idx).astype(int)
        clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        clf.fit(X_train, binary_y)
        noise = np.random.normal(0, 1e-6, size=clf.feature_importances_.shape)
        class_importances.append(clf.feature_importances_ + noise)
    return np.array(class_importances)

def feature_selection_objective(feature_threshold, importance_scores):
    selected_indices = np.where(importance_scores > feature_threshold)[0]
    if len(selected_indices) < 50:
        return 1.0
    X_train_sel = X_train[:, selected_indices]
    X_test_sel = X_test[:, selected_indices]
    model = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1)
    model.fit(X_train_sel, y_train)
    y_pred = model.predict(X_test_sel)
    return 1 - accuracy_score(y_test, y_pred)

def optimize_feature_selection(X_train, y_train, class_labels, base_importance, performance_metrics):
    class_importances = get_class_specific_feature_importance(X_train, y_train, class_labels)
    perf_weights = np.array([1 - metrics['f1'] for metrics in performance_metrics.values()])
    perf_weights = perf_weights / np.sum(perf_weights)
    blended_importance = 0.8 * base_importance + 0.2 * np.average(class_importances, axis=0, weights=perf_weights)
    return blended_importance

def get_complete_feature_labels(num_channels=8, wavelet_levels=4):
    base_features = [
        "Mean", "Variance", "Skew", "Kurtosis", "Median", "Max", "Min", "Energy",
        "FFT Mean", "FFT Variance",
        "Bandpower 5-8Hz", "Bandpower 8-13Hz", "Bandpower 13-30Hz", "Bandpower 30-60Hz",
        "Hjorth Activity", "Hjorth Mobility", "Hjorth Complexity",
        "Shannon Entropy", "Spectral Entropy", "Fractal Dimension",
        "Zero-Crossing Rate", "RMS", 
        "Spectral Edge Frequency", "Peak Frequency",
        "Spectral Skewness", "Spectral Kurtosis"
    ]
    channel_features = [f"{feat} (Ch {ch+1})" for ch in range(num_channels) for feat in base_features]
    wavelet_features = [f"Wavelet Coeff {lvl} (Ch {ch+1})" for ch in range(num_channels) for lvl in range(wavelet_levels)]
    connectivity_features = []
    for i in range(num_channels):
        for j in range(i+1, num_channels):
            connectivity_features.append(f"PLI (Ch{i+1}-Ch{j+1})")
            connectivity_features.append(f"Cross-Corr (Ch{i+1}-Ch{j+1})")
    return channel_features + wavelet_features + connectivity_features

# --- Evaluation Helper Functions ---
def evaluate_model(model, X_test, y_test, config_name, class_labels):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nClassification Report for {config_name}:")
    print(classification_report(y_test, y_pred, target_names=class_labels, digits=3))
    print(f"Accuracy for {config_name}: {accuracy:.2f}%")
    conf_mat = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8,6))
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap="Blues",
                xticklabels=class_labels, yticklabels=class_labels)
    plt.title(f"Confusion Matrix ({config_name})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return accuracy

def evaluate_model_dynamic_threshold(y_proba, y_test, class_labels, optimal_thresholds, config_name, default_class="StopThoughts"):
    default_index = class_labels.index(default_class)
    y_pred = np.zeros_like(y_test)
    for i in range(len(y_test)):
        class_probs = y_proba[i]
        adjusted_probs = np.where(class_probs > [optimal_thresholds[label] for label in class_labels], class_probs, 0)
        if np.all(adjusted_probs == 0):
            y_pred[i] = default_index
        else:
            y_pred[i] = np.argmax(adjusted_probs)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nClassification Report for {config_name}:")
    print(classification_report(y_test, y_pred, target_names=class_labels, digits=3))
    print(f"Accuracy for {config_name}: {accuracy:.2f}%")
    conf_mat = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8,6))
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap="Blues",
                xticklabels=class_labels, yticklabels=class_labels)
    plt.title(f"Confusion Matrix ({config_name})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return accuracy







# --- Main Code Section ---
base_dir = r"c:\Users\Brendon\Desktop\Robot Movements 20-seconds"
fs = 500
X, y, class_labels, b, a = load_data(base_dir, fs, window_size=1.0, step_size=0.5, files_per_class=1, trim_seconds=5)

# Balance Dataset and Stratified Train/Test Split
min_samples = np.min(np.bincount(y))
train_idx, test_idx = [], []
for class_id in np.unique(y):
    indices = np.where(y == class_id)[0]
    np.random.shuffle(indices)
    split = int(0.7 * min_samples)
    train_idx.extend(indices[:split])
    test_idx.extend(indices[split:])
X_train, y_train = X[train_idx], y[train_idx]
X_test, y_test = X[test_idx], y[test_idx]
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# --- Scaler Comparison on Raw Features ---
cv = 5
n_samples = int(X_train.shape[0] * (cv - 1) / cv)
scalers = {
    "StandardScaler": StandardScaler(),
    "MinMaxScaler": MinMaxScaler(),
    "RobustScaler": RobustScaler(quantile_range=(5,95)),
    "QuantileTransformer": QuantileTransformer(n_quantiles=n_samples, output_distribution='normal')
}

cv_scores = {}
for name, scaler in scalers.items():
    pipeline = make_pipeline(scaler, RandomForestClassifier(random_state=42))
    scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
    cv_scores[name] = np.mean(scores)
    print(f"{name}: Mean accuracy = {np.mean(scores):.4f}")
names = list(cv_scores.keys())
scores = list(cv_scores.values())
plt.figure(figsize=(8,4))
plt.bar(names, scores, color='skyblue')
plt.ylabel("Mean CV Accuracy")
plt.title("Scaler Comparison on Raw Features")
plt.show()

# --- Select Best Scaler ---
best_scaler_name = max(cv_scores, key=cv_scores.get)
print(f"Best scaler based on CV accuracy: {best_scaler_name}")
best_scaler = scalers[best_scaler_name]

# --- Standardize Features for Further Modeling Using Best Scaler ---
scaler_final = best_scaler
X_train_scaled = scaler_final.fit_transform(X_train)
X_test_scaled = scaler_final.transform(X_test)
print(f"Scaler fitted on {scaler_final.n_features_in_} features")
print(f"X_train_scaled shape: {X_train_scaled.shape}")

# --- Bayesian Optimization for Hyperparameter Tuning (All Features) ---
param_space = {
    'n_estimators': [1460],
    'min_samples_leaf': (3,6),
    'max_depth': [105],
    'max_features': (0.6, 0.9, 'uniform')
}
print("\nRunning Bayesian Optimization for All Features...")
start_time = timer()
optimizer = BayesSearchCV(RandomForestClassifier(random_state=42, oob_score=True, n_jobs=-1, warm_start=True), 
                          param_space, n_iter=5, cv=5, n_jobs=-1)
optimizer.fit(X_train_scaled, y_train)
best_params = optimizer.best_params_
end_time = timer()
print(f"Bayesian Optimization Completed in {end_time - start_time:.2f} seconds")
print("Best Parameters:")
for param, value in best_params.items():
    print(f"  {param}: {value}")

classes = np.unique(y_train)
weights = compute_class_weight('balanced', classes=classes, y=y_train)
class_weights = {cls: weight * 1.5 for cls, weight in zip(classes, weights)}

# --- Train Base Model (All Features) without Dynamic Thresholding ---
base_model_no_thresh = RandomForestClassifier(
    **best_params,
    class_weight=class_weights,
    bootstrap=True,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
base_model_no_thresh.fit(X_train_scaled, y_train)
accuracy_base = evaluate_model(base_model_no_thresh, X_test_scaled, y_test, "All Features (No Dynamic Thresholding)", class_labels)

# --- Train Base Model (All Features) with Dynamic Thresholding ---
base_model = RandomForestClassifier(
    **best_params,
    class_weight=class_weights,
    bootstrap=True,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
base_model.fit(X_train_scaled, y_train)
y_proba = base_model.predict_proba(X_test_scaled)
optimal_thresholds, performance_metrics = find_optimal_thresholds(y_proba, y_test, class_labels)
accuracy_dynamic = evaluate_model_dynamic_threshold(y_proba, y_test, class_labels, optimal_thresholds, "All Features + Dynamic Thresholding")

# --- Feature Selection to Get Reduced Features ---
blended_importance = optimize_feature_selection(X_train_scaled, y_train, class_labels, base_model.feature_importances_, performance_metrics)
search_space = [(0.0001, 0.005)]
res = gp_minimize(lambda thresh: feature_selection_objective(thresh, blended_importance), search_space, n_calls=30, random_state=42)
best_feature_threshold = res.x[0]
selected_indices = np.where(blended_importance > best_feature_threshold)[0]
X_train_selected = X_train_scaled[:, selected_indices]
X_test_selected = X_test_scaled[:, selected_indices]
print(f"Selected {X_train_selected.shape[1]} features out of {X_train_scaled.shape[1]}")

# --- Train Model with Reduced Features Only (No Dynamic Thresholding) ---
rf_reduced_only = RandomForestClassifier(**best_params, random_state=42)
rf_reduced_only.fit(X_train_selected, y_train)
accuracy_reduced_only = evaluate_model(rf_reduced_only, X_test_selected, y_test, "Reduced Features Only (No Dynamic Thresholding)", class_labels)

# --- Train Model with Reduced Features and Dynamic Thresholding ---
best_model_reduced = RandomForestClassifier(
    **best_params,
    bootstrap=True,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
best_model_reduced.fit(X_train_selected, y_train)
y_proba_reduced = best_model_reduced.predict_proba(X_test_selected)
optimal_thresholds_reduced, performance_metrics_reduced = find_optimal_thresholds(y_proba_reduced, y_test, class_labels)
accuracy_dynamic_reduced = evaluate_model_dynamic_threshold(y_proba_reduced, y_test, class_labels, optimal_thresholds_reduced, "Reduced Features + Dynamic Thresholding")

# --- Final Comparison Plot ---
configurations = ['All Features (No Dynamic)', 'All Features + Dynamic', 'Reduced Features + Dynamic', 'Reduced Features Only']
accuracies = [accuracy_base, accuracy_dynamic, accuracy_dynamic_reduced, accuracy_reduced_only]
plt.figure(figsize=(10,6))
sns.barplot(x=configurations, y=accuracies, palette="Blues", hue=configurations, dodge=False)
plt.legend([], [], frameon=False)
plt.ylabel("Accuracy (%)")
plt.title("Model Accuracy Comparison Across Configurations")
plt.ylim(0, 100)
plt.show()

# --- Save Model Package ---
def save_model_package(model, scaler, selected_indices, optimal_thresholds, performance_metrics, class_labels, filters, feature_labels, base_dir):
    model_package = {
        'model': model,
        'scaler': scaler,
        'selected_indices': selected_indices,
        'optimal_thresholds': optimal_thresholds,
        'performance_metrics': performance_metrics,
        'class_labels': class_labels,
        'filters': {'b': filters[0].tolist(), 'a': filters[1].tolist()},
        'feature_labels': feature_labels,
        'metadata': {
            'creation_date': datetime.now().isoformat(),
            'input_shape': (model.n_features_in_,),
            'classes': len(class_labels),
            'model_type': 'RandomForestClassifier'
        }
    }
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_dir = os.path.join(base_dir, f"eeg_model_{timestamp}")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model_package.joblib")
    joblib.dump(model_package, model_path)
    info = {
        'class_labels': class_labels,
        'num_features': len(selected_indices),
        'optimal_thresholds': optimal_thresholds,
        'creation_date': model_package['metadata']['creation_date']
    }
    with open(os.path.join(model_dir, "model_info.json"), 'w') as f:
        json.dump(info, f, indent=2)
    print(f"Model package saved to {model_dir}")
    return model_dir

feature_labels = get_complete_feature_labels(num_channels=8, wavelet_levels=4)
model_dir = save_model_package(
    model=best_model_reduced,
    scaler=scaler_final,
    selected_indices=selected_indices,
    optimal_thresholds=optimal_thresholds_reduced,
    performance_metrics=performance_metrics_reduced,
    class_labels=class_labels,
    filters=(b, a),
    feature_labels=feature_labels,
    base_dir=r"c:\Users\Brendon\Desktop\Robot Movements\saved_models"
)