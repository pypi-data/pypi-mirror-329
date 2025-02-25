import { useTheme } from "@mui/material";
import { GraphContainer, PlotEdf, useGraphComponentState } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
import { CompareStudiesPlotType } from "../apiClient";
import { useAPIClient } from "../apiClientProvider";
import { useBackendRender, usePlotlyColorTheme } from "../state";
export const GraphEdf = ({ studies, objectiveId }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    if (useBackendRender()) {
        return React.createElement(GraphEdfBackend, { studies: studies });
    }
    else {
        return (React.createElement(PlotEdf, { studies: studies, objectiveId: objectiveId, colorTheme: colorTheme }));
    }
};
const domId = "graph-edf";
const GraphEdfBackend = ({ studies }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const { apiClient } = useAPIClient();
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const studyIds = studies.map((s) => s.id);
    const numCompletedTrials = studies.reduce((acc, study) => acc + (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length), 0);
    useEffect(() => {
        if (studyIds.length === 0) {
            return;
        }
        if (graphComponentState !== "componentWillMount") {
            apiClient
                .getCompareStudiesPlot(studyIds, CompareStudiesPlotType.EDF)
                .then(({ data, layout }) => {
                plotly
                    .react(domId, data, Object.assign(Object.assign({}, layout), { template: colorTheme }))
                    .then(notifyGraphDidRender);
            })
                .catch((err) => {
                console.error(err);
            });
        }
    }, [studyIds, numCompletedTrials, graphComponentState]);
    return (React.createElement(GraphContainer, { plotDomId: domId, graphComponentState: graphComponentState }));
};
//# sourceMappingURL=GraphEdf.js.map