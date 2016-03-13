data(diamonds)

qplot(price, data = diamonds, binwidth = 1000)

qplot(price,
      data = diamonds,
      binwidth = 500,
      xlim = c(0, 5000))

qplot(price,
      data = diamonds,
      binwidth = 100) +
  facet_wrap(~cut)

qplot(x = price, data = diamonds) + facet_wrap(~cut, scales = "free_y")

qplot(x = price / carat,
      data = diamonds) +
  scale_x_log10() +
  facet_wrap(~cut) 

qplot(x = clarity,
      y = price,
      data = diamonds, 
      xlab = "Clarity",
      ylab = "Price",
      geom = 'boxplot') +
  coord_cartesian(ylim = c(600, 6100))

qplot(x = color,
      y = price / carat,
      data = diamonds, 
      xlab = "Color",
      ylab = "Price per carat",
      geom = 'boxplot') +
  coord_cartesian(ylim = c(600, 6100))

ggsave('ps3-diamonds-price-by-color.png')

qplot(carat, data = diamonds, binwidth = 0.01) +
  coord_cartesian(xlim = c(0, 1.6), ylim = c(2000, 2600)) +
  scale_x_continuous(breaks = seq(0, 1.6, 0.05))



ggsave('ps3-diamonds-price-by-color.png')
