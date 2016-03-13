library(ggplot2)
library(xlsx)
library(dplyr)
library(reshape2)

setwd("~/src/udacity-nano-da-04")

comp <- read.xlsx("indicator_hour compensation.xlsx", sheetIndex = 1)
head(comp)

colnames(comp)[1] <- "country"
comp$NA. <- NULL
years <- colnames(comp)[seq(2, dim(comp)[2], 1)]

coml <- melt(
  comp,
  id.vars = "country",
  variable.name = "year",
  value.name = "compensation")

coml$year <- as.integer(substr(coml$year, 2, 5))

head(coml)
row.names(coml)
summary(coml)

# Only subset selected countries.

countries = c(
  "France",
  "Germany",
  "Sweden",
  "United Kingdom",
  "United States",
  "Russia")

coms <- subset(coml, country %in% countries & !is.na(compensation))

coms.comp_by_country.wide <- dcast(
  coms,
  year + compensation ~ country,
  value.var = "country"
)

head(coms)
head(coms.comp_by_country.wide)

# Mean and median compensation for all countrues
ggplot(coms.comp_by_country.wide,
       aes(x = year, y = compensation)) +
  geom_line(stat = 'summary', fun.y = 'median', color = 'coral') +
  geom_line(stat = 'summary', fun.y = 'mean', color = 'cornflowerblue')

ggsave('ps4-comp-mean-and-median.png')

# Compensation by year faceted by country
ggplot(aes(x = year, y = compensation), data = coms) + 
  geom_line() +
  facet_wrap(~country)

ggsave('ps4-comp-facet-by-country.png')
