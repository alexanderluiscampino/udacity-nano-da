setwd("~/src/udacity-nano-da-04")

library(ggplot2)
data("diamonds")
names(diamonds)

ggplot(aes(x = price), data = diamonds) +
  geom_histogram(aes(fill = cut), binwidth = 1000) +
  facet_wrap(~color) +
  scale_fill_brewer(type = "qual")

ggplot(aes(x = table, y = price), data = diamonds) +
  geom_point(aes(color = cut)) +
  scale_colour_brewer(type = "qual")

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z

ggplot(aes(x = volume, y = price), data = diamonds) +
  geom_point(aes(color = clarity)) +
  scale_y_log10() +
  scale_colour_brewer(type = "qual") +
  xlim(0, quantile(diamonds$volume, 0.99))

# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.
ggplot(aes(x = cut, y = price / carat), data = diamonds) +
  geom_point(aes(color = color), position = position_jitter()) +
  facet_wrap(~clarity) +
  scale_colour_brewer(type = 'div')

pf <- read.delim('pseudo_facebook.tsv')
names(pf)
head(pf)

pf$prop_initiated <- pf$friendships_initiated / pf$friend_count
pf$year_joined <- floor(2014 - (pf$tenure / 365))
pf$year_joined.bucket <- cut(
  pf$year_joined, 
  breaks = c(2004, 2009, 2011, 2012, 2014))

ggplot(aes(x = tenure, y = prop_initiated), data = pf) +
  geom_line(aes(color = year_joined.bucket),
            stat= 'summary',
            fun.y = median)

# Smooth the last plot you created of
# of prop_initiated vs tenure colored by
# year_joined.bucket. You can bin together ranges
# of tenure or add a smoother to the plot.

ggplot(aes(x = tenure, y = prop_initiated), data = pf) +
  geom_smooth(aes(color = year_joined.bucket))

pfs <- subset(pf, year_joined.bucket == "(2012,2014]")
summary(pfs)
