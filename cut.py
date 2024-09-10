#sudo apt-get install ffmpeg

import subprocess
import auto_editor
import os

# Define start time, duration, and the command to trim video
start_time = "00:00:00"  # Start at 10 seconds
duration = "10"          # Duration of 20 seconds
input_file = "video-long.mp4"
output_file = "temp.mp4"

command = [
    "ffmpeg", "-ss", start_time, "-i", input_file, "-t", duration,
    "-c", "copy", output_file
]
command2 = [
    "ffmpeg", "-i", "temp.mp4", "temp.avi"
]
command3 = [
    "ffmpeg", "-i", "temp.avi", "video.mp4"
]
'''
[
    "auto-editor", output_file, "--edit", "(or audio:0.03 motion:0.06)"
]
'''
# Execute the command
subprocess.run(command)
subprocess.run(command2)
subprocess.run(command3)
#subprocess.run(command2)
try:
    os.remove("video-long.mp4")
    os.remove("temp.mp4")
    os.remove("temp.avi")
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))