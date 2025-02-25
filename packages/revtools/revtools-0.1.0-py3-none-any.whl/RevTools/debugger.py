import os
import ast
import hashlib
import google.generativeai as genai

class Debugger:
    def __init__(self, api_key):
        # Initialize Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.debugged_files = {}  # Track debugged files and their hashes

    def debug_code(self, file_or_folder, current_folder=False):
        """
        Debug a file or folder using Gemini.
        """
        if current_folder:
            # Process all Python files in the folder
            if os.path.isdir(file_or_folder):
                for root, _, files in os.walk(file_or_folder):
                    for file in files:
                        if file.endswith(".py"):
                            file_path = os.path.join(root, file)
                            self._process_file(file_path)
            else:
                print(f"Error: {file_or_folder} is not a folder.")
        else:
            # Process a single file
            if os.path.isfile(file_or_folder) and file_or_folder.endswith(".py"):
                self._process_file(file_or_folder)
            else:
                print(f"Error: {file_or_folder} is not a valid Python file.")

    def _process_file(self, file_path):
        """
        Process a single file: fix errors and save the original code.
        """
        # Step 1: Get the file hash
        file_hash = self._get_file_hash(file_path)

        # Step 2: Check if the file has been debugged before
        if file_path in self.debugged_files and self.debugged_files[file_path] == file_hash:
            print(f"Skipping unmodified file: {file_path}")
            return

        # Step 3: Read the file
        with open(file_path, "r") as f:
            code = f.read()

        # Step 4: Save the original code to a backup file (if it doesn't exist)
        backup_path = file_path + ".original"
        if not os.path.exists(backup_path):
            with open(backup_path, "w") as backup:
                backup.write(code)

        # Step 5: Check for syntax errors
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f"Syntax error found in {file_path}: {e}")
            # Step 6: Fix errors using Gemini
            fixed_code = self._fix_errors_with_gemini(code, str(e))
            if fixed_code:
                # Step 7: Save the fixed code to the original file
                with open(file_path, "w") as f:
                    f.write(fixed_code)
                print(f"Errors fixed in {file_path}. Original code saved to {backup_path}.")
                # Update the file hash in the debugged_files dictionary
                self.debugged_files[file_path] = file_hash
            else:
                print(f"Failed to fix errors in {file_path}.")
        else:
            print(f"No syntax errors found in {file_path}.")
            # Update the file hash in the debugged_files dictionary
            self.debugged_files[file_path] = file_hash

    def _fix_errors_with_gemini(self, code, error_message):
        """
        Use Gemini to fix errors in the code.
        """
        prompt = f"Fix the following Python code. The error is: {error_message}\n\nCode:\n{code}"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return None

    def _get_file_hash(self, file_path):
        """
        Generate a hash of the file content.
        """
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()