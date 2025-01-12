from PIL import Image, ImageSequence

# Open the GIF
gif = Image.open("lol.gif")

# Frame counter
frame_number = 0

# Process each frame
for frame in ImageSequence.Iterator(gif):
    frame = frame.resize((128, 160)).convert("RGB")
    with open(f"frame{frame_number}.raw", "wb") as f:
        for pixel in frame.getdata():
            r, g, b = pixel
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            f.write(rgb565.to_bytes(2, "big"))
    frame_number += 1

print(f"{frame_number} frames processed.")
