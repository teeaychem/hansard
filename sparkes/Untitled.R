library(tidyverse)
library(lme4)
library(languageR)
library(plyr) # for figuring out percentages

# For whatever reason, RStidio has troubles with figuring out where stuff is.
# The following commands set the current file path as the working directory.
currentDir = dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(currentDir)
getwd()

#load up the example CSV
p = read.csv("../declan/qbank.csv")
head(p)
summary(p)

table(p$memName, p$memPart)
table(p$memAffi)
table(p$memPart)
table(p$memPart, p$followup)
table(p$memAffi, p$followup)
table(p$Question)
summary(p)

p$memPart["Respect"]


q = read.csv("../sparkes/altqbank.csv")
summary(q)
table(q$memPart)
table(q$memAffi)

q %>% replace(is.na(.), 0) %>% summarise_each(funs(sum))
qs = colSums(Filter(is.numeric, q), na.rm=TRUE)
qs
summary(qs)
table(qs)
write.table(qs, "../sparkes/etc.csv", sep=",")
