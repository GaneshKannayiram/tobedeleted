import subprocess
import threading
import os
from time import sleep

def run_command(command, cwd=None):
    """Helper to run shell commands"""
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

def main():
    print("🚀 Starting Job Recommendation System...")
    
    # 1. Generate feature engineer
    print("\n🔧 Step 1/4: Generating ML model...")
    gen_process = run_command("python backend/generate_feature_engineer.py")
    gen_process.wait()
    if gen_process.returncode != 0:
        print(f"❌ Error generating model: {gen_process.stderr.read()}")
        return
    
    # 2. Start Flask backend
    print("\n🌐 Step 2/4: Starting API server...")
    flask_thread = threading.Thread(
        target=lambda: run_command("python backend/app.py")
    )
    flask_thread.daemon = True
    flask_thread.start()
    
    # 3. Start job updater
    print("\n🔄 Step 3/4: Starting job updater...")
    updater_thread = threading.Thread(
        target=lambda: run_command("python backend/update_jobs.py")
    )
    updater_thread.daemon = True
    updater_thread.start()
    
    # 4. Start React frontend
    print("\n💻 Step 4/4: Starting web interface...")
    os.chdir("frontend")
    frontend_process = run_command("npm start", cwd="..\\frontend")
    
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all processes...")
        frontend_process.terminate()

if __name__ == "__main__":
    main()