# nolint start
AUX <- UHSTable[ID==ID_TARGET&TR %in% TR_TARGET & Vs30 %in% Vs30_TARGET & p==p_TARGET]    # keep the source intact
AUX[ , SaF := {                               # <-- overwrite SaF in place
  o <- order(Tn)                        # indices that sort the period
  p <- o[ which.max(SaF[o]) ]           # row‑number of the earliest peak
  SaF[o][ seq_len( match(p , o) ) ] <- SaF[p]   # blast plateau rows 1:p
  SaF                                   # hand the whole column back
},
by = .(Vs30, TR, ID, p) ]


AUX[,ID:="design"]         # per spectrum

DATA <- AUX[, .(
  ID = paste0("AEP=1/", TR, " Vs30= ", Vs30, " [", ID, "]"),
  Y = SaF,
  X = Tn,
  style = "Solid",
  type = "spline"
)
][order(X)] |> unique()


if (!exists("Sa_LOG")) {
  Sa_LOG <- FALSE
}
if (!exists("Tn_LOG")) {
  Tn_LOG <- FALSE
}
PLOT <- buildPlot(
  yAxis.label = TRUE,
  plot.height = 700,
  legend.layout = "horizontal",
  legend.show = TRUE,
  xAxis.log = Tn_LOG,
  yAxis.log = Sa_LOG,
  line.size = MID_LINE_SIZE,
  xAxis.legend = "Tn [s]",
  yAxis.legend = "Sa [g]",
  group.legend = "ID",
  plot.theme = HC.THEME,
  data.lines = DATA
)
