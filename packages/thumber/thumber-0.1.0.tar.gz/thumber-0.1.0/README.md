# Thumber

This Python script takes an image and creates a composite image with the original one centered, while the background is filled with a blurred and faded version, if dimensions or aspect ratio are altered. If it follows the same aspect ratio, but dimensions are smaller, it only downscales the image. The final output will have dimensions specified by command-line arguments.

Install using pip:

```
pip install thumber
```

## Usage

```
thumber <input_image> <final_width> <final_height> [blur_radius]
```

Example:

```
thumber square.jpg 1920 1080 30
```

The closer to 0, the lower is the blur effect

## License 

This project is licensed under the MIT License.