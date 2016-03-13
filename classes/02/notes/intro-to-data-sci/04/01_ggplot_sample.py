# -*- coding: utf-8 -*-
from ggplot import ggplot, aes, geom_point, geom_line, ggtitle, xlab, ylab

data = []
xvar = 'X'
yvar = 'Y'

print ggplot(
    data,
    aes(x='yearID', y='HR')) + \
      geom_point(color='red') + \
      geom_line(color='red') + \
      ggtitle('Number of HR by year') + \
      xlab('Year') + \
      ylab('Number of HR')
