import nltk
from examples import trainingExamples
from examples import testExamples

# Create and train the classifier

classifier = nltk.NaiveBayesClassifier.train(trainingExamples)

# Try to classify some examples

for example in testExamples:
    classification = classifier.classify(example[0])

    wasRight = "Good!"
    if classification is not example[1]:
        wasRight = "BAD!"

    print "Classification: " + classification + "\tReal class: " + example[1] + "   \t" + wasRight
