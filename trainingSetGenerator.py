import random

TRAINING_SET_SIZE = 750
TEST_SET_SIZE = 10
TENDENCY_CHOICE_LIST_SIZE = 20
PROPORTION_PURCHASED = 0.25
OUTPUT_FILE_NAME = "examples.py"

# All of the features of shoes with all of their possible values
featuresWithValues = { "brand" : ["Nike", "Adidas", "Frye", "Converse", "Skechers"],
                       "size"  : [8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12],
                       "width" : ["narrow", "regular", "wide"],
                       "style" : ["athletic", "dress", "casual", "work"],
                       "material" : ["leather", "synthetic", "canvas"],
                       "laced" : ["yes", "no"] }

# A score for each value of each feature (lists will be normalized)
# indicating about how likely each value will be chosen for shoes
# that were purchased
featureTendencies = { "brand" : [50, 40, 10, 15, 20],
                      "size"  : [0, 5, 5, 0, 15, 50, 40, 10, 0],
                      "width" : [10, 60, 20],
                      "style" : [50, 10, 20, 0],
                      "material" : [15, 50, 20],
                      "laced" : [70, 30] }

# Names for the purchased/not purchased classes
classNames = { True : "purchased", False: "not-purchased" }

# Normalize all of the values in featureTendencies
for featureName, tendencies in featureTendencies.iteritems():
    tendenciesTotal = sum(tendencies)

    for i, tendency in enumerate(tendencies):
        tendencies[i] = float(tendencies[i]) / float(tendenciesTotal)

# Generate a bunch of examples that'll be split into a training and a testing set

examples = []

for i in range(0, TRAINING_SET_SIZE + TEST_SET_SIZE):
    example = {}
    isPurchased = False
    if random.random() < PROPORTION_PURCHASED:
        isPurchased = True

    if isPurchased:
        for featureName, tendencies in featureTendencies.iteritems():
            # If this is an example of a purchased shoe, we need a weighted
            # random choice of a value for each feature based on the tendencies.
            # This is done kind of quick and dirty by making a list of values
            # for each feature where values with higher tendencies are repeated more,
            # then picking a random element from that list

            valuesForThisFeature = featuresWithValues[featureName]

            weightedListOfValues = []
            for j in range(0, len(tendencies)):
                weightedListOfValues += [valuesForThisFeature[j]] * int(tendencies[j] * TENDENCY_CHOICE_LIST_SIZE)

            example[featureName] = random.choice(weightedListOfValues)
    else:
        for featureName, values in featuresWithValues.iteritems():
            # If this is an example of a shoe that wasn't purchased, just
            # randomly pick a value for each feature
            example[featureName] = random.choice(values)

    examples.append((example, classNames[isPurchased]))

# Write the training set to a file
# This is a mess. I'm sorry.

try:
    examplesFile = open(OUTPUT_FILE_NAME, "w")
except IOError as e:
    print "Couldn't write the examples to a file: " + str(e)

examplesFile.write("trainingExamples = [\n")
for example in examples[:TRAINING_SET_SIZE]:
    examplesFile.write("\t({ ")

    firstRun = True
    for feature, value in example[0].iteritems():
        if not firstRun:
            examplesFile.write("\t   ")
        else:
            firstRun = not firstRun
        examplesFile.write("\"" + feature + "\" : \"" + str(value) + "\",\n")

    examplesFile.write("\t}, \"" + example[1] + "\"),\n\n")
examplesFile.write("]\n\n")

examplesFile.write("testExamples = [\n")
for example in examples[TRAINING_SET_SIZE:]:
    examplesFile.write("\t({ ")

    firstRun = True
    for feature, value in example[0].iteritems():
        if not firstRun:
            examplesFile.write("\t   ")
        else:
            firstRun = not firstRun
        examplesFile.write("\"" + feature + "\" : \"" + str(value) + "\",\n")

    examplesFile.write("\t}, \"" + example[1] + "\"),\n\n")
examplesFile.write("]\n")
