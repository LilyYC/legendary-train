Asetwd(“~/A2”)
nfl.raw <- read.csv("NFLdraft.csv", head= T, strip.white= T, stringsAsFactors = F)
nfl.raw$Pos[nfl.raw$Pos == "LS"] <- "C"
nfl <- within(nfl.raw, { 
Pos <- factor(Pos)
PosGroup <- factor(ifelse(Pos %in% c("C", "DE", "DT", "OG", "OT", "TE"),"Linemen",
                            ifelse(Pos %in% c("CB", "WR", "FS"),"Small Backs", "Big Backs")))
HtFt <- as.numeric(sub("-.*", "", Ht))
HtIn <- as.numeric(sub("*.-", "", Ht))
Ht <- 12*HtFt + HtIn
  ProTeam <- factor(matrix(unlist(strsplit(Drafted, " / ")), ncol= 4, byrow = T)[,1])
  Round <- factor(matrix(unlist(strsplit(Drafted, " / ")), ncol= 4, byrow = T)[,2])
  Overall <- factor(matrix(unlist(strsplit(Drafted, " / ")), ncol= 4, byrow = T)[,3])
  Year <- factor(matrix(unlist(strsplit(Drafted, " / ")), ncol= 4, byrow = T)[,4])
  Overall <- as.numeric(gsub("[^0-9]", "", Overall))
  
  #1
  with(nfl , plot(I(6 - Yd40), Vertical, xlab = "40Yard game", ylab = "Vertical jump"))
  #2
  fit=lm(Vertical ~ I(6 - Yd40), data = nfl)
  #3
  abline(fit,col=2)
  #4
  par(mfrow=c(1, 2))
  with(fit, plot(fitted.values,residuals)) # Residual plot
  with(fit, qqnorm(residuals))
  #5 Exponential Transformation
  par(mfrow=c(1, 1))
  fit2 = lm ( Vertical ~ I(exp(6 - Yd40)) , data = nfl)
  with (nfl.raw, plot(exp(6 - Yd40), Vertical))
  par(mfrow=c(1, 2))
  with(fit2, plot(fitted.values,residuals)) # Residual plot
  with(fit2, qqnorm(residuals))
  
  #6 Squared Transformation
  par(mfrow=c(1, 1))
  with (nfl.raw, plot((6 - Yd40)^2, Vertical, main = "scatter plot between Vertical vs. squared transformation on X"))
  fit3=lm (Vertical ~ I((6 - Yd40)^2), data = nfl)
  abline(fit3, col=2)
  par(mfrow=c(1, 2))
  with(fit3, plot(residuals, fitted.values, main="Residual plot for fit3"))
  with(fit3, qqnorm(residuals))
  #7
  rSquared1 = summary(fit)$r.squared
  SSE1 = anova(fit)$'Sum Sq'[2]
  tstat1 = summary(fit)$coefficients[6]
  slope1 = summary(fit)$coefficients[2]
  
  rSquared2 = summary(fit2)$r.squared
  SSE2 = anova(fit2)$'Sum Sq'[2]
  tstat2 = summary(fit2)$coefficients[6]
  slope2 = summary(fit2)$coefficients[2]
  
  rSquared3 = summary(fit3)$r.squared
  SSE3 = anova(fit3)$'Sum Sq'[2]
  tstat3 = summary(fit3)$coefficients[6]
  slope3 = summary(fit3)$coefficients[2]
  
  data.frame(Table=c("linear", "expon", "square"),
             rSquare = c(rSquared1,rSquared2,rSquared3), SSE=c(SSE1,SSE2,SSE3),
             tstat = c(tstat1, tstat2, tstat3), Slpoe = c(slope1, slope2, slope3))
  
  
  influence.measures(fit3)
  infl <- as.data.frame(influence.measures(fit3)$infmat)
  infl$dffit
  infl$hat
  nfl.raw
  ok <- influence.measures(fit3)
  
  ####Q8 Players' name####
  nfl.raw$Name[as.numeric(rownames(infl)[which(infl$hat > 2.5*mean(infl$hat))])]
  nfl.raw$Name[as.numeric(rownames(infl)[(abs(infl$dffit) > 0.3 )])]
  ####Indexing those players####
  idx1= ()
  idx1
  idx2=((infl)[(abs(infl$dffit) > 0.3 )])
  idx2
  
  with (nfl.raw, plot(exp(6 - Yd40), Vertical, col=idx,
  )
  idx=idx2*3+1
  idx2
  idx[idx1]=2
  
  ##############PART B NFL SEASON############
  R = read.csv("Receiving.csv", head=T, strip.white=T, stringsAsFactors=F)
  R
  R <- cbind(R$Player, R$TD)
  R
  