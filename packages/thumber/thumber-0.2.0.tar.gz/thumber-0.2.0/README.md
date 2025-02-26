# Thumber

This Python script takes an image and creates a composite image with the original one centered, while the background is filled with a blurred and faded version, if dimensions or aspect ratio are altered. If it follows the same aspect ratio, but dimensions are smaller, it only downscales the image. The final output will have dimensions specified by command-line arguments.

Install using pip:

```
pip install thumber
```

## Usage

```
thumber <mode> <input_image> <final_width> <final_height> [blur_radius]
```

Examples:

To produce a 1920x1080 image:

```
thumber dimensions square.jpg 1920 1080 --blur=30
```

To produce an image whose width is 1.778x the height:

```
thumber aspect square.jpg 1.778 --blur=30
```

The closer to 0, the lower is the blur effect


## Gallery Examples


| `babel.webp` (1024x1024)| `babel-dimensions-1920x1080.webp` | `babel-aspect-0.5.webp` | `babel-aspect-2.webp`
|:----:|:----:|:-----:|:----:| 
| ![](assets/babel.webp)| ![](assets/babel-dimensions-1920x1080.webp) | ![](assets/babel-aspect-0.5.webp) | ![](assets/babel-aspect-2.webp)


## License 

This project is licensed under the MIT License.