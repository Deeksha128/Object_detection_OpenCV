#!/usr/bin/env python

import cv2
import numpy as np

def read_rgb_image(image_name,show):
	rgb_image=cv2.imread(image_name)
	if show:
		cv2.imshow("RGB Image",rgb_image)
	return rgb_image

def convert_rgb_to_hsv(rgb_image,show):
	hsv_image=cv2.cvtColor(rgb_image,cv2.COLOR_BGR2HSV)
	if show:
		cv2.imshow("HSV Image",hsv_image)
	return hsv_image

def color_filtering(hsv_image,yellowLower,yellowUpper,show):
	binary_mask=cv2.inRange(hsv_image,yellowLower,yellowUpper)
	if show:
		cv2.imshow("Mask Image",binary_mask)
	return binary_mask

def getContours(binary_mask):
	_,contours,hierarchy=cv2.findContours(binary_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	return contours

def draw_ball_contour(binary_mask,rgb_image,contours):
	for c in contours:
		area=cv2.contourArea(c)
		((x,y),radius)=cv2.minEnclosingCircle(c)

		if area>900:
			cv2.drawContours(rgb_image,[c],-1,(150,0,255),2)
			cx,cy=get_contour_centre(c)
			cv2.circle(rgb_image,(cx,cy),(int)(radius),(0,0,255),1)
			print("Area: {}".format(area))
		cv2.imshow("RGB Contours",rgb_image)
		

def get_contour_centre(c):
	M=cv2.moments(c)
	cx=-1
	cy=-1
	if (M['m00']!=0):
		cx=int(M['m10']/M['m00'])
		cy=int(M['m01']/M['m00'])
	return cx,cy

def main():
	image_name="images/tennisball05.jpg"
	rgb_image=read_rgb_image(image_name,True)
	hsv_image=convert_rgb_to_hsv(rgb_image,True)
	yellowLower=(30,10,10)
	yellowUpper=(60,255,255)
	binary_mask=color_filtering(hsv_image,yellowLower,yellowUpper,True)
	contours=getContours(binary_mask)
	draw_ball_contour(binary_mask,rgb_image,contours)

	cv2.waitKey(0)
	cv2.destroyAllWindows

if __name__ == '__main__':
	main()