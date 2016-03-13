library(ggplot2)
library(plyr)

data(diamonds)
?diamonds
names(diamonds)
range(diamonds$depth)

ggplot(aes(x = price, y = x), data = diamonds) +
  geom_point(color = "cornflowerblue", alpha = 0.2)

cor.test(diamonds$price, diamonds$x)
cor.test(diamonds$price, diamonds$y)
cor.test(diamonds$price, diamonds$z)

ggplot(aes(x = price, y = z), data = diamonds) +
  geom_point(color = "coral", alpha = 0.2)

ggplot(data = diamonds, aes(x = depth, y = price)) + 
  geom_point(alpha = .01) +
  scale_x_continuous(breaks = seq(43, 79, 2))

cor.test(diamonds$depth, diamonds$price)

ggplot(aes(x = price, y = carat), data = diamonds) +
  geom_point(color = 'coral', alpha = 0.2) +
  xlim(0, quantile(diamonds$price, 0.99)) +
  ylim(0, quantile(diamonds$carat, 0.99))

diamonds$volume = with(diamonds, x * y * z)
head(diamonds)

count(diamonds$volume == 0)
detach("package:plyr", unload=TRUE)

ggplot(aes(x = price, y = volume), data = diamonds) +
  geom_point(color = "coral", alpha = 0.2)

d1 <- subset(diamonds, volume > 0 & volume < 800)

cor.test(d1$volume, d1$price)

ggplot(aes(x = price, y = volume), data = d1) +
  geom_point(color = "coral", alpha = 0.1) +
  geom_smooth(method = 'lm', color = 'seagreen')

library(dplyr)

diamondsByClarity <- diamonds %>%
  group_by(clarity) %>%
  summarize(mean_price = mean(price),
            median_price = median(price),
            min_price = min(price),
            max_price = max(price),
            n = n()) %>%
  arrange(clarity)

diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))
p1 <- ggplot(aes(x = clarity, y = mean_price), data = diamonds_mp_by_clarity) +
  geom_bar(stat = "identity")  

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))
p2 <- ggplot(aes(x = color, y = mean_price), data = diamonds_mp_by_color) +
  geom_bar(stat = "identity")  

grid.arrange(p1, p2, ncol = 1)
