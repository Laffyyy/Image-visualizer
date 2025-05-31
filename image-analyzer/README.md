# Image Analyzer

## Overview
The Image Analyzer is a Python application that allows users to analyze images by selecting colors and finding similar colors within the image. The application features a user-friendly interface that supports drag-and-drop functionality for easy image loading.

## Project Structure
```
image-analyzer
├── src
│   ├── main.py                # Entry point of the application
│   ├── utils
│   │   └── image_loader.py    # Loads images from specified paths
│   ├── analyzer
│   │   ├── color_selector.py   # Allows users to select colors from images
│   │   └── color_analyzer.py   # Analyzes images for similar colors
│   └── ui
│       ├── app.py             # Main application for the user interface
│       └── drag_and_drop.py    # Handles drag-and-drop events for images
├── requirements.txt            # Lists project dependencies
└── README.md                   # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd image-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
   or for the UI version:
   ```
   python src/ui/app.py
   ```
2. Drag and drop an image file onto the application window to load it.
3. Select a color from the image to analyze.
4. The application will display similar colors found in the image.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.