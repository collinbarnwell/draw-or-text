

def argmax(iterable):
        return max(enumerate(iterable), key=lambda x: x[1])[0]

def t():

    data = ["dry", "damp", "soggy"]

    priorCloud = 0.17
    priorRain = 0.2
    priorSun = 0.63

    stateTransition = {
        "cloud": {"cloud":0.125, "sun":0.25, "rain":0.625},
        "sun": {"cloud":0.375, "sun":0.5, "rain":0.125},
        "rain": {"cloud":0.375, "sun":0.25, "rain":0.375}
    }

    confusionMatrix = {
        "cloud": {"dry": .25, "dryish": .25,  "damp": .25, "soggy": .25},
        "sun": {"dry": .6, "dryish": .2,  "damp": .15, "soggy": .05 },
        "rain": {"dry": .05, "dryish": .1,  "damp": .35, "soggy": .5}
    }

    # first round
    sunpath = []
    cloudpath = []
    rainpath = []

    prevCprob = priorCloud * confusionMatrix["cloud"][data[0]]
    prevRprob = priorRain * confusionMatrix["rain"][data[0]]
    prevSprob = priorSun * confusionMatrix["sun"][data[0]]

    print "first state cloudy: ", prevCprob, " rainy: ", prevRprob, " sunny: ", prevSprob

    for obs in data[1:]:

        sposs = [
            prevCprob * stateTransition["cloud"]["sun"] * confusionMatrix["sun"][obs],
            prevSprob * stateTransition["sun"]["sun"] * confusionMatrix["sun"][obs],
            prevRprob * stateTransition["rain"]["sun"] * confusionMatrix["sun"][obs]
        ]
        sunBest = argmax(sposs)

        if (sunBest == 0):
            nextsunpath = cloudpath[:]
            nextsunpath.append("cloud")
            print "s - for ", obs, " chose ", sunBest, ": ", sposs[sunBest], " w p = ", prevSprob
        elif (sunBest == 1):
            nextsunpath = sunpath[:]
            nextsunpath.append("sun")
            print "s - for ", obs, " chose ", sunBest, ": ", sposs[sunBest], " w p = ", prevSprob
        else:
            nextsunpath = rainpath[:]
            nextsunpath.append("rain")
            print "s - for ", obs, " chose ", sunBest, ": ", sposs[sunBest], " w p = ", prevSprob


        rposs = [
            prevCprob * stateTransition["cloud"]["rain"] * confusionMatrix["rain"][obs],
            prevSprob * stateTransition["sun"]["rain"] * confusionMatrix["rain"][obs],
            prevRprob * stateTransition["rain"]["rain"] * confusionMatrix["rain"][obs]
        ]
        print "Rain probs: ", rposs
        rainBest = argmax(rposs)

        if (rainBest == 0):
            nextrainpath = cloudpath[:]
            nextrainpath.append("cloud")
            print "r - for ", obs, " chose ", rainBest, ": ", rposs[rainBest], " w p = ", prevRprob
        elif (rainBest == 1):
            nextrainpath = sunpath[:]
            nextrainpath.append("sun")
            print "r - for ", obs, " chose ", rainBest, ": ", rposs[rainBest], " w p = ", prevRprob
        else:
            nextrainpath = rainpath[:]
            nextrainpath.append("rain")
            print "r - for ", obs, " chose ", rainBest, ": ", rposs[rainBest], " w p = ", prevRprob


        cposs = [
            prevCprob * stateTransition["cloud"]["cloud"] * confusionMatrix["cloud"][obs],
            prevSprob * stateTransition["sun"]["cloud"] * confusionMatrix["cloud"][obs],
            prevRprob * stateTransition["rain"]["cloud"] * confusionMatrix["cloud"][obs]
        ]
        cloudBest = argmax(cposs)

        if (cloudBest == 0):
            nextcloudpath = cloudpath[:]
            nextcloudpath.append("cloud")
            print "c - for ", obs, " chose ", cloudBest, ": ", cposs[cloudBest], " w p = ", prevCprob
        elif (cloudBest == 1):
            nextcloudpath = sunpath[:]
            nextcloudpath.append("sun")
            print "c - for ", obs, " chose ", cloudBest, ": ", cposs[cloudBest], " w p = ", prevCprob
        else:
            nextcloudpath = rainpath[:]
            nextcloudpath.append("rain")
            print "c - for ", obs, " chose ", cloudBest, ": ", cposs[cloudBest], " w p = ", prevCprob

        prevSprob = sposs[sunBest]
        prevRprob = rposs[rainBest]
        prevCprob = cposs[cloudBest]

        rainpath = nextrainpath
        sunpath = nextsunpath
        cloudpath = nextcloudpath
        print "second state cloudy: ", prevCprob, " rainy: ", prevRprob, " sunny: ", prevSprob


    pathProbs = [prevCprob, prevRprob, prevSprob]
    bestpath = argmax(pathProbs)
    if bestpath == 0:
        cloudpath.append("cloud")
        return cloudpath
    elif bestpath == 1:
        rainpath.append("rain")
        return rainpath
    else:
        sunpath.append("sun")
        return sunpath




