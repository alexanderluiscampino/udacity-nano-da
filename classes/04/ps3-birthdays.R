library(ggplot2)
install.packages("lubridate")
library(lubridate)
library(plyr)

setwd("~/src/udacity-nano-da-04")

bd <- read.csv("birthdaysExample.csv")

head(bd)
bd$dates <- mdy(bd$dates)
?strptime

bd$day <- as.numeric(strftime(bd$dates, format = "%d"))
bd$month <- as.numeric(strftime(bd$dates, format = "%m"))
bd$year <- as.numeric(strftime(bd$dates, format = "%Y"))
bd$year_day <- as.numeric(strftime(bd$dates, format = "%j"))

range(bd$year_day)

# Which day of the year has the most number of birthdays?

t1 <- count(bd, c("year_day"))
max_bdays <- max(t1$freq)
max_bday_days <- t1[t1$freq == max_bdays,]

# Days 36, 141, and 196

# Do you have at least 365 friends that have birthdays on everyday
# of the year?
qplot(year_day,
      data = bd,
      xlab = "Day of year",
      ylab = "Number of birthdays",
      binwidth = 1) +
  scale_x_discrete(breaks = seq(0, 365, 20))

# No. There are days with 0 birthdays in the chart.

ggsave("ps3-bd-by-doy.png")

# Which month contains the most number of birthdays?

t2 <- count(bd, c("month"))
max_bdays_in_month <- max(t2$freq)
max_bday_months <- t2[t2$freq == max_bdays_in_month,]

# Month #3 (March) contains most birthdays (98).
qplot(month,
      data = bd,
      xlab = "Month",
      ylab = "Number of birthdays",
      binwidth = 1) +
  scale_x_discrete(lim = c(1, 12))

ggsave("ps3-bd-by-month.png")
