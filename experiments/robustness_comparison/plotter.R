library(reshape2)
library(ggplot2)

# reading and formatting csv for ggplot
data = read.csv('result.csv')[1:50,]
xcol = head(colnames(data), n=1)
ycol = tail(colnames(data), n=-1)
data <- melt(data, id.vars = xcol, measure.vars = ycol, na.rm=TRUE)

# ggplot
ggplot(data, aes(x=q, y=value, colour=as.factor(variable))) +
  geom_line(aes(group=variable)) +
  xlab(expression(italic('q'))) + ylab(expression(italic('S(q)'))) + # setting x and y labels
  labs(colour='opt type') + # setting legend title
  scale_colour_discrete(breaks=c('original', # setting order of legend
                                 'greedy',
                                 'onion',
                                 'new.100.swaps',
                                 'new.1000.swaps'),
                        labels=c('original', # setting label of legend
                               'greedy',
                               'onion',
                               'our method, 100 swaps',
                               'our method, 1000 swaps')) +
  theme(text = element_text(size=16))
