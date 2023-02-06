# install packages

install.packages("xts") # data type in Time Anal.
install.packages("forecast") # make and predict model
install.packages("urca") # unit root test(stationarity T/F)
install.packages("ggplot2") # draw a graph
install.packages("ggfortify")

library(xts)
library(forecast)
library(urca)
library(ggplot2)
library(ggfortify)

ts_sample <- ts(
  1:36,
  start = c(2000, 1),
  freq = 12
)
ts_sample
