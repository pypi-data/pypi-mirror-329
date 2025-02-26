import threading
from datetime import timedelta, datetime
import os
import platform
import shlex
from subprocess import Popen, PIPE, TimeoutExpired
from threading import Thread, Event
import time
from queue import Queue

from kortical.helpers import print_helpers


class Console:

    @classmethod
    def run(cls, command, environment_variables=None):
        console = cls(command, environment_variables)
        console._start_read_line_threads()

        # shlex only works on linux/mac, on windows it will remove "\"
        # which breaks paths passed into the CLI.
        # No need to split on Windows because subprocess.Popen calls subprocess.list2cmdline
        if platform.system() == 'Windows':
            args = command
        else:
            args = shlex.split(command)
        console._start_process(args)
        return console

    def __init__(self, command, environment_variables):
        self.command = command
        self.environment_variables = environment_variables if environment_variables is not None else {}
        self.output = '\n'                             # Console output.
        self.output_lock = threading.Lock()
        self.error_lock = threading.Lock()
        self.error = ''                                # Error output.
        self.process = None                            # Process launched by the command we want to test on console.
        self.threads = []                              # Background threads which read lines from the stdout and stderr.
        self.cancel = Event()                          # Flag to cancel background thread.
        self.exit_code = None                          # Exit code of the process.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_for_exit()

    def wait_for_output(self, desired_output, timeout_seconds=30):
        end_time = datetime.now() + timedelta(seconds=timeout_seconds)
        while datetime.now() < end_time:
            if desired_output in self.output:
                return
            time.sleep(0.25)

        self.cancel.set()
        for thread in self.threads:
            thread.join()
        if desired_output in self.output:
            return

        raise TimeoutError(f"Timed out.\n\n"
                        f"Desired output: \n{desired_output}\n"
                        f"Console output:\n{self.output}\n"
                        f"Error output:\n{self.error}\n")

    def wait_for_error(self, desired_output, timeout_seconds=30):
        end_time = datetime.now() + timedelta(seconds=timeout_seconds)
        while datetime.now() < end_time:
            if desired_output in self.error:
                return
            time.sleep(0.25)

        self.cancel.set()
        for thread in self.threads:
            thread.join()
        if desired_output in self.error:
            return

        raise TimeoutError(f"Timed out.\n\n"
                        f"Desired output: \n{desired_output}\n"
                        f"Console output:\n{self.output}\n"
                        f"Error output:\n{self.error}\n")

    def input(self, user_input, hide_in_output=False):
        if self.process is None:
            raise Exception("Process has not started yet.")

        # Process user input
        if not user_input.endswith('\n'):
            user_input += '\n'

        self.process.stdin.write(user_input)
        self.process.stdin.flush()

        with self.output_lock:
            if hide_in_output:
                self.output += '(HIDDEN INPUT)\n'
            else:
                self.output += user_input

    def return_output(self, raw=False):
        # Built up text of full run.
        # Should mirror what we see on the console as much as possible
        string = self.output
        # Remove special color characters
        if not raw:
            string = print_helpers.strip_colour(string)

        return string

    def wait_for_exit(self, timeout_seconds=None):
        if self.exit_code is not None:
            return self.exit_code

        if self.process is None:
            raise Exception("Process was not started.")

        try:
            self.process.wait(timeout=timeout_seconds)
        except TimeoutExpired:
            # We timed out: kill the process
            self.process.kill()
            self.exit_code = 124
            raise
        else:
            # Normal exit
            self.exit_code = self.process.returncode

        # Give the threads time to read the last lines of the process
        time.sleep(0.25)
        # End thread/subprocess and check the error code
        self.cancel.set()
        for thread in self.threads:
            thread.join()

        self.exit_code = self.process.returncode
        return self.exit_code

    def _read_stdout(self, event: Event):
        event.set()
        while not self.cancel.is_set():
            if self.process is not None:
                for line in iter(self.process.stdout.readline, ''):
                    print(line, end='')
                    with self.output_lock:
                        self.output += line
                self.process.stdout.flush()
            time.sleep(0.25)
        return

    def _read_stderr(self, event: Event):
        event.set()
        while not self.cancel.is_set():
            if self.process is not None:
                for line in iter(self.process.stderr.readline, ''):
                    print(line, end='')
                    with self.error_lock:
                        self.error += line
                self.process.stderr.flush()
            time.sleep(0.25)
        return

    def _start_read_line_threads(self):
        targets = [self._read_stdout, self._read_stderr]
        ready_events = [Event() for target in targets]
        for index, target in enumerate(targets):
            ready_event = ready_events[index]
            thread = Thread(target=target, args=(ready_event,), daemon=True)
            thread.start()
            self.threads.append(thread)
        for ready_event in ready_events:
            ready_event.wait()

    def _start_process(self, args_sequence):
        my_env = os.environ.copy()
        my_env.update(self.environment_variables)
        self.process = Popen(args_sequence, env=my_env, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
