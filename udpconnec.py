import socket

# marker send to MATLAB
# # 🔹 UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
# 🔹 EEG Stream Settings
# fs = 500  # Sampling rate (Hz)
# samples_per_packet = 125  # Send 50 samples per packet (0.1 sec of data)

eeg_bytes = bytearray(b'1')
sock.sendto(eeg_bytes, (UDP_IP, UDP_PORT))


# retrieve frame of PsychoPy  
def timesync():
    pass

