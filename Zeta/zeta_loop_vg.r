# Code for getting zeta diversity and exporting as csv

library("zetadiv")

years <- seq.int(1990, 2021)

for (year in years) {

  # Read dataframe from csv into correct format
  filename1a <- paste("/Users/izzy/Desktop/UNI/ECM3401 Individual Literature Review and Project/zeta diversity/matrices/vg_zeta_data_", year, sep="")
  filename1 <- paste(filename1a, '.0.csv', sep="")

  data.tropes <- read.csv(file=filename1)

  numlocations <- max(data.tropes$X) + 1

  drops <- c("X", "country")
  data.tropes = data.tropes[ , !(names(data.tropes) %in% drops)]

  zeta.tropes <- Zeta.decline.mc(data.tropes, orders=1:numlocations)
  # save the figure?

  zdata <- list(zeta.tropes[["zeta.order"]], zeta.tropes[["zeta.val"]], zeta.tropes[["zeta.val.sd"]])
  zdf <- as.data.frame(zdata, col.names = c('order', 'value', 'sd'))
  filename2a <- paste('Desktop/ZETA_RESULTS/vg_zeta_', year, sep="")
  filename2 <- paste(filename2a, '.csv', sep="")
  write.csv(zdf, filename2)

}
