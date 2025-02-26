import sys
import os
from PIL import Image, ImageFilter, ImageEnhance

def thumbnail(input_path, final_width, final_height, blur_radius=50):

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

def main():

    if len(sys.argv) < 4:
        print("Usage: python your_module.py <input_image> <final_width> <final_height> [blur_radius]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    final_width = int(sys.argv[2])
    final_height = int(sys.argv[3])
    blur_radius = float(sys.argv[4]) if len(sys.argv) > 4 else 20
    
    thumbnail(input_path, final_width, final_height, blur_radius)

if __name__ == '__main__':
    main()
