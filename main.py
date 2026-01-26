import os, subprocess, tempfile, json, re, shutil
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from validators import VALIDATORS

app = FastAPI()

# Load tasks from JSON
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return {task["id"]: task for task in data["tasks"]}
    return {}

TASKS = load_tasks()

def extract_octave_function_name(code):
    """Extract function name from Octave code if it's a function definition."""
    match = re.search(r'function\s+(?:\w+\s*=\s*)?(\w+)\s*\(', code)
    return match.group(1) if match else None

class Submission(BaseModel):
    task_id: int
    code: str
    language: str

@app.post("/run")
async def run_task(sub: Submission):
    suffix = ".py" if sub.language == "python" else ".m"
    test_appendix = VALIDATORS.get(sub.task_id, {}).get(sub.language, "")
    
    # Prefix for Python to use non-interactive backend
    prefix = "import matplotlib\nmatplotlib.use('Agg')\nimport sys\n" if sub.language == "python" else ""
    
    # Always make the code available as a variable for validators that need it (e.g., Task 9)
    if sub.language == "python":
        code_var = f"\ncode = \"\"\"{sub.code}\"\"\"\n"
    else:
        # Octave string syntax (escape quotes)
        escaped_code = sub.code.replace("'", "''").replace("\n", "\\n")
        code_var = f"\ncode = '{escaped_code}';\n"
    
    env_code = prefix + sub.code + code_var + test_appendix

    tmp_dir = None
    tmp_path = None
    asset_files = []

    try:
        # Get task info to check for assets
        task_info = TASKS.get(sub.task_id, {})
        asset_text = task_info.get("asset_text")
        asset_filename = task_info.get("asset_filename")
        
        if sub.language == "python":
            # Python: create temp directory for asset files if needed
            if asset_text and asset_filename:
                tmp_dir = tempfile.mkdtemp()
                asset_path = os.path.join(tmp_dir, asset_filename)
                with open(asset_path, 'w') as f:
                    f.write(asset_text)
                asset_files.append(asset_path)
                # Write main script to same directory
                script_path = os.path.join(tmp_dir, "script.py")
                with open(script_path, 'w') as f:
                    f.write(env_code)
                tmp_path = script_path
                cmd = ["python3", "script.py"]
                cwd = tmp_dir
            else:
                # No assets, use simple temporary file
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, dir=".") as tmp:
                    tmp.write(env_code.encode())
                    tmp_path = tmp.name
                cmd = ["python3", tmp_path]
                cwd = None
        else:
            # Octave: create temp directory with correctly named file
            if not tmp_dir:
                tmp_dir = tempfile.mkdtemp()
            
            # Create asset file if needed
            if asset_text and asset_filename:
                asset_path = os.path.join(tmp_dir, asset_filename)
                with open(asset_path, 'w') as f:
                    f.write(asset_text)
                asset_files.append(asset_path)
            
            function_name = extract_octave_function_name(sub.code)
            
            if function_name:
                # Function file: write only the function definition
                func_filename = f"{function_name}.m"
                func_path = os.path.join(tmp_dir, func_filename)
                with open(func_path, 'w') as f:
                    # Ensure function code ends with newline for proper parsing
                    func_code = sub.code.rstrip() + '\n'
                    f.write(func_code)
                
                # Test script: Octave automatically finds functions in current directory
                # Use 'run_test.m' to avoid conflict with Octave's built-in 'test' function
                test_filename = "run_test.m"
                test_path = os.path.join(tmp_dir, test_filename)
                with open(test_path, 'w') as f:
                    # Write code variable (available for validators that need it)
                    f.write(code_var)
                    # Write the validation code (Octave will auto-load the function file)
                    f.write(test_appendix)
                
                cmd = ["octave", "--quiet", "--no-gui", test_filename]
                tmp_path = test_path
            else:
                # Script-based code: write everything to one file
                filename = "script.m"
                tmp_path = os.path.join(tmp_dir, filename)
                with open(tmp_path, 'w') as f:
                    f.write(env_code)
                cmd = ["octave", "--quiet", "--no-gui", filename]
            
            cwd = tmp_dir
            
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10, cwd=cwd)
        
        if proc.returncode == 0:
            return {"status": "success", "message": "✅ Validation Passed!", "output": proc.stdout}
        else:
            # Include both stderr and stdout in case of failures
            error_details = proc.stderr if proc.stderr else proc.stdout
            return {"status": "error", "message": "❌ Validation Failed", "details": error_details}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "❌ Execution Timed Out", "details": "Code took too long to run."}
    except Exception as e:
        return {"status": "error", "message": "❌ Server Error", "details": str(e)}
    finally:
        # Cleanup
        if tmp_dir and os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        elif tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/tasks")
async def get_tasks():
    return {"tasks": list(TASKS.values())}

@app.get("/", response_class=HTMLResponse)
async def home():
    if os.path.exists("index.html"):
        with open("index.html") as f: 
            return f.read()
    return "index.html not found"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
