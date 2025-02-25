import { Grid, useTheme } from "@mui/material";
import { PlotTimeline } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
import { PlotType } from "../apiClient";
import { studyDetailToStudy } from "../graphUtil";
import { usePlot } from "../hooks/usePlot";
import { usePlotlyColorTheme } from "../state";
import { useBackendRender } from "../state";
const plotDomId = "graph-timeline";
export const GraphTimeline = ({ study }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    if (useBackendRender()) {
        return React.createElement(GraphTimelineBackend, { study: study });
    }
    else {
        return (React.createElement(PlotTimeline, { study: studyDetailToStudy(study), colorTheme: colorTheme }));
    }
};
const GraphTimelineBackend = ({ study }) => {
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.Timeline,
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
    return (React.createElement(Grid, { item: true, xs: 9 },
        React.createElement("div", { id: plotDomId })));
};
//# sourceMappingURL=GraphTimeline.js.map