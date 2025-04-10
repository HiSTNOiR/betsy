# tests/test_logging.py
import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.logging import get_logger
import time

# Test basic logging
logger = get_logger("test")
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Test log rotation by writing a larger amount of data
print("Testing log rotation by writing some larger data...")
for i in range(1000):
    logger.info(f"Log rotation test message #{i} with some padding to make it larger: {'X' * 500}")

# Check log file existence
log_path = os.path.join("logs", "test.log")
if os.path.exists(log_path):
    print(f"Log file created successfully at: {log_path}")
    print(f"Log file size: {os.path.getsize(log_path) / 1024:.2f} KB")
    
    # Check for rotation (backup files)
    backup_files = [f for f in os.listdir("logs") if f.startswith("test.log.")]
    if backup_files:
        print(f"Log rotation working! Backup files created: {len(backup_files)}")
        for bf in backup_files:
            print(f" - {bf} ({os.path.getsize(os.path.join('logs', bf)) / 1024:.2f} KB)")
    else:
        print("No backup files created yet - might need larger test data for rotation")
else:
    print(f"ERROR: Log file not found at expected location: {log_path}")

print("Logging test complete!")