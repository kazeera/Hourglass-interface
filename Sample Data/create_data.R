
library(dplyr)

# Make numeric matrix
mat <- matrix(rnorm(200), nrow = 10, ncol = 20)
colnames(mat) <- paste0("GENE", 1:20) #rownames(sc)[400:419] %>% toupper()
rownames(mat) <- paste0("Patient", 1:10)

# Make annotations

# Row annotations describe mat's rows (patients)
rowAnn <- data.frame(Smoker = rep(c("Yes", "No"), c(4,6)) %>% sample,
                     Age = sample(35:70, 10, T),
                     row.names = rownames(mat)
)


# Column annotations describes mat's columns
x <- sample(35:70, 10, T)
factor(x, labels=c("30-40", "41-50", "51-60", "60-70"))
