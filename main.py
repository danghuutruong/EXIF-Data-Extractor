from PIL import Image, ExifTags
import os
import sys

def print_logo():
    print("""
================================
https://github.com/danghuutruong
┐ (￣∀￣) ┌ 
I don't care what you are doing
================================
""")

def write_exif_data(exif_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for tag, value in exif_data.items():
            if isinstance(value, bytes):
                try:
                    value = value.decode()
                except UnicodeDecodeError:
                    value = value.hex()
            f.write(f"{tag}: {value}\n")

def get_maps_url(gps_info):
    if not gps_info:
        return "No GPS data available"
    
    def convert_to_degrees(value):
        return value[0] + value[1] / 60 + value[2] / 3600.0
    
    lat = convert_to_degrees(gps_info['GPSLatitude'])
    lon = convert_to_degrees(gps_info['GPSLongitude'])
    
    if gps_info.get('GPSLatitudeRef') == 'S':
        lat = -lat
    if gps_info.get('GPSLongitudeRef') == 'W':
        lon = -lon
    
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        info = image._getexif()
        if not info:
            print("\n[!] No EXIF data found\n")
            return

        exif_data = {ExifTags.TAGS.get(tag, tag): value for tag, value in info.items()}
        
        if "GPSInfo" in exif_data:
            gps_data = {ExifTags.GPSTAGS.get(k, k): v for k, v in exif_data["GPSInfo"].items()}
            exif_data["GPSInfo"] = gps_data
            exif_data["Google Maps link"] = get_maps_url(gps_data)
        
        print("\n===== EXIF DATA =====")
        for key in ["Make", "Model", "DateTimeOriginal", "ExifImageWidth", "ExifImageHeight", "ExposureTime", "FNumber", "ISOSpeedRatings", "LensModel", "Flash", "Orientation", "MimeType", "ImageDescription", "Keywords", "Copyright"]:
            print(f"{key}: {exif_data.get(key, 'N/A')}")
        print("Google Maps link:", exif_data.get("Google Maps link", "N/A"))
        print("=====================")
        
        out_file = os.path.splitext(image_path)[0] + ".txt"
        write_exif_data(exif_data, out_file)
        print(f'\n[+] EXIF data saved to {out_file}\n')
    except Exception as e:
        print(f"\n[!] Error processing image: {e}\n")

def main():
    print_logo()
    try:
        while True:
            path = input("Enter path to image file (Press Ctrl+C to exit): ").strip()
            if os.path.isfile(path):
                get_exif_data(path)
            else:
                print("\n[!] Invalid file path\n")
    except KeyboardInterrupt:
        print("\n[!] Exiting program...\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
