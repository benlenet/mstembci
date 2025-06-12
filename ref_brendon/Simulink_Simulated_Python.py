import scipy.io
import numpy as np
import socket
import time
import os
import random

# 🔹 UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 🔹 EEG Stream Settings
fs = 500  # Sampling rate (Hz)
samples_per_packet = 125  # Send 50 samples per packet (0.1 sec of data)
mat_dir = r"c:\Users\e203gtec\Desktop\Robot Movements 20-seconds\OpenThoughts"  # 🔹 Path to your EEG files

# Get all .mat files in the directory
mat_files = [f for f in os.listdir(mat_dir) if f.endswith(".mat")]

if not mat_files:
    raise ValueError("❌ No .mat files found!")

print(f"📡 Found {len(mat_files)} EEG files. Streaming continuously...")

while True:
    # 🎲 Pick a random EEG file
    mat_file = random.choice(mat_files)
    mat_data = scipy.io.loadmat(os.path.join(mat_dir, mat_file))

    # Extract EEG data (assumes 8 channels, time in columns)
    eeg_data = mat_data[list(mat_data.keys())[-1]][1:, :]  # Ignore first row if metadata

    num_samples = eeg_data.shape[1]  # Total time samples
    num_packets = num_samples // samples_per_packet  # Number of UDP packets to send

    print(f"🚀 Streaming {mat_file} ({num_samples} samples, {num_packets} packets)")

    # 🔹 Stream EEG data in real-time
    for i in range(num_packets):
        chunk = eeg_data[:, i * samples_per_packet : (i + 1) * samples_per_packet]
        eeg_bytes = chunk.astype(np.float64).tobytes()
        sock.sendto(eeg_bytes, (UDP_IP, UDP_PORT))
        
        time.sleep(samples_per_packet / fs)  # Maintain real-time pacing (0.1 sec per packet)

    print(f"🔁 Finished {mat_file}, switching to another EEG file...")