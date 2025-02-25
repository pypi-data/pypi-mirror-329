import os
from time import time
import shutil
import tempfile
import unittest
import subprocess
import select



# --- The Shell implementation (as provided earlier) ---
class CommandResult:
    def __init__(self, command: str, exit_code: int, stdout: str, stderr: str):
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        return f"CommandResult(command={self.command}, exit_code={self.exit_code}, stdout={self.stdout!r}, stderr={self.stderr!r})"

class Shell:
    def __init__(self):
        # Use the default system shell (or /bin/sh if SHELL is not defined)
        self.shell = os.environ.get("SHELL", "/bin/sh")
        self.max_timeout = int(os.environ.get("MAX_TIMEOUT", "60"))
        # Disable the shell prompt by overriding PS1 (helps avoid extra output)
        env = os.environ.copy()
        env["PS1"] = ""
        self.process = subprocess.Popen(
            self.shell,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # text mode
            bufsize=1,  # line-buffered
            env=env
        )

    def executeCommand(self, cmd: str) -> CommandResult:
        # Define a unique marker that signals command completion along with the exit code.
        marker = f"__CMD_DONE_{os.urandom(4).hex()}__"
        # Append an echo command that outputs the marker and the exit code of the last command ($?)
        full_cmd = f"{cmd}\necho {marker} $?\n"
        
        # Send the command to the shell's standard input.
        self.process.stdin.write(full_cmd)
        self.process.stdin.flush()

        stdout_lines = []
        exit_code = None
        timed_out = True

        # Read the shell's output until the marker line is detected.
        start_time = time()
        while time() - start_time < self.max_timeout:
            line = self.process.stdout.readline()
            if not line:
                timed_out = False
                break  # End-of-file or process termination.
            if marker in line:
                # The marker line should be of the form: "__CMD_DONE_{random}__ <exit_code>"
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        exit_code = int(parts[1])
                    except ValueError:
                        exit_code = None
                timed_out = False
                break
            stdout_lines.append(line)

        # Optionally, try to read any stderr output that might have been generated.
        stderr_output = ""
        # Use a short timeout so as not to block if there is no stderr output.
        while True:
            r, _, _ = select.select([self.process.stderr], [], [], 0.1)
            if self.process.stderr in r:
                err_line = self.process.stderr.readline()
                if not err_line:
                    break
                stderr_output += err_line
            else:
                break

        stdout_output = "".join(stdout_lines)
        if timed_out:
            stdout_output += f"\nCommand timed out after {self.max_timeout}s"

        cmd_result = CommandResult(cmd, exit_code, stdout_output, stderr_output)
        return cmd_result
    
    def close(self):
        for pipe in (self.process.stdin, self.process.stdout, self.process.stderr):
            if pipe:
                pipe.close()
        self.process.terminate()
        self.process.wait(timeout=1)
        if self.process.poll() is None:
            self.process.kill()

# --- Test Suite ---
class TestShell(unittest.TestCase):
    def setUp(self):
        # Create a Shell instance for each test.
        self.shell = Shell()
        # Use a temporary directory to run directory-related tests without affecting the real filesystem.
        self.test_dir = tempfile.mkdtemp(prefix="shell_test_")
        # Change the shell's current directory to the temporary directory.
        result = self.shell.executeCommand(f"cd {self.test_dir}")
        self.assertEqual(result.exit_code, 0, "Failed to change to temporary directory in setUp.")

    def tearDown(self):
        # Terminate the persistent shell process.
        self.shell.close()
        self.shell.process.terminate()
        self.shell.process.wait()
        # Remove the temporary directory.
        shutil.rmtree(self.test_dir)

    def test_echo(self):
        # Test a simple command that outputs text.
        result = self.shell.executeCommand("echo Hello, World!")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout.strip(), "Hello, World!")

    def test_cd_and_pwd(self):
        # Create a subdirectory within the temporary directory.
        subdir = "subdir"
        result = self.shell.executeCommand(f"mkdir -p {subdir}")
        self.assertEqual(result.exit_code, 0)
        # Change into the subdirectory.
        result = self.shell.executeCommand(f"cd {subdir}")
        self.assertEqual(result.exit_code, 0)
        # Call pwd to verify that we are in the new directory.
        result = self.shell.executeCommand("pwd")
        expected_dir = os.path.join(self.test_dir, subdir)
        # The pwd output should match the expected absolute path.
        self.assertEqual(result.stdout.strip(), expected_dir)

    def test_invalid_command(self):
        # Run a command that does not exist.
        result = self.shell.executeCommand("nonexistent_command")
        # The exit code should be non-zero.
        self.assertNotEqual(result.exit_code, 0)
        # Expect an error message indicating that the command was not found.
        error_lower = result.stderr.lower()
        self.assertTrue("not found" in error_lower or "command not found" in error_lower)

    def test_command_exit_codes(self):
        # Test that the command "true" returns 0.
        result = self.shell.executeCommand("true")
        self.assertEqual(result.exit_code, 0)
        # Test that the command "false" returns a non-zero exit code.
        result = self.shell.executeCommand("false")
        self.assertNotEqual(result.exit_code, 0)

    def test_directory_persistence(self):
        # Create and enter a new subdirectory.
        subdir = "persistent_test"
        result = self.shell.executeCommand(f"mkdir -p {subdir}")
        self.assertEqual(result.exit_code, 0)
        result = self.shell.executeCommand(f"cd {subdir}")
        self.assertEqual(result.exit_code, 0)
        # Verify that pwd reflects the new directory.
        result = self.shell.executeCommand("pwd")
        self.assertEqual(result.stdout.strip(), os.path.join(self.test_dir, subdir))
        # Change directory back to the parent directory.
        result = self.shell.executeCommand("cd ..")
        self.assertEqual(result.exit_code, 0)
        result = self.shell.executeCommand("pwd")
        self.assertEqual(result.stdout.strip(), self.test_dir)

    def test_command_timeout(self):
        # Override the default timeout for this test
        self.shell.max_timeout = 2  # Set timeout to 2 seconds
        
        # Test a command that should timeout (sleep for longer than the timeout)
        result = self.shell.executeCommand("sleep 5")
        
        # Verify timeout message appears in stdout
        self.assertIn(f"Comand timed out after {self.shell.max_timeout}s", result.stdout)
        
        # Since the command timed out, exit_code should be None
        self.assertIsNone(result.exit_code)

    def test_long_running_command_completes(self):
        # Test a command that runs for less than the timeout period
        self.shell.max_timeout = 3  # Set timeout to 3 seconds
        result = self.shell.executeCommand("sleep 1")
        
        # Verify command completed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Verify no timeout message in stdout
        self.assertNotIn("timed out after", result.stdout)

    def test_timeout_environment_variable(self):
        # Test that the MAX_TIMEOUT environment variable is respected
        original_timeout = os.environ.get("MAX_TIMEOUT")
        try:
            os.environ["MAX_TIMEOUT"] = "1"  # Set 1 second timeout
            new_shell = Shell()  # Create new shell instance to pick up new timeout
            
            # Run a command that should timeout
            result = new_shell.executeCommand("sleep 3")
            
            # Verify timeout message
            self.assertIn("Comand timed out after 1s", result.stdout)
            self.assertIsNone(result.exit_code)
            
            new_shell.close()
        finally:
            # Restore original MAX_TIMEOUT value
            if original_timeout is not None:
                os.environ["MAX_TIMEOUT"] = original_timeout
            else:
                del os.environ["MAX_TIMEOUT"]

if __name__ == "__main__":
    unittest.main()
