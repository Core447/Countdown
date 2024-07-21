from PIL import Image, ImageDraw

def create_progress_ring(percentage: float, size=(200, 200), bg_color=(255, 255, 255, 0), ring_color=(0, 128, 0, 255), ring_thickness=20):
    """
    Creates a progress ring image.
    
    :param percentage: The progress percentage (0 to 100).
    :param size: Tuple representing the size of the image (width, height).
    :param bg_color: Background color (RGBA).
    :param ring_color: Ring color (RGBA).
    :param ring_thickness: Thickness of the ring.
    :return: A PIL Image object representing the progress ring.
    """
    # Create a blank image with a transparent background
    image = Image.new('RGBA', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Calculate the end angle for the progress arc
    end_angle = (1 - percentage) * 360
    
    # Define the bounding box for the outer edge of the ring
    outer_bbox = [ring_thickness // 2, ring_thickness // 2, size[0] - ring_thickness // 2, size[1] - ring_thickness // 2]

    # Draw the progress arc
    if percentage >= 1:
        draw.ellipse(outer_bbox, fill=(0, 0, 0, 0), width=ring_thickness, outline=ring_color)
    else:
        draw.arc(outer_bbox, start=-90, end=-90 - end_angle, fill=ring_color, width=ring_thickness)
    
    return image