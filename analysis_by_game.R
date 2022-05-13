library(tidyverse)
library(readr)

raw.games <- read_csv("data/games.csv")
raw.participants <- read_csv("data/participants.csv")
raw.players <- read_csv("data/players.csv")
raw.queue_mappings <- read_csv("data/queue_mappings.csv")

solo_queue_games <- raw.games %>%
  filter(queue_id == 420) %>%
  select(id)

ranks <- raw.players %>%
  filter(queue_type == 'RANKED_SOLO_5x5') %>%
  select(summoner_id, tier) %>%
  mutate(tier=case_when(
    tier == 'IRON' ~ 0,
    tier == 'BRONZE' ~ 1,
    tier == 'SILVER' ~ 2,
    tier == 'GOLD' ~ 3,
    tier == 'PLATINUM' ~ 4,
    tier == 'DIAMOND' ~ 5,
    tier == 'MASTER' ~ 6,
    tier == 'GRANDMASTER' ~ 7,
    tier == 'CHALLENGER' ~ 8
  )) %>%
  merge(raw.participants, how='right') %>%
  group_by(game_id) %>%
  summarise(avg_tier=mean(tier))

champs <- raw.participants %>%
  mutate(
    champ_name=as.factor(champ_name),
    filled_role=as.factor(case_when(
      index == 0 ~ "BLUE_TOP",
      index == 1 ~ "BLUE_JUNGLE",
      index == 2 ~ "BLUE_MIDDLE",
      index == 3 ~ "BLUE_BOTTOM",
      index == 4 ~ "BLUE_SUPPORT",
      index == 5 ~ "RED_TOP",
      index == 6 ~ "RED_JUNGLE",
      index == 7 ~ "RED_MIDDLE",
      index == 8 ~ "RED_BOTTOM",
      index == 9 ~ "RED_SUPPORT",
    ))
  ) %>%
  select(game_id, filled_role, champ_name) %>%
  spread(filled_role, champ_name)

blue_side_win <- raw.participants %>%
  filter(index < 5) %>%
  mutate(blue_side_win=as.factor(win)) %>%
  select(game_id, blue_side_win) %>%
  distinct()

data <- solo_queue_games %>%
  mutate(game_id=id) %>%
  select(-id) %>%
  merge(champs, how='left') %>%
  merge(blue_side_win, how='left') %>%
  merge(ranks, how='left') %>%
  select(-game_id)


library(caret)
library(rpart)
library(rattle)
library(randomForest)
set.seed(123)
size <- floor(0.8 * nrow(data))
train_indices <- sample(seq_len(nrow(data)), size=size)
train_data <- data[train_indices,]
test_data <- data[-train_indices,]

# Binary Tree
bt <- rpart(blue_side_win ~ ., data=train_data, method="class")
fancyRpartPlot(bt)
pred <- predict(bt, test_data, type="class")
confusionMatrix(table(pred, test_data$blue_side_win))

# Random Forest
rf <- train(
  blue_side_win ~ ., 
  data=train_data, 
  method="ranger",
  importance='impurity'
)
varImp(rf)
pred <- predict.train(rf, test_data)
confusionMatrix(table(pred, test_data$blue_side_win))

# TODO: Gradient Boosting

# TODO: Naive Bayes


