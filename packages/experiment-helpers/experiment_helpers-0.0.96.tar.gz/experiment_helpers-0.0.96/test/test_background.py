from PIL import Image
import os
import sys
sys.path.append('/home/jlb638/Desktop/package')

from src.experiment_helpers.background import remove_background

def concatenate_images(images, direction='horizontal'):
    # Determine the width and height of the final image
    if direction == 'horizontal':
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)
        new_image = Image.new('RGB', (total_width, max_height))
        
        x_offset = 0
        for img in images:
            new_image.paste(img, (x_offset, 0))
            x_offset += img.width
    elif direction == 'vertical':
        total_height = sum(img.height for img in images)
        max_width = max(img.width for img in images)
        new_image = Image.new('RGB', (max_width, total_height))
        
        y_offset = 0
        for img in images:
            new_image.paste(img, (0, y_offset))
            y_offset += img.height
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'")
    
    return new_image


src=Image.open("ArcaneJinx.jpg")
images=[src]
for model_name in  ["u2net", "u2net_human_seg", "u2netp"]:
    dest=remove_background(src,model_name=model_name)
    images.append(dest)
cat=concatenate_images(images)
cat.save("removed.png")