"""
CLEAN CROPPER - Deletes old extracted_data first
"""

import os
import zipfile
import shutil
from PIL import Image
from pathlib import Path
import hashlib
from datetime import datetime

class CleanCropper:
    def __init__(self, zip_path, output_folder="cropped_clean"):
        self.zip_path = zip_path
        self.base_output = output_folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_folder = os.path.join(output_folder, f"crops_{timestamp}")
        self.extract_folder = "extracted_data"
        self.seen_hashes = set()
        
    def clean_old_data(self):
        """DELETE old extracted_data folder completely"""
        if os.path.exists(self.extract_folder):
            print(f"🗑️  Deleting old extracted_data folder...")
            shutil.rmtree(self.extract_folder)
            print(f"   ✓ Cleaned up old data\n")
        
    def extract_zip(self):
        """Extract zip"""
        if not os.path.exists(self.zip_path):
            print(f"❌ ERROR: Zip file not found: {self.zip_path}")
            print(f"   Looking for: {os.path.abspath(self.zip_path)}")
            return False
        
        print(f"📦 Extracting: {self.zip_path}")
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_folder)
        print(f"✓ Extracted to: {self.extract_folder}\n")
        return True
        
    def get_image_hash(self, img):
        return hashlib.md5(img.tobytes()).hexdigest()
        
    def polygon_to_bbox(self, polygon_coords, img_width, img_height):
        """Convert polygon to bbox"""
        x_coords = [coord[0] * img_width for coord in polygon_coords]
        y_coords = [coord[1] * img_height for coord in polygon_coords]
        
        x1 = int(min(x_coords))
        y1 = int(min(y_coords))
        x2 = int(max(x_coords))
        y2 = int(max(y_coords))
        
        return (x1, y1, x2, y2)
    
    def parse_polygon_file(self, txt_path):
        """Parse - ONE LINE = ONE OBJECT"""
        objects = []
        
        with open(txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                
                if len(parts) < 3:
                    continue
                
                try:
                    class_id = int(parts[0])
                except:
                    continue
                
                coords = []
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        try:
                            x = float(parts[i])
                            y = float(parts[i + 1])
                            coords.append((x, y))
                        except:
                            continue
                
                if coords:
                    objects.append({
                        'class_id': class_id,
                        'coords': coords
                    })
        
        return objects
    
    def find_folders(self):
        """Find images and labels"""
        images_path = None
        labels_path = None
        
        for root, dirs, files in os.walk(self.extract_folder):
            if 'images' in dirs or 'image' in dirs:
                img_folder = 'images' if 'images' in dirs else 'image'
                images_path = os.path.join(root, img_folder)
                
            if 'labels' in dirs or 'label' in dirs:
                lbl_folder = 'labels' if 'labels' in dirs else 'label'
                labels_path = os.path.join(root, lbl_folder)
                
            if images_path and labels_path:
                break
        
        return images_path, labels_path
    
    def process(self):
        """Main processing"""
        print("="*70)
        print("CLEAN CROPPER - FRESH START")
        print("="*70 + "\n")
        
        # STEP 1: Delete old extracted data
        self.clean_old_data()
        
        # STEP 2: Extract fresh
        if not self.extract_zip():
            return
        
        # STEP 3: Find folders
        images_path, labels_path = self.find_folders()
        
        if not images_path or not labels_path:
            print("❌ Could not find images/labels folders")
            return
        
        print(f"📂 Found:")
        print(f"   Images: {images_path}")
        print(f"   Labels: {labels_path}")
        
        # Check what's actually in there
        image_files = [f for f in os.listdir(images_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        print(f"\n📊 Dataset info:")
        print(f"   Total images: {len(image_files)}")
        
        if image_files:
            print(f"   First image: {image_files[0]}")
            print(f"   Last image: {image_files[-1]}")
        
        # Create output folder (with timestamp inside base folder)
        os.makedirs(self.output_folder, exist_ok=True)
        print(f"   ✓ Output: {self.output_folder}\n")
        
        input(f"Press ENTER to continue cropping {len(image_files)} images...")
        print()
        
        saved_count = 0
        skipped_duplicate = 0
        
        for img_idx, img_file in enumerate(image_files, 1):
            img_path = os.path.join(images_path, img_file)
            img_name = Path(img_file).stem
            label_file = img_name + '.txt'
            label_path = os.path.join(labels_path, label_file)
            
            if not os.path.exists(label_path):
                continue
            
            # Parse
            objects = self.parse_polygon_file(label_path)
            
            if not objects:
                continue
            
            # Open image
            try:
                img = Image.open(img_path)
                img_width, img_height = img.size
                
                crops_this_image = 0
                
                # Process each object
                for idx, obj in enumerate(objects):
                    x1, y1, x2, y2 = self.polygon_to_bbox(obj['coords'], img_width, img_height)
                    
                    # Clip
                    x1 = max(0, min(x1, img_width))
                    y1 = max(0, min(y1, img_height))
                    x2 = max(0, min(x2, img_width))
                    y2 = max(0, min(y2, img_height))
                    
                    if x2 <= x1 or y2 <= y1:
                        continue
                    
                    # Crop
                    cropped = img.crop((x1, y1, x2, y2))
                    
                    # Check duplicate
                    img_hash = self.get_image_hash(cropped)
                    if img_hash in self.seen_hashes:
                        skipped_duplicate += 1
                        continue
                    
                    self.seen_hashes.add(img_hash)
                    
                    # Save
                    crop_name = f"{img_name}_class{obj['class_id']}_obj{idx+1}.jpg"
                    crop_path = os.path.join(self.output_folder, crop_name)
                    cropped.save(crop_path, quality=95)
                    
                    saved_count += 1
                    crops_this_image += 1
                
                if crops_this_image > 0:
                    print(f"✓ [{img_idx}/{len(image_files)}] {img_file[:50]}: {crops_this_image} crops")
                    
            except Exception as e:
                print(f"✗ Error: {img_file}: {e}")
        
        print(f"\n{'='*70}")
        print(f"✅ COMPLETED!")
        print(f"   Crops saved: {saved_count}")
        print(f"   Duplicates skipped: {skipped_duplicate}")
        print(f"   Output: {self.output_folder}")
        print(f"{'='*70}")


if __name__ == "__main__":
    # ========== CONFIGURATION ==========
    ZIP_FILE = "inputfile.zip"  # PUT YOUR ZIP FILE PATH HERE
    OUTPUT_FOLDER = "outputfolderpath"         # Output folder name
    # ===================================
    
    cropper = CleanCropper(ZIP_FILE, OUTPUT_FOLDER)
    cropper.process()
