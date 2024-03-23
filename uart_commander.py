import cv2
import numpy as np
import serial
import RPi.GPIO as GPIO
# Global variables for threshold box and previous ball position
threshold_x = 200  # Threshold box x-coordinate
threshold_y = 200  # Threshold box y-coordinate
threshold_width = 200  # Threshold box width
threshold_height = 200  # Threshold box height
prev_ball_x = None   # Previous ball x-coordinate
prev_ball_y = None   # Previous ball y-coordinate

is_inside = False

# Function to detect and track the ball
def track_ball(frame, uart):
    global threshold_x, threshold_y, threshold_width, threshold_height, prev_ball_x, prev_ball_y

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([30,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a rectangle for the threshold box
    cv2.rectangle(frame, (threshold_x, threshold_y),
                  (threshold_x + threshold_width, threshold_y + threshold_height),
                  (0, 255, 0), 2)

    # Draw a rectangle around the detected ball
    if len(contours) > 0:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(max_contour)
        # Draw the bounding box on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Calculate the center of the bounding box
        ball_x = x + w / 2
        ball_y = y + h / 2

        # Check if the ball is outside the threshold box
        if (x < threshold_x or x + w > threshold_x + threshold_width or
            y < threshold_y or y + h > threshold_y + threshold_height):
            print("Ball is outside the threshold box!")
            is_inside = False
        else:
            print("Ball is inside the threshold box! Stop the rover.")
            is_inside = True
            # Transmit and receive bytes using UART
            uart.write(b'Transmitting data')
            received_data = uart.read(10)
            print("Received data:", received_data)

        # Determine the direction of the ball with respect to the bounding box
        direction = "stop"
        if prev_ball_x is not None and prev_ball_y is not None:
            if ball_x < threshold_x + threshold_width / 2:
                direction = "left"
                # Transmit bytes for left direction
                uart.write(b'Left')
            elif ball_x > threshold_x + threshold_width / 2:
                direction = "right"
                # Transmit bytes for right direction
                uart.write(b'Right')
        prev_ball_x = ball_x
        prev_ball_y = ball_y

        # Print the direction
        if not is_inside:
            print(direction)

    return frame

# Main function
def main():
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    uart_pin1 = 17  # Example UART pin 1
    uart_pin2 = 18  # Example UART pin 2
    GPIO.setup(uart_pin1, GPIO.OUT)
    GPIO.setup(uart_pin2, GPIO.OUT)

    # Open the UART connection
    uart = serial.Serial('/dev/ttyAMA0', 9600)  # Replace with your UART configuration

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Track the ball
        tracked_frame = track_ball(frame, uart)

        # Display the resulting frame
        cv2.imshow('Ball Tracking', tracked_frame)

        # Check for 'q' key pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture, close UART, and clean up GPIO
    cap.release()
    uart.close()
    cv2.destroyAllWindows()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
