import { Card, CardContent, useTheme } from "@mui/material";
import { PlotIntermediateValues } from "@optuna/react";
import React from "react";
import { usePlotlyColorTheme } from "../state";
export const GraphIntermediateValues = ({ trials, includePruned, logScale }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    return (React.createElement(Card, null,
        React.createElement(CardContent, null,
            React.createElement(PlotIntermediateValues, { trials: trials, includePruned: includePruned, logScale: logScale, colorTheme: colorTheme }))));
};
//# sourceMappingURL=GraphIntermediateValues.js.map