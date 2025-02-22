# src/stratio/utils/commons.py
import contextlib
import os
import signal
import subprocess
import sys
from logging import Logger


def execute_command(command: list[str], logger: Logger, environment: dict = None) -> None:
    try:
        # Start the subprocess in a new process group to isolate signal handling
        process = subprocess.Popen(
            command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, preexec_fn=os.setsid, env=environment
        )

        # Define a signal handler to forward SIGINT and SIGTERM to the subprocess
        def signal_handler(signum, frame):
            logger.debug(f"Received signal {signum}, forwarding to child process.")
            try:
                os.killpg(os.getpgid(process.pid), signum)  # Forward the signal to the subprocess group
            except Exception as error:
                logger.error(f"Failed to forward signal {signum} to child process: {error}")

        # Register the signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Wait for the subprocess to complete
        process.wait()

        # Optionally, check the return code
        if process.returncode != 0:
            logger.error(f"AWS CLI command exited with return code {process.returncode}.")
            raise RuntimeError(f"AWS CLI command exited with return code {process.returncode}.")
    except KeyboardInterrupt as e:
        logger.info("SSM session interrupted by user.")
        with contextlib.suppress(Exception):
            os.killpg(os.getpgid(process.pid), signal.SIGINT)
        raise RuntimeError("SSM session interrupted by user.") from e
