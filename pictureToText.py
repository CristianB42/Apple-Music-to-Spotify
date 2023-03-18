# This program will analyze screenshots from the Apple Music library and extract the song title and artist
# in a txt file.

import os
import pytesseract

# Initialize pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

captures_path = os.getcwd() + '\captures\\'
print ("captures_path: " + captures_path)

fp_tmp = open('tmp.txt', 'w')

total = len(os.listdir(captures_path))
count = 0

# Iterate through all the captures in the captures folder and extract the song title and artist
# in a 'tmp.txt' file.
for picName in os.listdir(captures_path):
    count += 1
    path = './captures/' + picName
    print( 'Extracting information from picture ' + str(count) + '/' + str(total) + ' at path: ' + path)

    content = pytesseract.image_to_string(path)
    fp_tmp.write(content)

fp_tmp.close()
print ('Analysis complete!')

# Remove all empty lines from 'tmp.txt' file and store result in 'songs.txt' 
fp_tmp = open('tmp.txt', 'r')
fp_songs = open('songs.txt', 'w')
line_started = False
for line in fp_tmp:
    if line != "\n":
        if line_started is True:
            new_line += line.strip() + "\n"
            fp_songs.write(new_line)
            line_started = False
        else:
            new_line = line.strip() + " "
            line_started = True

        
fp_tmp.close()
fp_songs.close()

# Delete tmp file
os.remove('tmp.txt')


        
# print(pytesseract.image_to_string(r'IMG_6265.jpeg'))