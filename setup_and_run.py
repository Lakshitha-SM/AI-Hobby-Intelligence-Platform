#!/usr/bin/env python
"""
Comprehensive setup and execution script for AI Hobby Intelligence Platform
Handles all dependency installation and platform launch
"""
import subprocess
import sys
import os
import platform

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    if description:
        print(f"\n▶ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def main():
    print_header("AI HOBBY INTELLIGENCE PLATFORM - SETUP & LAUNCH")
    
    # Step 0: Verify Python version
    print("\n[STEP 0] Verifying Python environment...")
    py_version = platform.python_version()
    print(f"  Python version: {py_version}")
    if sys.version_info < (3, 8):
        print(f"  ✗ Error: Python 3.8+ required, but found {py_version}")
        sys.exit(1)
    print(f"  ✓ Python version acceptable")
    
    # Step 1: Create/Fix requirements.txt
    print("\n[STEP 1] Fixing requirements.txt...")
    requirements = """pandas>=2.0.0
sentence-transformers>=2.2.0
chromadb>=0.4.0
google-generativeai>=0.3.0
rich>=13.0.0
python-dotenv>=1.0.0
"""
    try:
        with open("requirements.txt", "w") as f:
            f.write(requirements)
        print("  ✓ requirements.txt created/updated")
    except Exception as e:
        print(f"  ✗ Failed to write requirements.txt: {e}")
        sys.exit(1)
    
    # Step 2: Install dependencies
    print("\n[STEP 2] Installing dependencies...")
    print("  (This may take several minutes on first run, especially sentence-transformers)")
    
    packages = [
        ("pandas>=2.0.0", "Pandas Data Processing"),
        ("sentence-transformers>=2.2.0", "Sentence Transformers Embeddings"),
        ("chromadb>=0.4.0", "ChromaDB Vector Database"),
        ("google-generativeai>=0.3.0", "Google Generative AI (Gemini)"),
        ("rich>=13.0.0", "Rich CLI Library"),
        ("python-dotenv>=1.0.0", "Python Dotenv"),
    ]
    
    failed_packages = []
    for package, name in packages:
        success, output = run_command(
            f"{sys.executable} -m pip install -q {package}",
            f"Installing {name}"
        )
        if success:
            print(f"    ✓ {name}")
        else:
            print(f"    ⚠ {name} - Warning: {output[:50]}")
            failed_packages.append(name)
    
    if failed_packages:
        print(f"\n  ⚠ Warning: Some packages may not have installed correctly: {', '.join(failed_packages)}")
        print("  The platform may still work if core dependencies are installed.")
    else:
        print("\n  ✓ All dependencies installed successfully!")
    
    # Step 3: Run tests
    print("\n[STEP 3] Running platform diagnostics...")
    success, output = run_command(f"{sys.executable} test_all.py", "Running diagnostic tests")
    
    if success:
        print("\n" + output)
    else:
        print(f"\n  ⚠ Some tests may have issues, but continuing...")
        print(output[:200])
    
    # Step 4: Launch the platform
    print_header("LAUNCHING AI HOBBY INTELLIGENCE PLATFORM")
    print("\n  Starting interactive CLI...")
    print("  Press Ctrl+C to exit at any time\n")
    
    try:
        os.system(f"{sys.executable} main.py")
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Platform interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Failed to launch platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        sys.exit(1)
