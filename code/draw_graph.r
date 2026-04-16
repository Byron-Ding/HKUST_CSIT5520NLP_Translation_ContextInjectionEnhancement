# library 不存在则安装
if (!require("ggplot2")) {
  install.packages("ggplot2")
}
if (!require("readr")) {
  install.packages("readr")
}

library(ggplot2)
library(readr)


# separator , header TRUE, stringsAsFactors FALSE
df <- read_csv("result/analysis_results.csv",
                
                col_names = TRUE
)

ggplot(df, aes(x = WordType, y = AverageNonSimilarWordLength, fill = Condition)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Average Non-Similarity Word Length by WordType and Condition",
       x = "WordType", y = "Average NonSimilar WordLength") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


ggplot(df, aes(x = Condition, y = AverageNonSimilarWordLength, group = WordType, color = WordType)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Average Non-Similarity Word Length Trends by Condition",
       x = "Condition", y = "Average NonSimilar WordLength")
