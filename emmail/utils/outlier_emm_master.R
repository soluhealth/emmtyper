
# Command line arguments
args = commandArgs(trailingOnly = T)

# For now, only catering for file input and range multiplier
file_input = args[1]

if (length(args) > 1) {
  multiplier = as.double(args[2])
} else {
  multiplier = 1
}

tab = read.table(file_input, sep="\t")

nameTable = function(df) {
  # Name table, based on BLAST results
  if (ncol(df) == 12) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit")}
  else if (ncol(df) == 13) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit", "SuLength")}
  return(df)
}

# Name data frame, and filter the ones with alignment length lower that 80.
tab = nameTable(tab)
tab = tab[tab$AlLength > 80,]

mean = mean(table$Qstart)
median = median(table$Qstart)
sd = sd(table$Qstart)

print(c("Mean: ", mean)); print(c("SD: ", sd))

# Calculate z-value of every query start.
pVals = sapply(table$Qstart, function(x) {dnorm((x - mean)/sd)})

# First: show those outside a threshold of mean and multiplier * sd
as.vector(subset(table, Qstart <= (mean - multiplier*sd) | Qstart >= (mean + multiplier*sd))$EMM)
# Second: show the ones with signifinicance on (presumed) normal distribution
as.vector(table[pVals < 0.025 | pVals > 0.975,]$EMM)
# Third: show the ones outside +- 500 range from median
as.vector(subset(table, Qstart <= (median - 500) | Qstart >= (median + 500))$EMM)
