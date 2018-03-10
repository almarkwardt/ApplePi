from PIL import Image, ImageFilter;
import matplotlib.pyplot as plt;
import AppleOrBackgroundCategorizer;
import glob;
import os;
import errno;

def FindBlobs(image, activePixelClassifier):
	discoveredBlobs = [];

	# First, I'll create a giant list of all pixels that are
	# considered "active" by the categorizer. In other words,
	# all pixels that would be considered part of a blob, even
	# if it is only a single-pixel blob.
	activePixels = [];

	for pixelY in range(image.height):
		for pixelX in range(image.width):
			pixelValue = image.getpixel((pixelX, pixelY));

			if activePixelClassifier(pixelValue):
				activePixels.append((pixelX, pixelY));
			else:
				# Keep checking, this pixel isn't active though
				pass;

	# Now I'll use a flood fill algorithm to find contiguous blob
	# areas. I'll consider the eight pixels surrounding each active
	# pixel and if it's also active, make it part of the blob.
	while len(activePixels) > 0:
		# We know we have at least one active pixel, so we start by making
		# that pixel part of "this blob", and we remove that pixel from the
		# active pixels so we don't "discover" it again later. We'll basically
		# do that in a loop... if a pixel appears to be connected to our
		# growing blob we'll add it to "this" blob and remove it from the
		# active pixels list so we won't keep re-discovering the same pixels
		# over and over.
		print("Active pixel list now at " + str(len(activePixels)) + " items.");
		pixelsInThisBlob = [];
		pixelsInThisBlob.append(activePixels[0]);
		activePixels.remove(activePixels[0]);

		currentlyConsideredPixelIndex = 0;
		while(currentlyConsideredPixelIndex < len(pixelsInThisBlob)):
			currentlyConsideredPixel = pixelsInThisBlob[currentlyConsideredPixelIndex];
			#print("Considering area adjoining pixel " + str(currentlyConsideredPixel));

			# We consider the eight pixels surrounding this one.
			adjoiningPixels = [
				(currentlyConsideredPixel[0] - 1, currentlyConsideredPixel[1] - 1),
				(currentlyConsideredPixel[0], currentlyConsideredPixel[1] - 1),
				(currentlyConsideredPixel[0] + 1, currentlyConsideredPixel[1] - 1),
				(currentlyConsideredPixel[0] - 1, currentlyConsideredPixel[1]),
				(currentlyConsideredPixel[0] + 1, currentlyConsideredPixel[1]),
				(currentlyConsideredPixel[0] - 1, currentlyConsideredPixel[1] + 1),
				(currentlyConsideredPixel[0], currentlyConsideredPixel[1] + 1),
				(currentlyConsideredPixel[0] + 1, currentlyConsideredPixel[1] + 1)
			];
			# But we also need to do bounds-checking. We'll filter out any
			# pixels that have locations outside the bounds of the image.
			adjoiningPixels = [pixel for pixel in adjoiningPixels if (pixel[0] >= 0 and pixel[1] >= 0 and pixel[0] < image.width and pixel[1] < image.height)];
			#print("Found " + str(len(adjoiningPixels)) + " real adjoining pixels.");

			for adjoiningPixel in adjoiningPixels:
				if adjoiningPixel in activePixels and adjoiningPixel not in pixelsInThisBlob:
					# This is an active adjoining pixel and we have not already
					# discovered it previously, so it gets added to the blob.
					activePixels.remove(adjoiningPixel);
					pixelsInThisBlob.append(adjoiningPixel);
					#print("Pixels in this blob grows to " + str(len(pixelsInThisBlob)));
				else:
					# This is either not an active pixel or it is but we've already
					# counted it as part of the blob, so we don't count it again.
					pass;

			# Ok move on to the next pixel we need to consider
			currentlyConsideredPixelIndex += 1;

		# We've found a blob, now we need to find the extents so we can
		# return it.
		leftBound = pixelsInThisBlob[0][0];
		rightBound = leftBound;
		topBound = pixelsInThisBlob[0][1];
		bottomBound = topBound;

		for pixel in pixelsInThisBlob[1:]:
			if pixel[0] < leftBound:
				leftBound = pixel[0];
			else:
				# Keep the old value.
				pass;

			if pixel[0] > rightBound:
				rightBound = pixel[0];
			else:
				# Keep the old value.
				pass;

			if pixel[1] < topBound:
				topBound = pixel[1];
			else:
				# Keep the old value.
				pass;

			if pixel[1] > bottomBound:
				bottomBound = pixel[1];
			else:
				# Keep the old value.
				pass;

		# And now we've found the extents of the blob, so add it to the
		# blob list.
		discoveredBlobs.append((leftBound, rightBound, topBound, bottomBound));

	return discoveredBlobs;




filePathsOfOriginalImages = glob.glob("./Images/**/*.jpeg");

# Go through each image we found and extract out the subregion that seems to
# belong to the apple. We'll save these images in a folder called AppleSubImages
# in each apple category folder (one in "GrannySmith", one in "Kanzi", etc.)
for originalFilePath in filePathsOfOriginalImages:
	originalFilePath = originalFilePath.replace("\\", "/");
	originalFileName = originalFilePath[originalFilePath.rfind("/") + 1:];
	containingFolderPath = originalFilePath[0:originalFilePath.rfind("/")] + "/";
	appleSubImageFolderPath = containingFolderPath + "AppleSubImages/";

	try:
		os.makedirs(appleSubImageFolderPath);
	except OSError as err:
		if err.errno != errno.EEXIST:
			raise;
		else:
			# Ok, the folder already exists, that's not a problem for us.
			pass;

	originalImage = Image.open(originalFilePath);

	# To reduce noise in the image that can throw off our bounds-finding, we
	# will apply a large-radius gaussian blur to the image. This should make
	# an apple (a contiguous convex object) appear even more contiguous/convex
	# which should make finding its boundaries easier.
	blurredImage = originalImage.filter(ImageFilter.GaussianBlur(radius=25));

	# We'll find all contiguous apple-ish pixel blobs in the image and take
	# the largest one to be the apple itself.
	print("Finding blobs in " + originalFilePath);
	discoveredBlobs = FindBlobs(blurredImage, AppleOrBackgroundCategorizer.IsPixelAnApple);

	if len(discoveredBlobs) > 0:
		print("Found " + str(len(discoveredBlobs)) + " blobs in " + originalFilePath);
		largestBlob = discoveredBlobs[0];
		largestBlobArea = ((largestBlob[1] - largestBlob[0]) + 1) * ((largestBlob[3] - largestBlob[2]) + 1);

		for blob in discoveredBlobs[1:]:
			blobArea = ((blob[1] - blob[0]) + 1) * ((blob[3] - blob[2]) + 1);

			if blobArea > largestBlobArea:
				largestBlob = blob;
				largestBlobArea = blobArea;
				print("Found new largest blob of area " + str(largestBlobArea));
			else:
				# This blob is smaller than one we found previously so forget it.
				print("Blob of area " + str(blobArea) + " smaller than " + str(largestBlobArea));

		print("Extracting area ({0},{1})-({2},{3}) of image {4}".format(largestBlob[0], largestBlob[2], largestBlob[1], largestBlob[3], originalFilePath));
		appleSubImage = originalImage.crop((largestBlob[0], largestBlob[2], largestBlob[1], largestBlob[3]));
		appleSubImage.save(appleSubImageFolderPath + originalFileName);
	else:
		print("Did not find an apple in image " + originalFilePath);
