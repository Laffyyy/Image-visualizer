class ImageLoader:
    def load(self, image_path):
        from PIL import Image
        
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None