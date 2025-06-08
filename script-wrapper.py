import subprocess
import sys
import signal
import shlex

process = None  # Global reference to the process


def handle_sigint(signum, frame):
    global process
    print("\n[Wrapper] Ctrl+C received.")
    if process and process.poll() is None:
        print("[Wrapper] Terminating child process...")
        process.terminate()
    else:
        print("[Wrapper] No active process to terminate.")

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_sigint)

def run_command(cmd):
    global process
    while True:
        print(f"\nRunning command: {cmd}\n{'='*40}")
        process = start_process(cmd)
        process.wait()
        choice = input("\nProcess ended. Restart? (y/n): ").strip().lower()
        if choice != 'y':
            break

def run_commands_in_sequences(cmds):
    global process
    while True:
        print(f"\nRunning {len(cmds)} commands: \n{'='*40}")
        for cmd in cmds:
            cmd = cmd.strip()
            print(f"Running command: {cmd}")
            process = start_process(cmd)
            process.wait()

        choice = input("\nProcess ended. Restart? (y/n): ").strip().lower()
        if choice != 'y':
            break

def start_process(cmd):
    global process
    process = subprocess.Popen(cmd, shell=False)
    return process

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_wrapper.py <command_to_run>")
        sys.exit(1)

    print(f"Arguments: {sys.argv[1:]}")

    full_input = shlex.join(sys.argv[1:])
    full_input = full_input.replace("'", '"')  # Replace single quote to double quotes


    print(f"Full input: {full_input}")

    # Split into multiple commands if "command=" appears multiple times
    if "command=" in full_input:
        # Find all substrings starting with "command=" and split accordingly
        parts = full_input.split("command=")
        print(f"Parts: {parts}")
        run_commands_in_sequences(parts[1:]) # skip the first empty part before the first command=
    else:
        run_command(full_input)
