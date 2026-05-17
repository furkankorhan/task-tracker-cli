import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import app


class TaskTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def capture(self, func, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            func(*args)
        return output.getvalue()

    def test_add_and_list_task(self):
        add_output = self.capture(app.add_task, "Write README")
        list_output = self.capture(app.list_tasks)

        self.assertIn('Added task: "Write README"', add_output)
        self.assertIn("[ ]  Write README", list_output)
        self.assertTrue(Path("tasks.db").exists())

    def test_complete_task(self):
        self.capture(app.add_task, "Learn SQLite")
        done_output = self.capture(app.complete_task, 1)
        list_output = self.capture(app.list_tasks)

        self.assertIn("Marked task #1 as done.", done_output)
        self.assertIn("[x]  Learn SQLite", list_output)

    def test_delete_missing_task(self):
        output = self.capture(app.delete_task, 99)

        self.assertIn("Task #99 was not found.", output)


if __name__ == "__main__":
    unittest.main()
