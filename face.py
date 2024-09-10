import cv2
import os
import shutil
from face_recognize import get_mids
# Function to convert frames to video
def crop(output_folder, mid):    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video file
    cap = cv2.VideoCapture('video.mp4')
    
    frame_count = 0
    success, frame = cap.read()
    height, width, _ = frame.shape
    # Loop through the video frames
    while success:
        # Save each frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)
        img = cv2.imread(frame_filename)
        if mid[frame_count] - int((0.5625*height)/2) < 0:
            cropped_image = img[0:height, 0:mid[frame_count]+int((0.5625*height)/2)-(mid[frame_count] - int((0.5625*height)/2))]
        elif mid[frame_count] + int((0.5625*height)/2) > width:
            cropped_image = img[0:height, mid[frame_count]-int((0.5625*height)/2)+(mid[frame_count] + int((0.5625*height)/2) - width):width]
        else:
            cropped_image = img[0:height, mid[frame_count]-int((0.5625*height)/2):mid[frame_count]+int((0.5625*height)/2)]
        cv2.imwrite(frame_filename, cropped_image)
        
        # Read the next frame
        success, frame = cap.read()
        frame_count += 1
    cap.release()
    print(f"Video has been converted into {frame_count} frames.")


video_path = 'video.mp4'
output_folder = 'output_frames'
mids = get_mids(video_path)

output_folder = 'output_frames'  # Folder where the frames are stored
output_video = 'server/static/video.mp4'  # Name of the output video file
fps = 30  # Frames per second for the output video
print(len(mids))
crop(output_folder, mids)

def frames_to_video(input_folder, output_video, fps):
    # Get all the frame file names in the folder
    frames = sorted([f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    # Read the first frame to get dimensions
    frame_path = os.path.join(input_folder, frames[0])
    frame = cv2.imread(frame_path)
    height, width, _ = frame.shape
    
    
    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' or 'MJPG' for .avi
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # Write each frame to the video file
    for frame_name in frames:
        frame_path = os.path.join(input_folder, frame_name)
        frame = cv2.imread(frame_path)
        print(frame.shape)
        video.write(frame)
    
    # Release the video writer
    video.release()
    
    try:
        shutil.rmtree(output_folder)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
    print(f"Video saved as {output_video}")

# Example usage:
input_folder = 'output_frames'
output_video = 'output_video.mp4'
fps = 30  # Frames per second

frames_to_video(input_folder, output_video, fps)
