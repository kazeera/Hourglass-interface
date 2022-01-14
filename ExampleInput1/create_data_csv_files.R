# This script makes the 3 files to test package
library(kazutils)
library(dplyr)

# Make output directory
out_dir <- create_folder("csv files")

# Make numeric matrix
mat <- matrix(rnorm(400), nrow = 20, ncol = 40)
colnames(mat) <- paste0("Gene", 1:40) #rownames(sc)[400:419] %>% toupper()
rownames(mat) <- paste0("Patient", 1:20)

# Make annotations
# Row annotations describe mat's rows (patients)
rowAnn <- data.frame(Smoker = rep(c("Yes", "No", NA), c(8, 11, 1)) %>% sample,
                     Age = sample(35:70, 20, T),
                     Sex = rep(c("M", "F", "X"), c(9, 10, 1)) %>% sample,
                     Cancer.Type = rep(c("Lung", "Stomach", "Mouth", "Brain", NA), c(4,6,5,4,1)) %>% sample,
                     row.names = rownames(mat)
)

# Column annotations describes mat's columns
colAnn <- data.frame(Gene.Sym = colnames(mat), 
                     Parameter = rep(c("RNA.Abundance", "Pixel.Intensity"), 20) %>% sample,
                     Gene.ID = sample(1000:2000, 40),
                     row.names = colnames(mat)
)

# Write to file
write.csv(mat, sprintf("%s/numeric_matrix.csv", out_dir), row.names = T)
write.csv(colAnn, sprintf("%s/column_annotations.csv", out_dir), row.names = T)
write.csv(rowAnn, sprintf("%s/row_annotations.csv", out_dir), row.names = T)

# Write to Excel file
library(openxlsx)
wb <- createWorkbook()
write_df_to_Excel("mat", mat, wb, incl_rownames = T)
write_df_to_Excel("rowAnn", rowAnn, wb, incl_rownames = T)
write_df_to_Excel("colAnn", colAnn, wb, incl_rownames = T)
saveWorkbook(wb, "data.xlsx", overwrite = T)
