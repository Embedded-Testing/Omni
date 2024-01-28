import subprocess

# Define the command to be executed
command = "sigrok-cli --version"

# Execute the command and capture the output
try:
    result = subprocess.check_output(command, shell=True, text=True)
except subprocess.CalledProcessError as e:
    result = e.output

# The output is now stored in 'result'
print("Command output:" + result+"ABC")
