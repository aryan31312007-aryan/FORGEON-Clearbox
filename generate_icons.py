import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_app_icon(size):
    # Create high-res image with dark futuristic background
    img = Image.new("RGBA", (size, size), (11, 15, 23, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer glow / border
    pad = int(size * 0.08)
    corner_radius = int(size * 0.22)
    
    # Draw rounded rectangle container
    rect_box = [pad, pad, size - pad, size - pad]
    
    # Draw dark card fill with border
    draw.rounded_rectangle(rect_box, radius=corner_radius, fill=(22, 27, 34, 255), outline=(0, 240, 255, 200), width=int(size * 0.025))
    
    # Draw Audio Spectrum bars inside
    cx = size // 2
    cy = size // 2
    
    bars = [0.35, 0.65, 0.9, 0.7, 1.0, 0.8, 0.5, 0.75, 0.4]
    num_bars = len(bars)
    bar_width = int(size * 0.05)
    gap = int(size * 0.03)
    total_width = num_bars * bar_width + (num_bars - 1) * gap
    start_x = cx - total_width // 2
    max_h = int(size * 0.42)
    base_y = cy + int(max_h * 0.4)
    
    for i, h_ratio in enumerate(bars):
        bx = start_x + i * (bar_width + gap)
        bh = int(max_h * h_ratio)
        by = base_y - bh
        
        # Color gradient ratio
        if i % 3 == 0:
            color = (0, 240, 255) # Cyan
        elif i % 3 == 1:
            color = (0, 255, 102) # Green
        else:
            color = (255, 176, 0) # Gold
            
        draw.rounded_rectangle([bx, by, bx + bar_width, base_y], radius=bar_width//2, fill=color)
    
    # Add central "C" or ClearBox logo text overlay
    try:
        font_size = int(size * 0.2)
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        
    draw.text((cx, base_y + int(size * 0.08)), "FORGEON CLEARBOX", fill=(230, 237, 243), font=font, anchor="mm")
    
    return img

if __name__ == "__main__":
    icon192 = create_app_icon(192)
    icon192.save("icon-192.png")
    
    icon512 = create_app_icon(512)
    icon512.save("icon-512.png")
    
    icon512.save("favicon.ico", format="ICO", sizes=[(64, 64)])
    print("App Icons generated successfully: icon-192.png, icon-512.png, favicon.ico")
