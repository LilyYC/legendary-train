setwd("~/A1")
d=read.csv("NFLdraft.csv", head=T, strip.white=T, stringsAsFactors=F)   #1 #(a)read my data
d$Pos[d$Pos=="LS"]="C"                                                  #(b) remove LS-->C
ind1=d$Pos  %in% c("fC", "OG", "OT", "TE", "DT", "DE")                  #(c) categorize my data Pos
d$Pos2[ind1]="Linemen"                                                  #index all players in the accordingly category and name it
ind2=d$Pos %in% c("CB", "WR", "FS")
d$Pos2[ind2]="Small Backs"
d$Pos2[!ind1 ^ !ind2]="Big Back"
Pos<-factor(d$Pos2)                                                     #create a new factor for d$Pos with 3 categories
d$Ht=as.numeric(substr(d$Ht,1,1))*12+as.numeric(substr(d$Ht,3,4))       #(d) substract - from the data and apply some math to change its unit
first=strsplit(d$Drafted," / ",fixed = TRUE)   #remove / from the Drafted data
first=unlist(first)                             #unlist data
add=matrix(first,nrow(d),4,byrow = TRUE)        #put my data in matrix form, with 4 columns and 212 rows
colnames(add)<-c("Pro","round","pick","year")   #name my columns
d=cbind(d,add)                                  #coombine my data to the original data
d$round=as.numeric(substr(d$round,1,1))         # turn data in numerial form
d$pick=as.numeric(gsub("[^0-9]","",x=d$pick))   #remove all non number elements from data pick
tapply(d$pick, d$Pro, length)                                        #2a) table between my pick and Pro
d$CollegeTeam <- factor(d$CollegeTeam)                              #b)
CT1 <-d$CollegeTeam
CT2 <-factor(CT1, levels=levels(CT1)[order(-table(CT1))])
barplot(table(CT2))
f1 = factor(d$Pos)                              #c) factor my data Pos
f2 <- factor(f1, levels= levels(f1)[order(-table(f1))])   # make a new factor with level in an increasing order
barplot(table(f2), main="barplot between position and draft picks", 
        xlab="position", ylab="draft picks",ylim=c(0,30))
fivenum(d$Ht)                                   #d) 
mean(d$Ht)
hist(d$Ht, main="histogram of heights", xlab="heights")  #e) make a histogram
d$Name[d$Ht==min(d$Ht)]                                  #f)
d$Wt[d$Ht==min(d$Ht)] 
x1 <- d$Wt                                               #g)
y1 <- d$Yd40
plot(x1,y1, xlab="Weight(X)", ylab="Yd40(Y)", main="player's 40-yd dash time (Y) vs.  Weight (X)")
x2 <- d$Shuttle                                          #h)
y2 <- d$Cone3 
plot(x2,y2, main="3-Cone Drill Time vs. Shuttle Drill Time for 2015 NFL Draft Players",
     xlab="Shuttle Drill Time",ylab="3-Cone Drill Time", xlim=c(3.8,5),ylim=c(6.5,8.5))
f1 = factor(d$Pos)                                       #i)
plot(d$Shuttle[f1=="Linemen"],d$Cone3[f1=="Linemen"],
     pch=4,col="black", main="3-Cone Drill Time vs. Shuttle Drill Time for 2015 NFL Draft Players",
     xlab="Shuttle Drill Time(s)",ylab="3-Cone Drill Time(s)", xlim=c(3.8,5),ylim=c(6.5,8.5))
points(d$Shuttle[f1=="Big Back"],d$Cone3[f1=="Big Back"], pch=10,col="Red")
points(d$Shuttle[f1=="Small Backs"],d$Cone3[f1=="Small Backs"], pch=25,col="grey50")
legend(x=3.8,y=8.5,pch=c(10,4,25),text.width = 0.4, legend=c("Big Back(red)","Linemen(black)","Small Back(grey)"))
newx3 <- d$Bench[ind1]                          #j)
newy3 <- d$Broad[ind1]
plot(newx3,newy3, ylab="Broad jump score",xlab="Bench press score",
     main="linemen--Broad jump score vs. Bench press score")
d$Name[d$Broad==min(d$Broad, na.rm = T)]        #k)
d$Wt[d$Broad==min(d$Broad, na.rm = T)]
d[d$Name=="Austin Shepherd",]
d$Name[d$Broad==max(d$Broad, na.rm = T)]        #l) 
d[d$Name=="Byron Jones",]
model=lm(Cone3 ~ Shuttle, d = d)                #B 1)abc
summary(model)
model$coefficients
confint(model, level=0.92)                       
m=data.frame(Shuttle=4.5)                        #d)     
predict(model, newd= m, interval = "confidence")   
n=data.frame(Shuttle=4.7)                        #e)
predict(model, newd= n, interval = "prediction")
fit=lm(pick ~ Yd40, d = d)                       #2)
summary(fit)
fit2=lm(pick ~Broad, d=d)
summary(fit2)