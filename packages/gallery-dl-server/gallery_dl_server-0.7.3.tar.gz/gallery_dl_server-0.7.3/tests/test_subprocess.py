import os, sys, subprocess

prompt = os.environ.get("PROMPT", "None")

os.environ["PROMPT"] = "$P$G"

command = [sys.executable, "print_name.py"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

while True:
    if process.stdout:
        output = process.stdout.readline()

        if output == "" and process.poll() is not None:
            break

        if output:
            print(output)

status = process.wait()
print(status)

if prompt == "None":
    input("\n" + "Press Enter to continue . . . ")
