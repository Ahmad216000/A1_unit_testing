import subprocess

# List of test files
test_files = [
    "test_task3_checkout.py",
    "test_task3_checkcart.py",
    "test_task3_loadproductsfromcsv.py",
]

# Run each test file
for test_file in test_files:
    result = subprocess.run(["python", "-m", "pytest", test_file])

    # Check the return code
    if result.returncode == 0:
        print(f"Tests in {test_file} passed.")
    else:
        print(f"Tests in {test_file} failed.")
