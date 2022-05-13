library(tidyverse)
library(readr)

games <- read_csv("data/games.csv")
participants <- read_csv("data/participants.csv")
players <- read_csv("data/players.csv")
queue_mappings <- read_csv("data/queue_mappings.csv")

players <- players %>% merge(queue_mappings)
games <- games %>% rename(game_id=id)
full <- participants %>% 
  merge(games) %>% 
  merge(players) %>%
  mutate(
    gold_spent_per_s=gold_spent/game_duration,
    damage_per_s=total_damage_dealt_to_champions/game_duration,
    kills_per_s=kills/game_duration,
    deaths_per_s=deaths/game_duration,
  )
champs_per_game <- participants %>% 
  select(game_id, blue_side, champ_name) %>%
  mutate(champ=TRUE, champ_name=ifelse(
    blue_side, 
    paste("blue", champ_name, sep="_"), 
    paste("red", champ_name, sep="_")
  )) %>%
  select(-blue_side) %>%
  spread(champ_name, champ, fill=FALSE) %>%
  print(n=10)

full_pre_game <- full %>% select(
  game_id, queue_id, champ_name, blue_side, lane, role, game_version, tier, win
)
full <- full %>% merge(champs_per_game)
full_pre_game <- full_pre_game %>% merge(champs_per_game)

wins_by_champ <- full %>% 
  group_by(champ_name, win) %>% 
  summarise(count=n()) %>%
  ungroup() %>%
  mutate(win=factor(ifelse(win, "wins", "losses"))) %>%
  spread(win, count) %>% 
  mutate(count=n()) %>%
  filter(wins > 0 & losses > 0) %>%
  group_by(champ_name) %>%
  mutate(
    win_rate=wins/(wins+losses),
    lower_95_ci=binom.test(x=wins, n=wins + losses, conf.level=1-pbinom(0, count, 0.05))["conf.int"][[1]][1],
    upper_95_ci=binom.test(x=wins, n=wins + losses, conf.level=1-pbinom(0, count, 0.05))["conf.int"][[1]][2]
  ) %>%
  select(-count) %>%
  arrange(desc(lower_95_ci)) %>%
  print(n=Inf)

library(caret)
library(rpart)
library(rpart.plot)
library(rattle)
library(randomForest)

set.seed(123)
size <- floor(0.9 * nrow(games))
# test data could cheat with game information
train_indices <- sample(seq_len(nrow(games)), size=size)
train_games <- games[train_indices,"game_id"][["game_id"]]
test_games <- games[-train_indices,"game_id"][["game_id"]]

train_data <- full_pre_game %>% 
  subset(game_id %in% train_games) %>%
  select(-game_id) %>%
  filter(tier != "DIAMOND")
test_data <- full_pre_game %>% 
  subset(game_id %in% test_games) %>% 
  select(-game_id) %>%
  filter(tier != "DIAMOND")
train_full_data <- full %>% 
  subset(game_id %in% train_games) %>%
  select(-game_id) %>%
  filter(tier != "DIAMOND")
test_full_data <- full %>% 
  subset(game_id %in% test_games) %>% 
  select(-game_id) %>%
  filter(tier != "DIAMOND")

bt <- rpart(win ~ ., data=train_data, method="class")
fancyRpartPlot(bt)
pred <- predict(bt, test_data, type="class")
confusionMatrix(table(pred, test_data$win))

rf <- randomForest(win ~ ., data=train_data, ntree=40)
pred <- predict(rf, test_data, type="class")
confusionMatrix(table(pred > 0.5, test_data$win))
varImpPlot(rf)
