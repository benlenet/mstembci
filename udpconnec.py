import socket
import keyboard
# marker send to MATLAB
# # 🔹 UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
# 🔹 EEG Stream Settings
# fs = 500  # Sampling rate (Hz)
# samples_per_packet = 125  # Send 50 samples per packet (0.1 sec of data)

while(1):
    userval = input("type number value to send to udp: ")
    try:
        eegbytes = bytes([int(userval)])
    except:
        print("cannot cast", userval, "as int\n")
        continue
    sock.sendto(eegbytes, (UDP_IP, UDP_PORT))
    print("sent to udp value:", eegbytes, '\n')

# retrieve frame of PsychoPy  
def timesync():
    pass

