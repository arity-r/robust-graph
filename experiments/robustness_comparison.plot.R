library(reshape2)
library(ggplot2)

# reading and formatting csv for ggplot
data = read.csv('experiment1.result.csv')[1:50,]
xcol = head(colnames(data), n=1)
ycol = tail(colnames(data), n=-1)
data <- melt(data, id.vars = xcol, measure.vars = ycol)

# ggplot
ggplot(data, aes(x=q, y=value, colour=as.factor(variable))) +
  geom_line(aes(group=variable)) +
  xlab(expression(italic('q'))) + ylab(expression(italic('S(q)'))) + # setting x and y labels
  labs(colour='opt algorithm') + # setting legend title
  theme(text = element_text(size=16))
