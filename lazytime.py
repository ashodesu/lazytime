import time
import ctypes
import threading
import ctypes


# Load necessary system libraries
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def move_mouse(x, y):
    global controller
    """
    Move the mouse to the specified coordinate position.
    
    Parameters:
    x (int): Target X coordinate
    y (int): Target Y coordinate
    """
    # Move the mouse to the specified coordinate position
    user32.SetCursorPos(x, y)

def mouse_click(x=None, y=None, clicks=1, button='left'):
    """
    Perform mouse click at the specified position.
    
    Parameters:
    x (int, optional): X coordinate for the click. If not specified, click at the current position.
    y (int, optional): Y coordinate for the click. If not specified, click at the current position.
    clicks (int): Number of clicks, default is 1.
    button (str): Mouse button to use, can be 'left', 'right', or 'middle', default is 'left'.
    """
    if x is not None and y is not None:
        move_mouse(x, y)
    
    button_map = {
        'left': 0x0002,  # MOUSEEVENTF_LEFTDOWN
        'right': 0x0008,  # MOUSEEVENTF_RIGHTDOWN
        'middle': 0x0020  # MOUSEEVENTF_MIDDLEDOWN
    }
    button_up_map = {
        'left': 0x0004,  # MOUSEEVENTF_LEFTUP
        'right': 0x0010,  # MOUSEEVENTF_RIGHTUP
        'middle': 0x0040  # MOUSEEVENTF_MIDDLEUP
    }
    
    for _ in range(clicks):
        user32.mouse_event(button_map[button], 0, 0, 0, 0)
        user32.mouse_event(button_up_map[button], 0, 0, 0, 0)
        time.sleep(0.1)

def mouse_drag(start_x, start_y, end_x, end_y, duration=0.5,press_left=False):
    """
    Perform mouse drag operation.
    
    Parameters:
    start_x (int): Starting X coordinate
    start_y (int): Starting Y coordinate
    end_x (int): Ending X coordinate
    end_y (int): Ending Y coordinate
    duration (float): Duration of the drag operation (seconds), default is 0.5 seconds
    """
    move_mouse(start_x, start_y)
    if press_left:
        user32.mouse_event(0x0002, 0, 0, 0, 0)  # Press left button
    
    steps = int(duration * 10)
    for i in range(1, steps + 1):
        x = start_x + (end_x - start_x) * i // steps
        controller = not check_key_press()
        y = start_y + (end_y - start_y) * i // steps
        move_mouse(x, y)
        time.sleep(duration / steps)
        controller = not check_key_press()
    
    if press_left:
        user32.mouse_event(0x0004, 0, 0, 0, 0)  # Release left button

def check_key_press():
    for i in range(256):
        if user32.GetAsyncKeyState(i) & 0x8000:
            return True
    return False

def thread_mouse_drag():
        mouse_drag(100, 100, 101, 101, duration=5)
        mouse_drag(101, 101, 100, 100, duration=5)

if __name__ == "__main__":
    controller = True
    
    print("Hold any key to stop the program...")

    

    # Create a thread to execute mouse_drag
    drag_thread = threading.Thread(target=thread_mouse_drag)
    
    # Start the thread
    drag_thread.start()
    
    while controller:
        controller = not check_key_press()
    
    # Attempt to terminate the thread
    if drag_thread.is_alive():
        print("Attempting to terminate mouse_drag operation...")
       
        drag_thread.join()

        while True:
            if drag_thread.is_alive():
                print("Unable to gracefully terminate the thread, the program may need to be forcibly exited")
                time.sleep(1)
            else:
                print("Mouse_drag operation has been successfully terminated")
                break