from PIL import Image;
import ColorChannelRatios;

def IsPixelAnApple(pixelValue):
	redGreenRatio = ColorChannelRatios.GetRedGreenRatio(pixelValue);
	redBlueRatio = ColorChannelRatios.GetRedBlueRatio(pixelValue);
	greenBlueRatio = ColorChannelRatios.GetGreenBlueRatio(pixelValue);

	# A background pixel has all three ratios falling between one and 1.5,
	# based on the analysis I did previously. This can be seen in the
	# ColorChannelRatioHistograms.png file.
	isABackgroundPixel = ((redGreenRatio >= 1.0 and redGreenRatio < 1.5)
	                  and (redBlueRatio >= 1.0 and redBlueRatio < 1.5)
	                  and (greenBlueRatio >= 1.0 and greenBlueRatio < 1.5));

	return (not isABackgroundPixel);
