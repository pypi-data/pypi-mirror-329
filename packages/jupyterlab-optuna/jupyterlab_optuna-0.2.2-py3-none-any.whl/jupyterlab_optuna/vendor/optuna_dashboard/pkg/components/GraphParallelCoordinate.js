import { GraphContainer, PlotParallelCoordinate, useGraphComponentState, } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
import { PlotType } from "../apiClient";
import { usePlot } from "../hooks/usePlot";
import { useBackendRender } from "../state";
const plotDomId = "graph-parallel-coordinate";
export const GraphParallelCoordinate = ({ study = null }) => {
    if (useBackendRender()) {
        return React.createElement(GraphParallelCoordinateBackend, { study: study });
    }
    else {
        return React.createElement(PlotParallelCoordinate, { study: study });
    }
};
const GraphParallelCoordinateBackend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.ParallelCoordinate,
    });
    useEffect(() => {
        if (data && layout && graphComponentState !== "componentWillMount") {
            try {
                plotly.react(plotDomId, data, layout).then(notifyGraphDidRender);
            }
            catch (err) {
                console.error(err);
            }
        }
    }, [data, layout, graphComponentState]);
    useEffect(() => {
        if (error) {
            console.error(error);
        }
    }, [error]);
    return (React.createElement(GraphContainer, { plotDomId: plotDomId, graphComponentState: graphComponentState }));
};
//# sourceMappingURL=GraphParallelCoordinate.js.map