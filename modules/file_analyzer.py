import hashlib
import os

def calculate_hashes(file_path):
    """Calculates MD5 and SHA-256 hashes for a given file."""
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
                md5.update(chunk)
        return {
            "md5": md5.hexdigest(),
            "sha256": sha256.hexdigest()
        }
    except Exception:
        return None

def analyze_file_heuristics(file_name):
    """Checks file extensions and naming patterns for common risk indicators."""
    dangerous_exts = ['.exe', '.bat', '.vbs', '.scr', '.pif', '.ps1', '.cmd']
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext in dangerous_exts:
        return "High Risk", f"Executable script/binary extension detected ({ext})."
    elif ext in ['.zip', '.rar', '.7z']:
        return "Suspicious / Archive", "Compressed archive; contents require manual inspection."
    else:
        return "Safe / Low Risk", "Standard document or media format."
