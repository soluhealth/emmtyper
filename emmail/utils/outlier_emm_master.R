args = commandArgs(trailingOnly = T)

if (length(args) == 2) {
  multiplier = as.integer(args[2])
} else {
  multiplier = 1
}

table = read.table(args[1], sep="\t")

nameTable = function(df) {
  # Name table, based on BLAST results
  if (ncol(df) == 12) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit")}
  else if (ncol(df) == 13) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit", "SuLength")}
  return(df)
}

table = nameTable(table)
table = table[table$AlLength > 80,]

mean = mean(table$Qstart)
median = median(table$Qstart)
sd = sd(table$Qstart)

print(c("Mean: ", mean)); print(c("SD: ", sd))

zVals = sapply(table$Qstart, function(x) {dnorm((x - mean)/sd)})

as.vector(subset(table, Qstart <= (mean - multiplier*sd) | Qstart >= (mean + multiplier*sd))$EMM)
as.vector(table[zVals*2 < 0.05,]$EMM)
as.vector(subset(table, Qstart <= (median - 500) | Qstart >= (median + 500))$EMM)
