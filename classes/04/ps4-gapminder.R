library(ggplot2)
library(xlsx)
install.packages("dplyr")
library(dplyr)

setwd("~/src/udacity-nano-da-04")

comp <- read.xlsx("indicator_hour compensation.xlsx", sheetIndex = 1)
head(comp)

colnames(comp)[1] <- "country"
comp$NA. <- NULL

dim(comp)[2]
years <- colnames(comp)[seq(2, dim(comp)[2], 1)]

coml <- reshape(
  comp,
  varying = years,
  v.names = "compensation",
  times = years,
  timevar = "year",
  direction = "long")

head(coml)
row.names(coml)
summary(coml)

row.names(coml) <- seq(1, dim(coml)[1], 1)
coml$year <- as.integer(substr(coml$year, 2, 5))
coml$id <- NULL

# Only subset selected countries.

countries = c(
  "France",
  "Germany",
  "Sweden",
  "United Kingdom",
  "United States",
  "Russia")

coms <- subset(coml, country %in% countries & !is.na(compensation))

head(coms)
tail(coms)

# Boxplot of compensations by year for selected countries.
ggplot(coms,
       aes(x = factor(year), y = compensation)) +
  geom_boxplot()

ggsave("ps4-comp-boxplot.png")

# Calculate mean compensation by year.

coms.mean_by_year <- coms %>%
  group_by(year) %>%
  summarize(compensation_mean = mean(compensation),
            compensation_median = median (compensation),
            n = n()) %>%
  arrange(year)

head(coms.mean_by_year)
tail(coms.mean_by_year)

# Plot compensation by year and country.

ggplot(data = coms,
       aes(x = year, y = compensation)) +
  geom_line(aes(color = country)) +
  scale_x_continuous(breaks = seq(1980, 2006, 5))

ggsave("ps4-comp-lines.png")

# Add mean and median to the plot by year and country.
ggplot(data = coms,
       aes(x = year, y = compensation)) +
  geom_line(aes(color = country)) +
  scale_x_continuous(breaks = seq(1980, 2006, 5)) +
  geom_line(stat = 'summary', fun.y = mean, linetype = 2, color = 'blue') +
  geom_line(stat = 'summary', fun.y = median, linetype = 2, color = 'red')

ggsave("ps4-comp-lines-with-mean.png")
