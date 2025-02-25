import { useTheme } from "@mui/material";
import { GraphContainer, PlotSlice, useGraphComponentState, } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
import { PlotType } from "../apiClient";
import { usePlot } from "../hooks/usePlot";
import { useBackendRender, usePlotlyColorTheme } from "../state";
export const GraphSlice = ({ study = null }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    if (useBackendRender()) {
        return React.createElement(GraphSliceBackend, { study: study });
    }
    else {
        return React.createElement(PlotSlice, { study: study, colorTheme: colorTheme });
    }
};
const domId = "graph-slice";
const GraphSliceBackend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.Slice,
    });
    useEffect(() => {
        if (data && layout && graphComponentState !== "componentWillMount") {
            plotly.react(domId, data, layout).then(notifyGraphDidRender);
        }
    }, [data, layout, graphComponentState]);
    useEffect(() => {
        if (error) {
            console.error(error);
        }
    }, [error]);
    return (React.createElement(GraphContainer, { plotDomId: domId, graphComponentState: graphComponentState }));
};
//# sourceMappingURL=GraphSlice.js.map