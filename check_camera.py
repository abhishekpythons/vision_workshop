# Description: This script asks for index and opens the webcam on that specific and displays the frames captured from the webcam.
import cv2

# Open the first webcam device
index = int(input("Enter the camera index: "))
cap = cv2.VideoCapture(index)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Unable to open webcam.")
    exit()

# Loop to continuously capture frames from the webcam
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Check for 'q' key pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam device and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
