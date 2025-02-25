import { Box, Card, CardContent, useTheme } from "@mui/material";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
import { PlotImportance } from "@optuna/react";
import { PlotType } from "../apiClient";
import { useParamImportance } from "../hooks/useParamImportance";
import { usePlot } from "../hooks/usePlot";
import { useBackendRender, usePlotlyColorTheme } from "../state";
const plotDomId = "graph-hyperparameter-importances";
export const GraphHyperparameterImportance = ({ studyId, study = null, graphHeight }) => {
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { importances } = useParamImportance({
        numCompletedTrials,
        studyId,
    });
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    if (useBackendRender()) {
        return (React.createElement(GraphHyperparameterImportanceBackend, { studyId: studyId, study: study, graphHeight: graphHeight }));
    }
    else {
        return (React.createElement(Card, null,
            React.createElement(CardContent, null,
                React.createElement(PlotImportance, { study: study, importance: importances, graphHeight: graphHeight, colorTheme: colorTheme }))));
    }
};
const GraphHyperparameterImportanceBackend = ({ studyId, study = null, graphHeight }) => {
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.ParamImportances,
    });
    useEffect(() => {
        if (data && layout) {
            plotly.react(plotDomId, data, layout);
        }
    }, [data, layout]);
    useEffect(() => {
        if (error) {
            console.error(error);
        }
    }, [error]);
    return React.createElement(Box, { component: "div", id: plotDomId, sx: { height: graphHeight } });
};
//# sourceMappingURL=GraphHyperparameterImportances.js.map