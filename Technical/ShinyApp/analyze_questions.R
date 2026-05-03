# Analyze questions breakdown
library(tidyverse)

q <- read_csv('data/shaikh_tonak_questions.csv', show_col_types = FALSE)

cat('\n====================================\n')
cat('QUESTIONS ANALYSIS\n')
cat('====================================\n\n')

cat('Total Questions:', nrow(q), '\n\n')

cat('Questions by Category:\n')
print(table(q$Category))

cat('\nQuestions by Priority:\n')
print(table(q$Priority))

cat('\nTarget Tabs:\n')
print(table(q$Target_Tab))

cat('\n====================================\n')
cat('Sample Questions:\n')
cat('====================================\n\n')

for (i in c(1, 9, 17, 22, 28)) {
  cat(sprintf('Q%d [%s | %s]: %s\n',
              q$Question_Number[i],
              q$Priority[i],
              q$Category[i],
              q$Question[i]))
}

cat('\n====================================\n')
