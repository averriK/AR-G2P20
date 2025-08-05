# Model comparison

DATA <- UHSTable[ID %in% ID_TARGET & Vs30 %in% Vs30_TARGET & TR %in% TR_TARGET & p %in% p_TARGET, .(
    ID = paste0("AEP=1/", TR, " Vs30= ", Vs30, " [", ID, "] (", p, ")"),
    Y = SaF,
    X = Tn,
    style = "Solid"
)][order(X)] |> unique()

if (!exists("Sa_LOG")) {
    Sa_LOG <- FALSE
}
if (!exists("Tn_LOG")) {
    Tn_LOG <- FALSE
}
PLOT <- buildPlot(
    yAxis.label = TRUE,
    line.type = "spline",
    plot.height = 500,
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
