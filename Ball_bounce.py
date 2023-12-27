#Ball Bounce code
import cv2
import numpy as np

# Define the video file path
video_path = 'my-clip.mp4'

# Define the video capture object
video_capture = cv2.VideoCapture(video_path)

# Read the first frame from the video
ret, frame = video_capture.read()

# Select a region of interest (ROI) to track
bbox = cv2.selectROI("Object Tracking", frame, False)

# Initialize the tracker
roi = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Set termination criteria for the tracker
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    # Read a new frame from the video
    ret, frame = video_capture.read()

    if not ret:
        break

    # Convert the frame to HSV color space
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate the back projection of the frame
    frame_backproj = cv2.calcBackProject([frame_hsv], [0, 1], roi_hist, [0, 180, 0, 256], 1)

    # Apply CAMShift to get the new bounding box
    ret, bbox = cv2.CamShift(frame_backproj, bbox, term_crit)

    # Draw the new bounding box on the frame
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Object Tracking", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
video_capture.release()
cv2.destroyAllWindows()


#sdnfsdlkfnlksdnflksdnflsndfklsdfnslkdnfsndflksdnflksdnflksdnflksdnflksdnflksdnflksdnflksdnflksdnflksdn