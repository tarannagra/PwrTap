from tqdm import tqdm
import time

def initialising():
    time.sleep(1)  # Simulate some work

def settingup():
    time.sleep(2)  # Simulate some work

def processing():
    time.sleep(3)  # Simulate some work

# List of functions
functions = [initialising, settingup, processing]

# Initialize the progress bar
total_functions = len(functions)
with tqdm(total=total_functions, desc="Progress", ncols=100) as pbar:
    for func in functions:
        func()  # Call the function
        pbar.update(1)  # Increment the progress bar

print("All functions completed!")
