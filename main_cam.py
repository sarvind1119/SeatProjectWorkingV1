import cv2
import os
import time

# RTSP stream URL (replace with your actual RTSP URL)
rtsp_url = "rtsp://lbs:admin@10.10.2.87"

# Create a directory to store images if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create a VideoCapture object to capture video from the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Initialize a counter to keep track of captured images
img_counter = 0

# Set the time to start capturing images
start_time = time.time()

# Main loop to capture and save images
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image. Exiting...")
        break

    # Display the captured frame (optional)
    cv2.imshow('frame', frame)

    # Check if 60 seconds have passed
    if time.time() - start_time >= 60:
        img_name = f"images/img_{img_counter}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")

        # Reset the start time
        start_time = time.time()
        img_counter += 1

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
