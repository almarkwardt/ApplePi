from PIL import Image, ImageFilter;
import matplotlib.pyplot as plt;
import AppleOrBackgroundCategorizer;
import glob;
import os;
import errno;

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

	appleLeftBound = None;
	appleRightBound = None;
	appleTopBound = None;
	appleBottomBound = None;

	originalImage = Image.open(originalFilePath);

	# To reduce noise in the image that can throw off our bounds-finding, we
	# will apply a large-radius gaussian blur to the image. This allows us to
	# use a simple bounds-finding approach because the noise has already been
	# smoothed out.
	blurredImage = originalImage.filter(ImageFilter.GaussianBlur(radius=50));

	for pixelY in range(blurredImage.height):
		for pixelX in range(blurredImage.width):
			pixelValue = blurredImage.getpixel((pixelX, pixelY));

			if AppleOrBackgroundCategorizer.IsPixelAnApple(pixelValue):
				if appleLeftBound is None or pixelX < appleLeftBound:
					appleLeftBound = pixelX;
				else:
					# This pixel is farther to the right than a left bound
					# we found previously, so it isn't actually the left bound
					# (it may be the right bound, though.)
					pass;

				if appleRightBound is None or pixelX > appleRightBound:
					appleRightBound = pixelX;
				else:
					# This pixel is farther to the left than a right bound
					# we found previously, so it isn't actually the right bound.
					pass;

				if appleTopBound is None or pixelY < appleTopBound:
					appleTopBound = pixelY;
				else:
					# This pixel is farther to the bottom than a top bound
					# we found previously, so it isn't actually the top bound
					# (it may be the bottom bound, though.)
					pass;

				if appleBottomBound is None or pixelY > appleBottomBound:
					appleBottomBound = pixelY;
				else:
					# This pixel is farther to the top than a bottom bound
					# we found previously, so it isn't actually the bottom bound.
					pass;
			else:
				# Background pixel, we can ignore it.
				pass;

	# If we found anything belonging to an apple, then none of our bound values
	# should be unassigned. If any are unassigned, we didn't find an apple.
	if (appleLeftBound is not None and appleRightBound is not None
	  and appleTopBound is not None and appleBottomBound is not None):
		print("Extracting area ({0},{1})-({2},{3}) of image {4}".format(appleLeftBound, appleTopBound, appleRightBound, appleBottomBound, originalFilePath));
		appleSubImage = originalImage.crop((appleLeftBound, appleTopBound, appleRightBound, appleBottomBound));
		appleSubImage.save(appleSubImageFolderPath + originalFileName);
	else:
		print("Did not find an apple in image " + originalFilePath);
