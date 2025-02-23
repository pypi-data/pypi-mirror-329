import time

# Sample string
msg = "# example message"

# Number of iterations for averaging
iterations = 10000000

# Timing slicing
start_time = time.time()
for _ in range(iterations):
    sliced_msg = msg[2:]
end_time = time.time()
slicing_time = end_time - start_time

# Timing removeprefix
start_time = time.time()
for _ in range(iterations):
    prefix_removed_msg = msg.removeprefix("# ")
end_time = time.time()
removeprefix_time = end_time - start_time

# Print results
print(f"Slicing took {slicing_time:.10f} seconds for {iterations} iterations.")
print(f"removeprefix() took {removeprefix_time:.10f} seconds for {iterations} iterations.")

input("\n" + "Press Enter to continue . . . ")
