# Real-Time Face Detection Task



This is a high-performance face detection system I built using Python. The goal was to create an application that could accurately detect multiple faces from a live webcam feed in real-time, with a clean and visually appealing interface.

###  Task Demo

![Demo GIF of the face detector in action](https://image2url.com/images/1759169437958-8d371558-1c37-4ef2-81a9-f03c3c5544ea.png)


---

## How It Works

The entire application is built on a simple but powerful pipeline. I chose **OpenCV** to handle all the camera interactions and drawing, and **Google's MediaPipe** for its incredibly fast and lightweight face detection model.

The core logic follows these steps for every single frame from the webcam:

1.  **Capture the Frame**: First, OpenCV grabs a new frame from the webcam. I flipped the image horizontally so it acts like a mirror.

2.  **Color Conversion**: MediaPipe requires images in RGB format, but OpenCV captures them in BGR. A crucial step was to convert the color space of the frame from `BGR` to `RGB` before processing.

3.  **Run Detection**: The RGB frame is then passed to the initialized MediaPipe `FaceDetection` model. This model scans the image and returns a list of all the faces it found.

4.  **Extract Data**: For each face detected, the model provides two key pieces of information:
    * **A Bounding Box**: The `(x, y, width, height)` coordinates that define the location of the face.
    * **A Confidence Score**: A percentage value indicating how certain the model is that it has found a face.

5.  **Visualize the Results**: This is where I added my custom touch. Instead of just drawing a plain rectangle, I wrote a `draw_stylish_bbox` function. This function takes the bounding box data and:
    * Draws a thin main rectangle.
    * Adds thicker lines at the corners to give it a more professional, "scanner" look.
    * Displays the confidence score in a clean, filled-in label above the box.

6.  **Display Final Info**: Finally, I added a semi-transparent overlay in the corner to display real-time stats like the **current FPS** and the **total number of faces detected**. The frame is then displayed on the screen.

---

## Core Features I Implemented

* **Efficient Real-Time Detection**: The core of the project is a `while` loop that processes the webcam feed frame by frame for smooth, live detection.
* **Multi-Face Capability**: The code is built to handle multiple faces in the frame at once, iterating through each detection provided by MediaPipe.
* **Custom Bounding Box UI**: I designed and implemented a unique drawing function to create a more stylish and readable bounding box than the default offered by many libraries.
* **Dynamic Color Assignment**: To make it easier to distinguish between different people, the bounding box for each detected face is assigned a different color from a predefined list.
* **Performance & Stats Overlay**: I implemented logic to calculate the FPS and display it along with the face count, which helps in understanding the real-time performance of the application.

---

##  Tech Stack

* **Language**: Python
* **Libraries**:
    * **OpenCV**: For video capture, image manipulation, and all drawing operations.
    * **MediaPipe**: For the high-performance, machine learning-based face detection.
