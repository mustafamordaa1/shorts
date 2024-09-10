import cv2
import os
import shutil
#sudo apt-get install ffmpeg libsm6 libxext6  -y

def get_mids(video_path):
    # Create the output folder if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    mids = []
    success, frame = cap.read()
    
    # Loop through the video frames
    while success:
        if frame_count % 30 == 0:
            # Save each frame as an image file
            frame_filename = os.path.join('temp', f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)

            img = cv2.imread(frame_filename)
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            face_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            face = face_classifier.detectMultiScale(
                gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
            )
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(frame_filename, img_rgb)
            
            if len(face) != 0:
                x = face[0][0]
                w = face[0][2]
                mid = int(x+(w/2))
                mids.append(mid)
            else:
                if len(mids) > 0:
                    mids.append(mids[(frame_count % 30)-1])
                else:
                    mids.append([0,0])
            
        # Read the next frame
        success, frame = cap.read()
        frame_count += 1

    cap.release()

    try:
        shutil.rmtree('temp')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    print(f"Video has been converted into {frame_count} frames.")
    crop_transition = []
    
    for i in range(frame_count//30):
        interval = mids[i] - mids[i + 1]
        if interval > 0:
            abs_interval = abs(interval)
            rounds = abs_interval
            for j in range(30):
                if rounds > 0:
                    crop_transition.append(mids[i]-(j*(max(round(abs_interval/30), 1))))
                    rounds -= max(round(abs_interval/30), 1)
                elif rounds <= 0:
                    crop_transition.append(mids[i+1])
        elif interval < 0:
            abs_interval = abs(interval)
            rounds = abs_interval
            for j in range(30):
                if rounds > 0:
                    crop_transition.append(mids[i]+(j*(max(round(abs_interval/30), 1))))
                    rounds -= max(round(abs_interval/30), 1)
                elif rounds <= 0:
                    crop_transition.append(mids[i+1])
        elif interval == 0:
            for j in range(30):
                crop_transition.append(mids[i])
    for i in range(frame_count%30):
        crop_transition.append(crop_transition[frame_count//30])
                    
    return crop_transition

# Function to crop frames 
def crop(output_folder, mid):    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video file
    cap = cv2.VideoCapture('video.mp4')
    
    frame_count = 0
    success, frame = cap.read()
    w, h, _ = frame.shape
    
    # Loop through the video frames
    while success:
        # Save each frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)
        img = cv2.imread(frame_filename)
        if mid[frame_count] - 200 < 0:
            cropped_image = img[0:h, 0:mid[frame_count]+200-(mid[frame_count] - 200)]
        else:
            cropped_image = img[0:h, mid[frame_count]-200:mid[frame_count]+200]
        cv2.imwrite(frame_filename, cropped_image)
        
        # Read the next frame
        success, frame = cap.read()
        frame_count += 1
    cap.release()
    print(f"Video has been converted into {frame_count} frames.")

