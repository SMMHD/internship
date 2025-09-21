from PIL import Image
import os
import subprocess
import shutil
from io import BytesIO
from tqdm import tqdm # Import tqdm for the progress bar

def check_cjpeg():
    """Checks if cjpeg is available in the system's PATH."""
    return shutil.which('cjpeg') is not None

def optimize_image(input_path, output_path, max_quality=90, min_quality=70, target_size_kb=None, use_cjpeg=True):
    """
    Optimizes an image to a target size by adjusting JPEG quality.

    Returns:
        tuple: (bool, str) -> (success_status, message string)
    """
    try:
        original_size_kb = os.path.getsize(input_path) / 1024
        
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            temp_buffer = BytesIO()
            quality = max_quality
            
            if target_size_kb:
                while quality >= min_quality:
                    temp_buffer.seek(0)
                    temp_buffer.truncate()
                    img.save(temp_buffer, format='JPEG', quality=quality, optimize=True)
                    current_size_kb = temp_buffer.tell() / 1024
                    if current_size_kb <= target_size_kb:
                        break
                    quality -= 5
                
                if current_size_kb > target_size_kb and quality < min_quality:
                    # If target not met, we still proceed with the smallest possible version
                    tqdm.write(f"⚠️  {os.path.basename(input_path)}: Target size not met. Smallest is {current_size_kb:.1f}KB at quality {min_quality}.")

            else:
                img.save(temp_buffer, format='JPEG', quality=max_quality, optimize=True)

        with open(output_path, 'wb') as f:
            f.write(temp_buffer.getvalue())

        if use_cjpeg:
            try:
                subprocess.run(
                    ['cjpeg', '-quality', str(quality), '-outfile', output_path, output_path],
                    check=True,
                    capture_output=True
                )
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass 

        final_size_kb = os.path.getsize(output_path) / 1024
        
        # Format the success message for return
        reduction_percent = (original_size_kb - final_size_kb) / original_size_kb * 100 if original_size_kb > 0 else 0
        message = f"{original_size_kb:.1f}KB → {final_size_kb:.1f}KB (Saved {reduction_percent:.1f}%)"
        
        return True, message

    except Exception as e:
        return False, f"Error: {str(e)}"

# --- Main Script ---
if __name__ == "__main__":
    input_dir = r"H:\Hosseini\dataset\image Kalantary"
    output_dir = r"H:\Hosseini\dataset\image Kalantary compressed"
    
    os.makedirs(output_dir, exist_ok=True)

    cjpeg_available = check_cjpeg()
    if not cjpeg_available:
        print("💡 Info: 'cjpeg' not found. Using Pillow-only optimization.")
        print("         For potentially smaller file sizes, consider installing mozjpeg.")

    image_files = [
        f for f in os.listdir(input_dir) 
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    if not image_files:
        print(f"No images found in '{input_dir}'. Exiting.")
    else:
        print(f"Found {len(image_files)} images. Starting optimization...")
        
        processed_count = 0
        error_logs = []

        # The main loop with tqdm progress bar
        for img_file in (pbar := tqdm(image_files, desc="Optimizing Images", unit="file")):
            # Update description to show the current file being processed
            pbar.set_description(f"Processing {img_file[:20]}")

            input_path = os.path.join(input_dir, img_file)
            output_filename = os.path.splitext(img_file)[0] + '.jpg'
            output_path = os.path.join(output_dir, output_filename)

            success, message = optimize_image(
                input_path=input_path,
                output_path=output_path,
                max_quality=85,
                min_quality=65,
                target_size_kb=300,
                use_cjpeg=cjpeg_available
            )
            
            if success:
                # Use tqdm.write() to print log messages without breaking the progress bar
                tqdm.write(f"✅ {img_file}: {message}")
                processed_count += 1
            else:
                # Still collect errors for a final summary
                error_log_message = f"❌ {img_file}: {message}"
                tqdm.write(error_log_message) # Also show errors in real-time
                error_logs.append(error_log_message)

        # --- Final Summary ---
        print("\n" + "="*60)
        print("Optimization Complete!")
        print(f"✅ Successfully processed: {processed_count}/{len(image_files)} files.")
        
        if error_logs:
            print(f"⚠️ Encountered {len(error_logs)} errors during the process.")
        print("="*60)