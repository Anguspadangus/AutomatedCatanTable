import cv2

# Callback function to get mouse coordinates
def get_mouse_coords(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print("Mouse coordinates (x, y):", x, y)

# Load the image
image = cv2.imread('src\\integration_test\\images\\image_training\\robber1_1_filter.jpg')

# Create a window to display the image
cv2.namedWindow('Image')

# Set the mouse callback function
cv2.setMouseCallback('Image', get_mouse_coords)

# Display the image
cv2.imshow('Image', image)

# Wait for the user to press any key to exit
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()