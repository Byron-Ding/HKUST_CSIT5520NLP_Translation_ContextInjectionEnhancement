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
df$Condition <- factor(df$Condition,
                        levels = c("No Synonyms; No Rules", "With Synonyms; No Rules", "No Synonyms; With Rules", "With Synonyms; With Rules")
)


average_similarity_trends_line_plot <- ggplot(df, aes(x = Condition, y = AverageSimilarity, group = WordType, color = WordType)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Average Similarity Trends by Condition",
       x = "Condition", y = "Average Similarity")
View(average_similarity_trends_line_plot)
ggsave(average_similarity_trends_line_plot,
  filename = "result/img/average_similarity_trends_line_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)
average_similarity_bar_plot <- ggplot(df, aes(x = WordType, y = AverageSimilarity, fill = Condition)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Average Similarity by WordType and Condition",
       x = "WordType", y = "Average Similarity") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
View(average_similarity_bar_plot)
ggsave(average_similarity_bar_plot,
  filename = "result/img/average_similarity_bar_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)


word_number_bar_plot <- ggplot(df, aes(x = WordType, y = WordNumber, fill = Condition)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Word Number by WordType and Condition",
       x = "WordType", y = "Word Number") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
View(word_number_bar_plot)
ggsave(word_number_bar_plot,
  filename = "result/img/word_number_bar_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)

word_number_line_plot <- ggplot(df, aes(x = Condition, y = WordNumber, group = WordType, color = WordType)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Word Number Word Length Trends by Condition",
       x = "Condition", y = "Word NumberWordLength")
View(word_number_line_plot)
ggsave(word_number_line_plot,
  filename = "result/img/word_number_line_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)


average_non_similar_word_length_bar_plot <- ggplot(df, aes(x = WordType, y = AverageNonSimilarWordLength, fill = Condition)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Average Non-Similarity Word Length by WordType and Condition",
       x = "WordType", y = "Average NonSimilar WordLength") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
View(average_non_similar_word_length_bar_plot)
ggsave(average_non_similar_word_length_bar_plot,
  filename = "result/img/average_non_similar_word_length_bar_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)

average_non_similar_word_length_line_plot <- ggplot(df, aes(x = Condition, y = AverageNonSimilarWordLength, group = WordType, color = WordType)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Average Non-Similarity Word Length Trends by Condition",
       x = "Condition", y = "Average NonSimilar WordLength")
View(average_non_similar_word_length_line_plot)
ggsave(average_non_similar_word_length_line_plot,
  filename = "result/img/average_non_similar_word_length_line_plot.png",
  width = 8,
  height = 6,
  dpi = 600
)
