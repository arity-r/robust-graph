library(reshape2)
library(ggplot2)

# reading and formatting csv for ggplot
data = read.csv('speed_comparison.csv')
xcol = head(colnames(data), n=1)
ycol = tail(colnames(data), n=-1)
data <- melt(data, id.vars = xcol, measure.vars = ycol)

# ggplot
ggplot(data, aes(x=t, y=value, colour=as.factor(variable))) +
  geom_line(aes(group=variable)) +
  #geom_smooth(se=TRUE, aes(colour=variable), size=0.5) +
  xlab(expression(italic('swaps'))) + ylab(expression(italic('R'))) + # setting x and y labels
  labs(colour='Algorithm') + # setting legend title
  theme(text = element_text(size=16))
