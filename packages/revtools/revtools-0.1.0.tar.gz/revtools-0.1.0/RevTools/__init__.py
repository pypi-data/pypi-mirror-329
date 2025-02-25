from .debugger import Debugger

# Global instance to track debugged files
_debugger = None

def debug_code(file_or_folder, current_folder=False, api_key=None):
    """
    Debug a file or folder using Gemini.
    """
    if api_key is None:
        raise ValueError("Please provide a Gemini API key.")

    global _debugger
    if _debugger is None:
        _debugger = Debugger(api_key)
    _debugger.debug_code(file_or_folder, current_folder)