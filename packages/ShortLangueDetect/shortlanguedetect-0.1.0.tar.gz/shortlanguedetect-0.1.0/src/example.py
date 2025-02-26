import short_language_detection as sld

# Create a detector
predictor = sld.Detector()

# Detect the language of a text
print(predictor.detect("hello the world"))
