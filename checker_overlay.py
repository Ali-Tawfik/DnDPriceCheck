import tkinter as tk
from multiprocessing import Process, Queue
import time

# Overlay function
def create_overlay(queue):
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size and position (top-right corner)
    window_width = 500  # Width of the overlay window
    window_height = 300  # Height of the overlay window
    x_position = screen_width - window_width  # X position for top-right
    y_position = 0  # Y position for top-right
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Make the window transparent
    root.attributes("-topmost", True)  # Keep the window on top
    root.attributes("-transparentcolor", "black")  # Make the background transparent
    root.configure(bg="black")  # Set the background color to black (will be transparent)

    # Create a label with white text and black background
    label = tk.Label(root, text="", font=("Arial", 12), bg="black", fg="white")
    label.pack()

    # Track the current after() ID for clearing scheduled tasks
    clear_event_id = None

    def update_overlay():
        nonlocal clear_event_id

        if not queue.empty():
            # Get the latest text and duration from the queue
            text, duration = queue.get()
            
            # Cancel any pending text-clearing event
            if clear_event_id is not None:
                root.after_cancel(clear_event_id)

            # Update text and schedule clearing after the specified duration
            label.config(text=text)
            clear_event_id = root.after(int(duration * 1000), clear_text)

        root.after(100, update_overlay)  # Check for updates every 100ms

    def clear_text():
        nonlocal clear_event_id
        label.config(text="")
        clear_event_id = None

    root.after(100, update_overlay)
    root.mainloop()

# Function to start the overlay in a separate process
def start_overlay(queue):
    overlay_process = Process(target=create_overlay, args=(queue,))
    overlay_process.start()
    return overlay_process

# Function to show text for a certain amount of time
def show_text(queue, text, duration):
    queue.put((text, duration))  # Send text and duration to the overlay

# Example usage
if __name__ == "__main__":
    queue = Queue()
    overlay_process = start_overlay(queue)

    # Show text for 10 seconds, then overwrite it after 3 seconds
    show_text(queue, "Hello, World!", 10)
    time.sleep(3)
    show_text(queue, "New Text Overwrites!", 5)

    time.sleep(6)  # Wait to see the second text disappear

    # Terminate the overlay process
    overlay_process.terminate()
