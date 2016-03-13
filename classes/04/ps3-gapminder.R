install.packages("ggplot2")
library(ggplot2)
library(dplyr)

?reshape

setwd("~/src/udacity-nano-da-04")

install.packages("xlsx", type = "source")
library(xlsx)

aac <- read.xlsx("indicator_air accident killed.xlsx", sheetIndex = 1)

head(aac)
colnames(aac)
colnames(aac)[1] <- "Country"
aac$NA. <- NULL

years <- colnames(aac)[seq(2, 40, 1)]

aal <- reshape(
  aac,
  varying = years,
  v.names = "Killed",
  times = years,
  timevar = "Year",
  direction = "long")

head(aal)
tail(aal)
row.names(aal) <- seq(1, dim(aal)[1], 1)
row.names(aal)
aal$Year <- as.numeric(substr(aal$Year, 2, 5))
aal$id <- NULL

countries = c(
  "France",
  "Germany",
  "Sweden",
  "United Kingdom",
  "United States",
  "Russia")

aas <- subset(aal, Country %in% countries & Killed > 0)

qplot(Killed,
      data = aas,
      geom = "freqpoly",
      color = Country,
      binwidth = 50)

ggsave("ps3-aeroplane-accidents-freq.png")

qplot(x = Year,
      y = Killed,
      data = aas,
      color = Country)

ggsave("ps3-aeroplane-accidents-by-year.png")
