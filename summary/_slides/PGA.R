# DT <- UHSTable[Tn == Tn_PGA & p == p_TARGET & ID == ID_TARGET & Vs30 %in% Vs30_TARGET & TR %in% TR_TARGET, .(TR, Vs30, PGA = SaF, Tn, p)]
ITo <- AEPTable$ITo |> unique()

DT <- UHSTable[p == p_TARGET & ID %in% ID_TARGET & Vs30 %in% Vs30_TARGET & TR %in% TR_TARGET][Tn == min(Tn), .(TR, Vs30, PGA = SaF, Tn, p, ID)]

DT[, `:=`(POE = round(100 * (1 - exp(-ITo / TR)), 1))]
DT <- DT[order(as.numeric(Vs30))]


if (PSA_Units %in% c("cm", "cm/s2", "cm/s**2", "cm/s^2")) {
    DT[, PGA := round(PGA * 988, 1)]
}

if (PSA_Units %in% c("g")) {
    DT[, PGA := round(PGA, 3)]
}
AUX <- dcast(
    DT[, .(TR, Vs30, PGA, POE, ID)],
    TR + POE + ID ~ Vs30,
    value.var = "PGA",
    fun.aggregate = mean
)

setcolorder(AUX, c("TR", "POE", sort(as.numeric(unique(DT$Vs30)))))
setnames(AUX, old = "POE", new = "poe[%]")
setnames(AUX, old = c("TR"), new = c("TR[yr]"))

TBL <- AUX |> buildTable(
    library = "flextable",
    align.body = "center",
    font.size.body = FONT.SIZE.BODY,
    font.size.header = FONT.SIZE.HEADER
)
TBL <- flextable::set_table_properties(TBL, layout = "autofit")
