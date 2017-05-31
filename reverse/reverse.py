import subprocess
import argparse

parser = argparse.ArgumentParser(prog='Reverse', description='Call adb reverse tcp:8081 tcp:8081')
#args = parser.parse_args()

subprocess.call(["adb", "reverse", "tcp:8081", "tcp:8081"]);
print 'done'
