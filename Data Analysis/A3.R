setwd(“~/A3”)
d=read.csv("NFLdraft.csv", head=T, strip.white=T, stringsAsFactors=F)   #1 #(a)read my data
d$Pos[d$Pos=="LS"]="C"                                                  #(b) remove LS-->C
ind1=d$Pos  %in% c("fC", "OG", "OT", "TE", "DT", "DE")                  #(c) categorize my data Pos
d$Pos2[ind1]="Linemen"                      #index all players in the accordingly category and name it
ind2=d$Pos %in% c("CB", "WR", "FS")
d$Pos2[ind2]="Small Backs"
d$Pos2[!ind1 ^ !ind2]="Big Back"
Pos<-factor(d$Pos2)                            #create a new factor for d$Pos with 3 categories
#(d) substract - from the data and apply some math to change its unit
d$Ht=as.numeric(substr(d$Ht,1,1))*12+as.numeric(substr(d$Ht,3,4))       
first=strsplit(d$Drafted," / ",fixed = TRUE)   #remove / from the Drafted data
first=unlist(first)                             #unlist data
add=matrix(first,nrow(d),4,byrow = TRUE)        #put my data in matrix form, with 4 columns and 212 rows
colnames(add)<-c("Pro","round","pick","year")   #name my columns
d=cbind(d,add)                                  #coombine my data to the original data
d$round=as.numeric(substr(d$round,1,1))         # turn data in numerial form
d$pick=as.numeric(gsub("[^0-9]","",x=d$pick))   #remove all non number elements from data pick
rm(ind1,ind2, Pos)

###############Assignment 3##################
#1. 
df <- d[complete.cases(d),]
full <- lm (Cone3 ~ Ht + Wt + Yd40 + Vertical + Bench + Broad + Shuttle, data = df)
par(mfrow=c(1, 2))
plot(full, 1)
plot(full, 2)
#2 
summary(full)
anova(full)
fit2 <- lm (Cone3 ~  Wt + Yd40 + Vertical + Bench + Broad + Shuttle, data = df)
summary(fit2)
fit3 <- lm (Cone3 ~  Wt + Yd40 + Vertical + Broad + Shuttle, data = df)
summary(fit3)
fit4 <- lm (Cone3 ~  Wt + Yd40 + Vertical + Shuttle, data = df)
summary(fit4)
fit5 <- lm (Cone3 ~  Wt + Yd40 + Shuttle, data = df)
summary(fit5)
reduced <- lm(Cone3 ~ Yd40 + Shuttle, data = df)
summary(reduced)  #Show this table
summary(full)
anova(full)
anova(reduced)
(2.6857-2.5539)/5/0.0246
#3.
anova(reduced, full)
#4
(as.numeric(anova(reduced)[3,2]) - as.numeric(anova(full)[8,2])) /as.numeric(anova(reduced)[3,2])
#5. 
dn <- d[complete.cases(d[,c(5:8,10:12)]),]
fit6 <- lm(Cone3 ~ Yd40 + Shuttle + Wt, data=dn)
summary(fit6)
rm(fit2, fit3, fit4, fit5, fit6, full)

#########################Part B#############################
dB = read.csv("Denver.csv", head=T, strip.white=T, stringsAsFactors=F)
#1
pairs(dB)
ind <- which((dB[6]==max (dB[6])) | (dB[2] == max (dB[2])))
dB <- dB[-ind, ]
#2
round(cor(dB),3)
#3
require(car)
full <- lm (dB$crime_chg_per ~ dB$pop_1000 + dB$pop_chg_per + dB$child_per + dB$lunch_part_per +dB$house_inc_chg_per +dB$crime_rate_per1000)
VIF <- as.data.frame(vif(full))
Summary <- as.data.frame(summary(full)$coefficients)
Summary$VIF <- c(NA, VIF$`vif(full)`)
Summary
#4
par(mfrow=c(1, 2))
plot(full,1)
plot(full,2)
#Do you see any problems here? If so, describe what you see.
hist(full$residuals, breaks = 30)
#5
reduced <- lm (dB$crime_chg_per ~ dB$child_per + dB$lunch_part_per + dB$crime_rate_per1000)
summary(reduced)
anova(reduced, full)
#7
interact <- lm (crime_chg_per ~ child_per * lunch_part_per * crime_rate_per1000, data = dB)
anova(reduced,interact)
#8
reduced <- lm(crime_chg_per ~ child_per + lunch_part_per + crime_rate_per1000, data= dB)
n = data.frame(child_per= 25 , lunch_part_per = 55, crime_rate_per1000 = mean(dB$crime_rate_per1000))
predict(reduced, n, interval = "prediction")
