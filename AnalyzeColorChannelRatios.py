from PIL import Image;
import matplotlib.pyplot as plt;
import ColorChannelRatios;

# It looks like for every photo I took, the background is shown at 100 pixels
# from the edge. That is, for a 960 x 540 image, the pixels at (100, 100),
# (860, 100), (100, 440), and (860, 440) are all part of the background. The
# apple is included at the center point (480, 270) and at least in a 10 x 10
# pixel square centered at this point. So I'm going to pull out the ratios of
# the color channels ((R / G), (R / B), (G / B)) at the following points and
# compare them:
# (100, 100), (860, 100), (100, 440), (860, 440)
# (480, 270), (475, 265), (485, 265), (475, 275), (485, 275)
backgroundPixelLocations = [(100, 100), (860, 100), (100, 440), (860, 440)];
applePixelLocations = [(480, 270), (475, 265), (485, 265), (475, 275), (485, 275)];

# I'm just going to use a subset of the images, but I'll choose at least one
# image from each apple type to check that they are all separable.
filePathsOfFujiImages = ["./Images/Fuji/fuji-1-001.jpeg",
                         "./Images/Fuji/fuji-1-010.jpeg",
                         "./Images/Fuji/fuji-2-003.jpeg",
                         "./Images/Fuji/fuji-2-013.jpeg",
                         "./Images/Fuji/fuji-3-007.jpeg",
                         "./Images/Fuji/fuji-3-012.jpeg"];

filePathsOfGalaImages = ["./Images/Gala/gala-1-003.jpeg",
                         "./Images/Gala/gala-1-009.jpeg",
                         "./Images/Gala/gala-2-004.jpeg",
                         "./Images/Gala/gala-2-011.jpeg"];

filePathsOfGrannySmithImages = ["./Images/GrannySmith/grannysmith-1-002.jpeg",
                                "./Images/GrannySmith/grannysmith-1-012.jpeg",
                                "./Images/GrannySmith/grannysmith-2-001.jpeg",
                                "./Images/GrannySmith/grannysmith-2-004.jpeg",
                                "./Images/GrannySmith/grannysmith-3-003.jpeg",
                                "./Images/GrannySmith/grannysmith-3-009.jpeg"];

filePathsOfHoneyCrispImages = ["./Images/HoneyCrisp/honeycrisp-1-004.jpeg",
                               "./Images/HoneyCrisp/honeycrisp-1-007.jpeg",
                               "./Images/HoneyCrisp/honeycrisp-2-001.jpeg",
                               "./Images/HoneyCrisp/honeycrisp-2-009.jpeg",
                               "./Images/HoneyCrisp/honeycrisp-3-012.jpeg",
                               "./Images/HoneyCrisp/honeycrisp-3-014.jpeg"];

filePathsOfKanziImages = ["./Images/Kanzi/kanzi-1-002.jpeg",
                         "./Images/Kanzi/kanzi-1-006.jpeg",
                         "./Images/Kanzi/kanzi-2-003.jpeg",
                         "./Images/Kanzi/kanzi-2-009.jpeg"];

filePathsOfPinkLadyImages = ["./Images/PinkLady/pinklady-1-001.jpeg",
                             "./Images/PinkLady/pinklady-1-012.jpeg",
                             "./Images/PinkLady/pinklady-2-002.jpeg",
                             "./Images/PinkLady/pinklady-2-011.jpeg",
                             "./Images/PinkLady/pinklady-3-004.jpeg",
                             "./Images/PinkLady/pinklady-3-007.jpeg"];

filePathsOfRedDeliciousImages = ["./Images/RedDelicious/reddelicious-1-001.jpeg",
                                 "./Images/RedDelicious/reddelicious-1-008.jpeg",
                                 "./Images/RedDelicious/reddelicious-2-004.jpeg",
                                 "./Images/RedDelicious/reddelicious-2-010.jpeg"];

filePathsOfImageSamples = (filePathsOfFujiImages + filePathsOfGalaImages
                               + filePathsOfGrannySmithImages + filePathsOfHoneyCrispImages
                               + filePathsOfKanziImages + filePathsOfPinkLadyImages + filePathsOfRedDeliciousImages);

# Ok now we'll actually pull the pixel values and calculate and store the ratios.
backgroundRedGreenRatios = [];
backgroundRedBlueRatios = [];
backgroundGreenBlueRatios = [];
appleRedGreenRatios = [];
appleRedBlueRatios = [];
appleGreenBlueRatios = [];

for imageFilePath in filePathsOfImageSamples:
	sampleImage = Image.open(imageFilePath);

	# Do the calculation on the background pixels, then the apple pixels.
	# There is a chance that we will end up with a denominator of zero, since
	# we are dealing with brightness values. In those cases, we will substitute
	# the value for one, which should be accurate enough.

	for backgroundPixelLocation in backgroundPixelLocations:
		pixelValue = sampleImage.getpixel(backgroundPixelLocation);

		redGreenRatio = ColorChannelRatios.GetRedGreenRatio(pixelValue);
		redBlueRatio = ColorChannelRatios.GetRedBlueRatio(pixelValue);
		greenBlueRatio = ColorChannelRatios.GetGreenBlueRatio(pixelValue);

		backgroundRedGreenRatios.append(redGreenRatio);
		backgroundRedBlueRatios.append(redBlueRatio);
		backgroundGreenBlueRatios.append(greenBlueRatio);

	for applePixelLocation in applePixelLocations:
		pixelValue = sampleImage.getpixel(applePixelLocation);

		redGreenRatio = ColorChannelRatios.GetRedGreenRatio(pixelValue);
		redBlueRatio = ColorChannelRatios.GetRedBlueRatio(pixelValue);
		greenBlueRatio = ColorChannelRatios.GetGreenBlueRatio(pixelValue);

		appleRedGreenRatios.append(redGreenRatio);
		appleRedBlueRatios.append(redBlueRatio);
		appleGreenBlueRatios.append(greenBlueRatio);

plt.subplot(321);
plt.hist(backgroundRedGreenRatios, bins=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]);
plt.xlabel("Red / Green Ratio");
plt.ylabel("Pixel Counts");
plt.title("Background Red / Green Pixel Ratios");
plt.subplot(322);
plt.hist(appleRedGreenRatios, bins=[0, 1, 2, 3, 4, 5]);
plt.xlabel("Red / Green Ratio");
plt.ylabel("Pixel Counts");
plt.title("Apple Red / Green Pixel Ratios");
plt.subplot(323);
plt.hist(backgroundRedBlueRatios, bins=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]);
plt.xlabel("Red / Blue Ratio");
plt.ylabel("Pixel Counts");
plt.title("Background Red / Blue Pixel Ratios");
plt.subplot(324);
plt.hist(appleRedBlueRatios, bins=[0, 1, 2, 3, 4, 5]);
plt.xlabel("Red / Blue Ratio");
plt.ylabel("Pixel Counts");
plt.title("Apple Red / Blue Pixel Ratios");
plt.subplot(325);
plt.hist(backgroundGreenBlueRatios, bins=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]);
plt.xlabel("Green / Blue Ratio");
plt.ylabel("Pixel Counts");
plt.title("Background Green / Blue Pixel Ratios");
plt.subplot(326);
plt.hist(appleGreenBlueRatios, bins=[0, 1, 2, 3, 4, 5]);
plt.xlabel("Green / Blue Ratio");
plt.ylabel("Pixel Counts");
plt.title("Apple Green / Blue Pixel Ratios");
plt.tight_layout(pad=0.5);
plt.show();
