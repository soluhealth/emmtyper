# Helper functions

nameTable = function(df) {
  # Name table, based on BLAST results
  if (ncol(df) == 12) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit")}
  else if (ncol(df) == 13) {names(df) = c("Isolate", "EMM", "PercIdent", "AlLength", "Mismatch", "GapOpen", "Qstart", "Qend", "Hstart", "HEnd", "EVal", "Bit", "SuLength")}
  return(df)
}

cleanKeys_and_set = function(vector){
  # Given a vector of emm types, return only the type
  emms = sapply(vector, function(x) {strsplit(x, "[.]")[[1]][1]})

  emm_nums = sapply(emms, function(x) {substr(x, 4, 9)})
  names(emm_nums) = NULL

  return(unique(emm_nums))
}

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

# Name data frame, and filter the ones with alignment length lower that 80.
tab = nameTable(tab)

if(nrow(tab) != 0) {
  mean = mean(tab$Qstart)
  median = median(tab$Qstart)
  sd = sd(tab$Qstart)

  # print(c("Mean: ", mean)); print(c("SD: ", sd))

  # Calculate z-value of every query start.
  df = nrow(tab) - 1
  pVals = sapply(tab$Qstart, function(x) {dt((x - mean)/sd, df=df)})

  # First: show those outside a threshold of mean and multiplier * sd
  normal_range = as.vector(subset(tab, Qstart < (mean - multiplier*sd) | Qstart > (mean + multiplier*sd))$EMM)
  # Second: show the ones with signifinicance on (presumed) normal distribution
  significant_p = as.vector(tab[pVals < 0.025 | pVals > 0.975,]$EMM)
  # Third: show the ones outside +- 500 range from median
  empiric_median = as.vector(subset(tab, Qstart <= (median - 500) | Qstart >= (median + 500))$EMM)

  # Print output
  print(normal_range); print(significant_p); print(empiric_median)
  print(cleanKeys_and_set(c(normal_range, significant_p, empiric_median)))
} else {
  return
}
