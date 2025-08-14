# nolint start

DATA <- ASCETable[ID=="mcer"&TR %in% TR_TARGET & Vs30 %in% Vs30_TARGET , .(
  ID = paste0("AEP=1/", TR, " Vs30= ", Vs30, " [", ID, "]"),
  Y = SaF,
  X = Tn,
  style = "Solid",
  type = "line"
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
  line.type = "line",
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
