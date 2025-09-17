#in this script, we optimize an index computed on a orthophoto, combining
#multi source images. For each pixels we have 15 values:
# - three RGB channels
# - ten multispectral channels
# - one thermal channel
# - one height channel from DEM file
#
#We optimize using simple gradient descent. The cost function is root mean
#square error against a target trait.
#
#For each pixel we have 15 numeric values, from  P1 to P15. The general
#formula for the family of indexes we are considering is:
#
#   sum(Ni * Pi) / sum(Di * Pi)
#
#Where Ni is a set of numerator weights, and Di are denominator weights.
#These are collected globally into the W set.
#Note that with this generic formula it is possible to reproduce common
#indexes like NDVI.
#
#The general structure of the code is:
#
# 0) assign random values to the weights
# 1) for each plot
#   1a) compute the candidate index for all pixels
#   1b) compute the average over the plot
# 2) compute RMSE(phenotype, index)
# 3) compute derivative D := dRMSE / dW
# 4) update W := W - Lr * D
# 5) stop condition? If not, to 1)
#
#With Lr is the learning rate.
#To compute the derivative D
