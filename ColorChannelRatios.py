def GetRedGreenRatio(pixelValue):
	redGreenRatio = pixelValue[0] / max(pixelValue[1], 1);

	return redGreenRatio;


def GetRedBlueRatio(pixelValue):
	redBlueRatio = pixelValue[0] / max(pixelValue[2], 1);

	return redBlueRatio;


def GetGreenBlueRatio(pixelValue):
	greenBlueRatio = pixelValue[1] / max(pixelValue[2], 1);

	return greenBlueRatio;
