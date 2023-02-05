x1 <- c(74, 61, 42, 57, 33)
y1 <- c(84, 51, 22, 77, 43)
df1 <- data.frame(x1, y1)
df1

head(df1)
summary(df1)
# row.names: index number
write.csv(x=df1, file = "./data/sample.csv", row.names = FALSE)

df2 <- read.csv(file = "./data/sample.csv")
df2
