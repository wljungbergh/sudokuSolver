import cv2 as cv 
import numpy as np 
import imutils
import pytesseract
import sudokusolver as ss
import os
from imutils import paths


def load_image(image_path):
    return cv.imread(image_path)

def preprocess_image(image):
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(7,7),0)
    thresh = cv.adaptiveThreshold(gray,255,1,1,11,2)
    return thresh

def find_contours(image):
    cnts, _  = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=lambda ctr: cv.boundingRect(ctr)[0])
    return cnts

def rectify(h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2),dtype = np.float32)
 
        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]
        hnew[2] = h[np.argmax(add)]
         
        diff = np.diff(h,axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
  
        return hnew

def find_correct_contour(cnts):
    biggest = None
    max_area = 0
    for i in cnts:
            area = cv.contourArea(i)
            if area > 100:
                    peri = cv.arcLength(i,True)
                    approx = cv.approxPolyDP(i,0.02*peri,True)
                    if area > max_area and len(approx)==4:
                            biggest = approx
                            max_area = area
    approx=rectify(biggest)
    return approx

def transform_image(image, contour, size = 450):
    h = np.array([ [0,0],[size,0],[size,size],[0,size] ],np.float32)
    retval = cv.getPerspectiveTransform(contour,h)
    warp = cv.warpPerspective(image,retval,(size,size))

    return warp

def extract_sudoku_image(image_path):
    image_org = load_image(image_path)
    image = preprocess_image(image_org)
    cnts = find_contours(image)
    approx = find_correct_contour(cnts)
    warp = transform_image(image, approx)

    return warp
    
def divide_sudoku_image(image):
    full_size = image.shape[0]
    cell_size = full_size // 9
    cells = []
    for i in range(9):
        for j in range(9):
            sub_img = image[i*cell_size:(i+1)*cell_size,j*cell_size:(j+1)*cell_size]
            cells.append(sub_img)
    '''for i in range(9):
        sub_img = image[i*cell_size:(i+1)*cell_size,:]
        cells.append(sub_img)'''


    return cells

if __name__ == '__main__':
    img_paths = list(paths.list_images('./images/sudoku_dataset'))
    for index, fp in enumerate(img_paths):
        #fp = ('./images/img-002.jpg')
        img = extract_sudoku_image(fp)
        cells = divide_sudoku_image(img)
        img2 = cv.bitwise_not(cells[2])
        suduko = ''
        '''for d in cells:
            d = cv.bitwise_not(d)
            rec = pytesseract.image_to_string(d,config='--psm 10')
            number = list(filter(str.isdigit, rec))
            if number:
                suduko += number[0]
            else:
                suduko += '.'
        
        print(ss.create_array_from_string(suduko))'''
        '''cv.imshow("Game Boy Screen", img)
        cv.waitKey(0)'''
        for idx, d in enumerate(cells):
            d = cv.bitwise_not(d)
            cv.imwrite('./images/dataset/{}_{}.png'.format(index, idx), d)
            

    


    #cv.waitKey(0)
    cv.destroyAllWindows()
    print('done')
    #img = preprocess_image(img)
   