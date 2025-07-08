import scipy.io as sio
import numpy as np
import h5py
import os
from collections import defaultdict
import argparse

# --- 1. Configuration ---
data_variable_name = 'y'
initial_sync_trigger = 21

parser = argparse.ArgumentParser(description="Process EEG data from a .mat file, synchronize time, and save blocks by epoch transitions.")
parser.add_argument('mat_file_path', type=str, default='data.mat', help='Path to the .mat file containing EEG data.')
parser.add_argument('output_directory', type=str, default='epoch_output_files', help='Path to the output directory for saving epoch files.')
args = parser.parse_args()

mat_file_path = args.mat_file_path
output_directory = args.output_directory

# map int values to epoch names (optional, for clarity)
epoch_names = {
    0: "BeforeExperiment",
    1: "fixation",
    2: "encoding",
    4: "maintenance",
    8: "retrieval",
    13: "feedback",
    21: "start",
    31: "end",
    45: "ITI",
    66: "ignore",
    'start': "preprocess"
}


# --- 2. Load the .mat File (v7.3 compatible) ---
try:
    with h5py.File(mat_file_path, 'r') as file:
        print(f"Successfully loaded '{mat_file_path}' using h5py.")
        # Transpose the data so that rows are signals and columns are time points
        eeg_data = file[data_variable_name][()].T
        print(f"Data matrix '{data_variable_name}' found with shape: {eeg_data.shape}")

except (OSError, KeyError):
    try:
        mat_contents = sio.loadmat(mat_file_path)
        print(f"Successfully loaded '{mat_file_path}' using SciPy.")
        eeg_data = mat_contents[data_variable_name]
        print(f"Data matrix '{data_variable_name}' found with shape: {eeg_data.shape}")
    except Exception as e:
        print(f"Error: Could not load the MAT file. Please check the path and variable name.")
        print(f"Details: {e}")
        exit()

# --- 3. Perform Initial Time Synchronization (New Section) ---
print(f"\nPerforming initial time synchronization based on trigger value: {initial_sync_trigger}...")
time_row = eeg_data[0, :]
epoch_row = eeg_data[-1, :]

try:
    # Find the index of the first occurrence of the sync trigger
    sync_index = np.where(epoch_row == initial_sync_trigger)[0][0]
    
    # Get the timestamp at that exact moment
    t_start = time_row[sync_index]
    
    # Create the new, globally synchronized time vector
    synchronized_time_vector = time_row - t_start
    
    # Replace the original time row in the main data matrix
    eeg_data[0, :] = synchronized_time_vector
    
    print(f"Synchronization complete. New t=0 corresponds to the first instance of '{initial_sync_trigger}'.")

    # Save time synchronized data to file
    output_filename = os.path.join(
        output_directory, 
        f'time_synchronized_data.mat'
    )
    sio.savemat(output_filename, {data_variable_name: eeg_data})
    print(f"Saved {output_filename} with shape {eeg_data.shape}")

    

except IndexError:
    print(f"Warning: Initial sync trigger '{initial_sync_trigger}' not found. Skipping initial synchronization.")


# --- 4. Identify Contiguous Blocks ---
# The epoch row is already defined from the sync step
change_indices = np.where(epoch_row[1:] != epoch_row[:-1])[0] + 1
block_start_indices = np.concatenate(([0], change_indices))

# --- 5. Create Output Directory ---
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"\nCreated output directory: '{output_directory}'")

# --- 6. Loop Through Blocks, Name by Transition, and Save ---
# A dictionary to count instances of each unique transition (e.g., 23 -> 43).
instance_counters = defaultdict(int)

print("\nProcessing and saving each block based on its transition...")

for i, start_index in enumerate(block_start_indices):
    # Determine the end index of the current block.
    if i < len(block_start_indices) - 1:
        end_index = block_start_indices[i+1]
    else:
        end_index = len(epoch_row)

    # Get the data for just this block.
    block_data = eeg_data[:, start_index:end_index]
    
    # Get the epoch value for this block.
    current_epoch_val = int(epoch_row[start_index])
    
    # Determine the previous epoch's value.
    if i == 0:
        previous_epoch_val = 'start'
    else:
        previous_epoch_val = int(epoch_row[start_index - 1])
    
    # Create a unique key for the transition and increment its instance counter.
    transition_key = (previous_epoch_val, current_epoch_val)
    instance_counters[transition_key] += 1
    instance_num = instance_counters[transition_key]
    
    # Define the new filename based on the transition.
    output_filename = os.path.join(
        output_directory, 
        f'{epoch_names[previous_epoch_val]}->{epoch_names[current_epoch_val]}_instance_{instance_num}.mat'
    )
    
    # Create a dictionary to save in the new .mat file.
    data_to_save = {data_variable_name: block_data}
    
    # Save the new .mat file.
    sio.savemat(output_filename, data_to_save)
    print(f"Saved {output_filename} with shape {block_data.shape}")

print("\nProcessing complete! All blocks have been saved by their transition. ✅")