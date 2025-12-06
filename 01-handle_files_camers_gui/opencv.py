import cv2

import numpy
import os
def main():
    # Make an array of 120,000 random bytes.
    randomByteArray = bytearray(os.urandom(120000))
    flatNumpyArray = numpy.array(randomByteArray)
    # Convert the array to make a 400x300 grayscale image.
    grayImage = flatNumpyArray.reshape(300, 400)
    cv2.imwrite('RandomGray.png', grayImage)
    # Convert the array to make a 400x100 color image.
    bgrImage = flatNumpyArray.reshape(100, 400, 3)
    cv2.imwrite('RandomColor.png', bgrImage)

    # file = 'sample_imgs/img-1.jpg'
    # img = cv2.imread(file)
    
    # if img is None:
    #     print(f'failed to open file: {file}')
    #     exit(1)
    # else:
    #     print("worked fine")
    
    # print(img.shape)
    # print(img)
    cv2.videw
    


if __name__ == "__main__":
    main()