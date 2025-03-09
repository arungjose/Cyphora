import threading
import subprocess
import os
import time

def run_program(filename, args=None, capture_output=False):
    """Runs a program and handles input/output."""
    command = ["python", filename]
    if args:
        command.extend(args)

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE,
        text=True,
    )

    if capture_output:
        output, _ = process.communicate()
        return output

    return process

def run_tor():
    """Runs the Tor executable."""
    tor_path = os.path.join("bundle", "tor", "tor.exe")
    print("Starting Tor...")
    return subprocess.Popen(tor_path)

def run_ipfs_daemon():
    """Runs the ipfs daemon executable."""
    ipfs_path = os.path.join("kubo", "ipfs.exe")
    print("Starting ipfs daemon...")
    return subprocess.Popen([ipfs_path, "daemon"])  # Start the daemon

def run_bot_function():
    """Runs the telegram bot."""
    run_program("telegram_bot.py")

def main():
    """Main function to run the pipeline."""

    # Run the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot_function)
    bot_thread.daemon = True
    bot_thread.start()

    time.sleep(15)  # Wait 15 seconds for the bot to run.

    # Run Tor after 15 seconds
    tor_process = run_tor()

    time.sleep(30)  # Wait 30 seconds for tor to run.

    # Run the scraper
    run_program("scraper.py")

    time.sleep(30) #wait 30 seconds for scraper.py

    #Run ipfs daemon
    ipfs_process = run_ipfs_daemon()

    time.sleep(15) # Wait 15 seconds for ipfs daemon to run.

    # Run ipfs.py
    run_program("ipfs.py")

    # Keep the main thread running (optional)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Main program interrupted. Exiting.")

    tor_process.terminate() #kill tor.
    ipfs_process.terminate() #Kill ipfs daemon.

if __name__ == "__main__":
    main()