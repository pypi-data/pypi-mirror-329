import sys
import os
import argparse
from PIL import Image, ImageFilter, ImageEnhance


def thumbnail(input_path, final_width, final_height, blur_radius=10):

    img = Image.open(input_path)
    
    orig_w, orig_h = img.size
    scale = max(final_width / orig_w, final_height / orig_h)
    bg_width = int(orig_w * scale)
    bg_height = int(orig_h * scale)
    
    bg = img.resize((bg_width, bg_height), Image.LANCZOS)
    crop_x = (bg_width - final_width) // 2
    crop_y = (bg_height - final_height) // 2
    bg = bg.crop((crop_x, crop_y, crop_x + final_width, crop_y + final_height))


    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))


    fg = img.copy()
    fg.thumbnail((final_width, final_height), Image.LANCZOS)
    

    final_img = bg.copy()
    paste_x = (final_width - fg.width) // 2
    paste_y = (final_height - fg.height) // 2
    final_img.paste(fg, (paste_x, paste_y))
    
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}-thumbnail{ext}"

    final_img.save(output_path)
    print(f"Image saved as {output_path}")
    
    return final_img



def adapt_aspect_ratio(input_path: str, target_aspect: float, blur_radius: float = 10):

    cover_path = input_path

    # Deduce extension without dot.
    cov_ext = os.path.splitext(cover_path)[1][1:]

    # Retrieve image dimensions.
    with Image.open(cover_path) as img:
        width, height = img.size


    print(f"Original Dimensions: {width} x {height}")

    current_ratio = width / height

    # Round current ratio if target is non-square.
    #ratio = current_ratio if target_aspect == 1 else round(current_ratio, 4)
    ratio = current_ratio
    is_ratio_right = (ratio == target_aspect)

    print(f"Current Ratio: {ratio} (Target: {target_aspect})")
    print(f"Correct aspect ratio: {is_ratio_right}")

    if not is_ratio_right:
        # Adjust dimensions.
        if target_aspect == 1:
            # For square covers: set the larger dimension equal to the smaller one.
            if current_ratio > 1:
                width = height
            else:
                height = width
        else:
            # Always adjust based on the smallest
            if current_ratio < 1:
                height = width

            width = height * target_aspect

        resize_width = int(width)
        resize_height = int(height)
        print(f"Resizing to: {resize_width} x {resize_height}")

        # Resize and apply blur and brightness effect.
        thumbnail(cover_path, resize_width, resize_height, blur_radius)

    else:
        print("Cover image already has the target aspect ratio. No changes made.")


def main():

    parser = argparse.ArgumentParser(
        description="Image Resizing Module: Choose dimensions dimensions or adapt to a target aspect ratio."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True, help="Mode of operation")

    dimensions_parser = subparsers.add_parser("dimensions", help="Resize an image to dimensions")
    dimensions_parser.add_argument("input_path", help="Input image file path")
    dimensions_parser.add_argument("width", type=int, help="Final width in pixels")
    dimensions_parser.add_argument("height", type=int, help="Final height in pixels")
    dimensions_parser.add_argument("--blur", type=float, default=10, help="Gaussian blur radius (default: 10)")

    aspect_parser = subparsers.add_parser("aspect", help="Adapt a cover image to a target aspect ratio with blur effect")
    aspect_parser.add_argument("input_path", help="Input image file path")
    aspect_parser.add_argument("target_aspect", type=float, help="Target aspect ratio (e.g., 1 or 1.78)")
    aspect_parser.add_argument("--blur", type=float, default=10, help="Gaussian blur radius (default: 10)")

    args = parser.parse_args()

    if args.mode == "dimensions":
        thumbnail(
            input_path=args.input_path,
            final_width=args.width,
            final_height=args.height,
            blur_radius=args.blur,
        )

    elif args.mode == "aspect":
        adapt_aspect_ratio(
            input_path=args.input_path,
            target_aspect=args.target_aspect,
            blur_radius=args.blur,
        )



if __name__ == '__main__':
    main()
