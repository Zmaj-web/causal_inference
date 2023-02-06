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

doubleValue <- function(x){
  return(x * 2)
}

doubleValue(5)

# help
?sqrt

2:7

vector <- c(2:7)
vector[1:4]

X <- matrix(
  c(1:8),
  nrow = 4
)

X

#       [,1] [,2]
# [1,]    1    5
# [2,]    2    6
# [3,]    3    7
# [4,]    4    8

class(X)

XT <- matrix(
  c(1:8),
  ncol = 4
)

XT 

#       [,1] [,2] [,3] [,4]
# [1,]    1    3    5    7
# [2,]    2    4    6    8


XT_horizon <- matrix(
  c(1:8),
  ncol = 4,
  byrow = T
)

XT_horizon 

#       [,1] [,2] [,3] [,4]
# [1,]    1    2    3    4
# [2,]    5    6    7    8

X_named <- matrix(
  c(1:8),
  ncol = 4,
  byrow = T,
  dimnames = list(c("row1", "row2"), c("col1", "col2", "col3", "col4"))
)

X_named

#       col1 col2 col3 col4
# row1    1    2    3    4
# row2    5    6    7    8

df <- data.frame(
  X = c(1:4),
  Y = c("a", "b", "c", "d")
)

df

#   X Y
# 1 1 a
# 2 2 b
# 3 3 c
# 4 4 d

class(df)
ncol(df) # 2
nrow(df) # 4

# extract row
df$X # 1 2 3 4

# matrix to dataframe
df_by_X <- as.data.frame(X)
df_by_X

#   V1 V2
# 1  1  5
# 2  2  6
# 3  3  7
# 4  4  8

# dataframe to matrix
as.matrix(df)

#       X   Y  
# [1,] "1" "a"
# [2,] "2" "b"
# [3,] "3" "c"
# [4,] "4" "d"

example_list <- list(
  df = df,
  X = X
)

example_list

# $df
#   X Y
# 1 1 a
# 2 2 b
# 3 3 c
# 4 4 d
# 
# $X
#       [,1] [,2]
# [1,]    1    5
# [2,]    2    6
# [3,]    3    7
# [4,]    4    8

example_list$df

#   X Y
# 1 1 a
# 2 2 b
# 3 3 c
# 4 4 d