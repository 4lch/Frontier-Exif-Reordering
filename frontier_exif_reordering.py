import sys
import os
import glob
from subprocess import check_output

# List of supported image file extensions, not case-sensitive
exts = ['jpg', 'jpeg']

# Get the folder that the user has dropped on the script
droppedFolder = sys.argv[1]
print(f'Working from {droppedFolder}.')

# Grab images with expected file extensions
grabbed_files = glob.glob(f'{droppedFolder}/*.{exts[0]}')
for ext in exts[1:]:
    grabbed_files += glob.glob(f'{droppedFolder}/*.{ext}')

# Iterate over images
for f in grabbed_files:
    
    # Split the filename into more useful bits
    img_path = os.path.abspath(f)
    name = os.path.basename(f)
    name_no_ext = os.path.splitext(name)[0]
    ext = os.path.splitext(img_path)[1]

    print(f'---\nWorking on {name}.')

    # Use exiftool to get the frame number
    frame_number = check_output(['exiftool.exe', '-MakerNotes:Framenumber', '-b', img_path]).decode('utf-8')

    # Handle cases where the relevant exif data is missing
    if frame_number == '':
        print('\tNo frame number was found.')

    # Relevant exif data has been found !
    else:
        print(f'\tImage has frame number [{frame_number}].')
        # Left-pad the frame number, eg from '13' to '013' to avoid issues with alphabetical order of files.
        # Padding to 3 characters should be plenty, but this can be increased.
        frame_number = frame_number.rjust(3, '0')

        # Build the new filename
        final_dest = f'{droppedFolder}\\{frame_number}{ext}'

        # Rename the image with the correct frame number from the exif data
        os.rename(img_path, final_dest)

        print(f'\tImage renamed to {frame_number}{ext}.')

# input('press Enter to escape')