import cv2
import numpy as np

# Function to detect and track the ball
def track_ball(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([30,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('mask', mask)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a circle around the detected ball
    if len(contours) > 0:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        # Get the center and radius of the contour
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
        # Draw the circle and centroid on the frame
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), -1)

    return frame

# Main function
def main():
    # Open the webcam
    cap = cv2.VideoCapture(2)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Track the ball
        tracked_frame = track_ball(frame)

        # Display the resulting frame
        cv2.imshow('Ball Tracking', tracked_frame)

        # Check for 'q' key pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("starting")
    main()
