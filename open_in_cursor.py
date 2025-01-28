import sublime
import sublime_plugin
import subprocess
import os

class OpenFileInCursorCommand(sublime_plugin.TextCommand):
    """Opens the current file in Cursor editor.
    
    If a project folder is available, opens with project context.
    Otherwise opens just the single file in a new window.
    """
    def is_enabled(self):
        return bool(self.view.file_name())

    def is_visible(self):
        return bool(self.view.file_name())

    def run(self, edit):
        sublime.set_timeout_async(self._run_async, 0)

    def _run_async(self):
        try:
            subprocess.run(["cursor", "--version"], check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            sublime.error_message("cursor: command not found\n\nPlease verify that it is installed and in your PATH.")
            return

        file_path = self.view.file_name()
        window = sublime.active_window()
        folders = window.folders()

        if file_path and os.path.exists(file_path):
            try:
                if folders:
                    project_path = folders[0]
                    cmd = ["cursor", "-n", "--folder-uri", project_path, file_path]
                else:
                    cmd = ["cursor", "-n", file_path]
                    
                subprocess.run(cmd, check=True)
                sublime.status_message(f"Opened file in Cursor: {file_path}")
            except Exception as e:
                sublime.error_message(f"Error opening file in Cursor: {str(e)}")
        else:
            sublime.error_message("No valid file selected to open in Cursor.")
