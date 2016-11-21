"""
This is an image classifier for DNA Origami Hinges
"""
from __future__ import division
import matplotlib.pyplot as plt
from sklearn import svm, datasets, metrics
import os
import pickle
import easygui as eg
import numpy as np
from imageio import imread, imwrite
from random import shuffle
from sklearn.externals import joblib	




def getImages(hingeDirectory, nonHingeDirectory):
	#Open the directory, pulls each image and returns an array with an np array as the 1st element and either a 1 or 0 as the 2nd
	#1 = Hinge, 0 = Non-Hinge
	n=0
	# FImages = np.array()
	FImages = np.zeros((len(os.listdir(hingeDirectory))+len(os.listdir(nonHingeDirectory))), dtype=np.int).tolist()
	# print FImages
	for file in os.listdir(hingeDirectory):
		rawNPArray = imread(hingeDirectory + '\\' + file)
		# print dim(rawNPArray)
		# print len(rawNPArray[0])
		# print len(rawNPArray[3][0])

		FImages[n] = [flatten(rawNPArray), 1]
		# print FImages[n]
		print ("Image " + str(n) + " built")
		n+=1
	for file in os.listdir(nonHingeDirectory):
		rawNPArray = imread(nonHingeDirectory + '\\' + file) 
		FImages[n] = [flatten(rawNPArray), 0]
		print ("Image " + str(n) + " built")
		n+=1
	return FImages

def flatten(image):
	# rowLen = len(image[0])
	# print image
	# flatImage = np.zeros((len(image)**2))	
	# print 'thisone'
	# return image[0]
	try:
		image = zip(*image[0]) #This strips the superflous rgb values
		flatImage = image[0][0]
		for num in range(1, len(image[0])):
			np.append(flatImage, np.hstack(image[0][num]))
	except TypeError:
		print 'huh'
		flatImage = image[0]
		print image
		for num in range(1, len(image)):
			np.append(flatImage, np.hstack(image[num]))
		# print flatImage
	# # image = zip(*image[0]) #This strips the superflous rgb values
	# # print image
	# # flatImage = np.hstack(image)
	# print flatImage
	return flatImage 



if __name__ == '__main__':
	#isn't python great? This is the same thing as the main method in java.
	#start by getting the images

	#Testing stuff
	hingeDir = eg.diropenbox(msg="Open labeled Hinge directory", title="Hinge dir")
	# print os.listdir(hingeDir)
	nonhingeDir = eg.diropenbox(msg="Open labeled Non-Hinge directory", title="Non-Hinge dir")
	images = getImages(hingeDir, nonhingeDir) #Getting training data

	# print images
	shuffle(images)
	# print images
	trainingImages = images[len(images)//2:] #Splits images into testing and training sets
	testingImages = images[:len(images)//2]
	
	# trainingImages = images
	# shuffle(images)
	# testingImages = images
	# userGamma, tolerence = eg.multenterbox("Enter custom values", "Customize SVC", ["Gamma", "Tolerence"])
	# if userGamma is None:
	# 	userGamma = "auto"
	# if tolerence is None:
	# 	tolerence = 0.001

	# classifier = svm.SVC(gamma=userGamma, tol=tolerence)
	classifier = svm.SVC()

	print zip(*trainingImages)[1]
	classifier.fit(zip(*trainingImages)[0], zip(*trainingImages)[1])
	# classifier.fit(zip(*trainingImages)[0], zip(*trainingImages)[1])


	expected = zip(*testingImages)[1]
	predicted = classifier.predict(zip(*testingImages)[0])

	print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
	print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

	joblib.dump(classifier, 'SVMClassifier.pkl')