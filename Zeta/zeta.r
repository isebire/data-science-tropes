# Code for getting zeta diversity and exporting as csv

library("zetadiv")

# Read dataframe from csv into correct format
data.tropes <- read.csv(file='/Users/izzy/Desktop/UNI/ECM3401 Individual Literature Review and Project/zeta diversity/matrices/vg_zeta_data_1990.0.csv')
drops <- c("X", "country")
data.tropes = data.tropes[ , !(names(data.tropes) %in% drops)]

zeta.tropes <- Zeta.decline.mc(data.tropes, orders=1:10)


zdata <- list(zeta.tropes[["zeta.order"]], zeta.tropes[["zeta.val"]], zeta.tropes[["zeta.val.sd"]])
zdf <- as.data.frame(zdata, col.names = c('order', 'value', 'sd'))
write.csv(zdf, 'Desktop/ZETA_RESULTS/vg_zeta_1990.csv')
