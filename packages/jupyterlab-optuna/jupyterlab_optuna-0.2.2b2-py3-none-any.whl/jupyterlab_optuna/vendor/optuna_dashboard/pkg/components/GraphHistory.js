import { useTheme } from "@mui/material";
import { PlotHistory } from "@optuna/react";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useConstants } from "../constantsProvider";
import { usePlotlyColorTheme } from "../state";
export const GraphHistory = ({ studies, logScale, includePruned, selectedTrials }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const linkURL = (studyId, trialNumber) => {
        return url_prefix + `/studies/${studyId}/trials?numbers=${trialNumber}`;
    };
    const navigate = useNavigate();
    return (React.createElement(PlotHistory, { studies: studies, logScale: logScale, includePruned: includePruned, colorTheme: colorTheme, linkURL: linkURL, router: navigate, selectedTrials: selectedTrials }));
};
//# sourceMappingURL=GraphHistory.js.map