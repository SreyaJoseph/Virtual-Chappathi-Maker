import cv2
import numpy as np
import time
import sys

# --- Setup Constants and Variables ---
# Define the chappathi-making states
STATE_INITIAL = "initial"
STATE_KNEADING = "kneading"
STATE_ROLLING = "rolling"
STATE_COOKING = "cooking"
STATE_DONE = "done"

# Initial state and variables
current_state = STATE_INITIAL
knead_count = 0
rolling_progress = 0
dough_radius = 50
motion_detected_this_frame = False

# Motion detection parameters
MOTION_THRESHOLD = 5000  # Lower value = more sensitive motion detection
KNEAD_GESTURE_COOLDOWN = 1.0 # Time in seconds to reset after a knead gesture
rolling_motion_threshold = 10000 # Threshold for continuous motion
rolling_speed_factor = 0.005 # How fast the dough rolls out

# Chappathi properties
dough_color_initial = (195, 235, 254)  # Light yellow/beige (B, G, R)
dough_color_cooked = (100, 160, 200) # Darker beige
dough_max_radius = 120

# --- Function to draw on the video frame ---
def draw_chappathi(frame, radius, color, state):
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2

    # Draw the dough/chappathi
    cv2.circle(frame, (center_x, center_y), int(radius), color, -1)
    
    # Add a border
    cv2.circle(frame, (center_x, center_y), int(radius), (180, 180, 180), 5)

    # Special drawing for 'done' state
    if state == STATE_DONE:
        # Draw the "puffed up" center
        inner_radius = radius * 0.7
        cv2.circle(frame, (center_x, center_y), int(inner_radius), (255, 255, 255), -1)

# --- Main video processing loop ---
def main():
    global current_state, knead_count, rolling_progress, dough_radius, motion_detected_this_frame

    # Determine input source: webcam (0) or a video file
    video_source = 0
    if len(sys.argv) > 1:
        video_source = sys.argv[1]
    
    # Access the webcam or video file
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}.")
        return

    # Get the frame size and set up previous frame for motion detection
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    last_knead_time = time.time()
    last_rolling_motion_time = time.time()
    
    print("Welcome to the Virtual Chappathi Maker!")

    while True:
        ret, frame = cap.read()
        if not ret:
            # If a video file is being used, restart from the beginning
            if video_source != 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break
        
        # Flip the frame horizontally for a "mirror" effect
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # --- Motion Detection Logic ---
        motion_detected_this_frame = False
        frame_delta = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        # Find contours to get a sense of motion area
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_area = sum(cv2.contourArea(c) for c in contours)
        
        if motion_area > MOTION_THRESHOLD:
            motion_detected_this_frame = True
        
        # --- State Machine for Chappathi Making ---
        if current_state == STATE_INITIAL:
            draw_chappathi(frame, dough_radius, dough_color_initial, current_state)
            cv2.putText(frame, "Wave your hands to start!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if motion_detected_this_frame:
                current_state = STATE_KNEADING
                print("Starting to knead the dough!")
                
        elif current_state == STATE_KNEADING:
            # Display instructions and counter
            cv2.putText(frame, f"Knead count: {knead_count}/5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Make quick motions to knead!", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

            # Detect a kneading gesture (brief, intense motion)
            if motion_detected_this_frame and (time.time() - last_knead_time) > KNEAD_GESTURE_COOLDOWN:
                knead_count += 1
                dough_radius -= 3  # Visually shrink the dough slightly
                last_knead_time = time.time()
                print(f"Kneaded {knead_count} times!")

                if knead_count >= 5:
                    current_state = STATE_ROLLING
                    print("Dough is ready to be rolled!")
                    
            draw_chappathi(frame, dough_radius, dough_color_initial, current_state)

        elif current_state == STATE_ROLLING:
            # Display instructions and progress
            cv2.putText(frame, f"Rolling Progress: {int(rolling_progress)}%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Make continuous motions to roll!", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

            # Detect rolling gesture (sustained motion)
            if motion_area > rolling_motion_threshold:
                rolling_progress += rolling_speed_factor * motion_area
                dough_radius += rolling_speed_factor * motion_area
                last_rolling_motion_time = time.time()
                
                if rolling_progress >= 100:
                    rolling_progress = 100
                    dough_radius = dough_max_radius
                    current_state = STATE_COOKING
                    print("Chappathi is rolled! Cooking...")
                    
            draw_chappathi(frame, dough_radius, dough_color_initial, current_state)

        elif current_state == STATE_COOKING:
            cv2.putText(frame, "Cooking...", (w//2 - 80, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Simulate cooking time
            if 'cooking_start_time' not in locals():
                cooking_start_time = time.time()
            
            elapsed_time = time.time() - cooking_start_time
            cooking_percentage = min(elapsed_time / 3.0, 1.0) * 100 # Cook for 3 seconds
            
            # Blend colors for cooking effect
            cooked_r = int(dough_color_initial[2] + (dough_color_cooked[2] - dough_color_initial[2]) * (cooking_percentage / 100))
            cooked_g = int(dough_color_initial[1] + (dough_color_cooked[1] - dough_color_initial[1]) * (cooking_percentage / 100))
            cooked_b = int(dough_color_initial[0] + (dough_color_cooked[0] - dough_color_initial[0]) * (cooking_percentage / 100))
            
            draw_chappathi(frame, dough_radius, (cooked_b, cooked_g, cooked_r), current_state)
            
            if cooking_percentage >= 100:
                current_state = STATE_DONE
                print("Chappathi is ready!")
                
        elif current_state == STATE_DONE:
            cv2.putText(frame, "Voila! Your chappathi is ready!", (w//2 - 200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to exit.", (w//2 - 100, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            draw_chappathi(frame, dough_radius, dough_color_cooked, current_state)

        # Show the video feed
        cv2.imshow('Virtual Chappathi Maker', frame)
        
        # Update the previous frame for the next iteration
        prev_gray = gray.copy()

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up and release the webcam
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
