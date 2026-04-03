import unittest
from unittest.mock import patch, MagicMock
from port_utils import get_pids_listening_on_port, kill_processes_on_port
class PortUtilsTestCase(unittest.TestCase):
    def test_get_pids_parses_lsof_output(self):
        fake = MagicMock()
        fake.returncode = 0
        fake.stdout = "1234\n5678\n"
        with patch("port_utils.subprocess.run", return_value=fake):
            self.assertEqual(get_pids_listening_on_port(5000), [1234, 5678])
    def test_kill_calls_os_kill(self):
        fake = MagicMock()
        fake.returncode = 0
        fake.stdout = "42\n"
        with patch("port_utils.subprocess.run", return_value=fake):
            with patch("port_utils.os.kill") as mock_kill:
                kill_processes_on_port(5000)
                self.assertEqual(mock_kill.call_count, 1)
if __name__ == "__main__":
    unittest.main(verbosity=2)
