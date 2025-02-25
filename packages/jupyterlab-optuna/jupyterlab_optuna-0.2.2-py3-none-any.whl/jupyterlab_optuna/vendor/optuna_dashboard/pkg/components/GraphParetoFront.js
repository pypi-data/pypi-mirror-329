import { Box, FormControl, FormLabel, Grid, MenuItem, Select, Typography, useTheme, } from "@mui/material";
import { getFeasibleTrials, getIsDominated } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PlotType } from "../apiClient";
import { useConstants } from "../constantsProvider";
import { makeHovertext } from "../graphUtil";
import { usePlot } from "../hooks/usePlot";
import { usePlotlyColorTheme } from "../state";
import { useBackendRender } from "../state";
const plotDomId = "graph-pareto-front";
export const GraphParetoFront = ({ study = null, selectedTrials = null }) => {
    if (useBackendRender() && !selectedTrials) {
        return React.createElement(GraphParetoFrontBackend, { study: study });
    }
    else {
        return (React.createElement(GraphParetoFrontFrontend, { study: study, selectedTrials: selectedTrials }));
    }
};
const GraphParetoFrontBackend = ({ study = null }) => {
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.ParetoFront,
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
    return React.createElement(Box, { component: "div", id: plotDomId, sx: { height: "450px" } });
};
const GraphParetoFrontFrontend = ({ study = null, selectedTrials = null }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const navigate = useNavigate();
    const [objectiveXId, setObjectiveXId] = useState(0);
    const [objectiveYId, setObjectiveYId] = useState(1);
    const metricNames = (study === null || study === void 0 ? void 0 : study.metric_names) || [];
    const handleObjectiveXChange = (event) => {
        setObjectiveXId(event.target.value);
    };
    const handleObjectiveYChange = (event) => {
        setObjectiveYId(event.target.value);
    };
    useEffect(() => {
        if (study != null) {
            plotParetoFront(study, objectiveXId, objectiveYId, theme.palette.mode, colorTheme, selectedTrials);
            const element = document.getElementById(plotDomId);
            if (element != null) {
                // @ts-ignore
                element.on("plotly_click", (data) => {
                    const plotTextInfo = JSON.parse(data.points[0].text.replace(/<br>/g, ""));
                    navigate(url_prefix +
                        `/studies/${study.id}/trials?numbers=${plotTextInfo.number}`);
                });
                return () => {
                    // @ts-ignore
                    element.removeAllListeners("plotly_click");
                };
            }
        }
    }, [
        study,
        selectedTrials,
        objectiveXId,
        objectiveYId,
        theme.palette.mode,
        colorTheme,
    ]);
    return (React.createElement(Grid, { container: true, direction: "row" },
        React.createElement(Grid, { item: true, xs: 3, container: true, direction: "column", sx: { paddingRight: theme.spacing(2) } },
            React.createElement(Typography, { variant: "h6", sx: { margin: "1em 0", fontWeight: theme.typography.fontWeightBold } }, "Pareto Front"),
            study !== null && study.directions.length !== 1 ? (React.createElement(React.Fragment, null,
                React.createElement(FormControl, { component: "fieldset" },
                    React.createElement(FormLabel, { component: "legend" }, "Objective X:"),
                    React.createElement(Select, { value: objectiveXId, onChange: handleObjectiveXChange }, study.directions.map((d, i) => (React.createElement(MenuItem, { value: i, key: i }, metricNames.length === (study === null || study === void 0 ? void 0 : study.directions.length)
                        ? metricNames[i]
                        : `${i}`))))),
                React.createElement(FormControl, { component: "fieldset" },
                    React.createElement(FormLabel, { component: "legend" }, "Objective Y:"),
                    React.createElement(Select, { value: objectiveYId, onChange: handleObjectiveYChange }, study.directions.map((d, i) => (React.createElement(MenuItem, { value: i, key: i }, metricNames.length === (study === null || study === void 0 ? void 0 : study.directions.length)
                        ? metricNames[i]
                        : `${i}`))))))) : null),
        React.createElement(Grid, { item: true, xs: 9 },
            React.createElement(Box, { component: "div", id: plotDomId, sx: {
                    height: "450px",
                } }))));
};
const filterFunc = (trial, selectedTrials, directions) => {
    return (selectedTrials.includes(trial.number) &&
        trial.state === "Complete" &&
        trial.values !== undefined &&
        trial.values.length === directions.length);
};
const makeScatterObject = (trials, objectiveXId, objectiveYId, hovertemplate, dominated, feasible, mode) => {
    const marker = makeMarker(trials, dominated, feasible, mode);
    return {
        x: trials.map((t) => t.values ? t.values[objectiveXId] : null),
        y: trials.map((t) => t.values ? t.values[objectiveYId] : null),
        text: trials.map((t) => makeHovertext(t)),
        mode: "markers",
        hovertemplate: hovertemplate,
        marker: marker,
        showlegend: false,
    };
};
const makeMarker = (trials, dominated, feasible, mode) => {
    if (feasible && dominated) {
        return {
            line: { width: 0.5, color: "Grey" },
            // @ts-ignore
            color: trials.map((t) => t.number),
            colorscale: "Blues",
            reversescale: true,
            colorbar: {
                title: "Trial",
            },
        };
    }
    else if (feasible && !dominated) {
        return {
            line: { width: 0.5, color: "Grey" },
            // @ts-ignore
            color: trials.map((t) => t.number),
            colorscale: "Reds",
            colorbar: {
                title: "Best Trial",
                x: 1.1,
                xpad: 80,
            },
        };
    }
    else {
        return {
            // @ts-ignore
            color: mode === "dark" ? "#666666" : "#cccccc",
        };
    }
};
const plotParetoFront = (study, objectiveXId, objectiveYId, mode, colorTheme, selectedTrials) => {
    if (document.getElementById(plotDomId) === null) {
        return;
    }
    const xmin = Math.min(...study.trials.map((t) => { var _a; return (_a = t.values) === null || _a === void 0 ? void 0 : _a[objectiveXId]; }));
    const xmax = Math.max(...study.trials.map((t) => { var _a; return (_a = t.values) === null || _a === void 0 ? void 0 : _a[objectiveXId]; }));
    const ymin = Math.min(...study.trials.map((t) => { var _a; return (_a = t.values) === null || _a === void 0 ? void 0 : _a[objectiveYId]; }));
    const ymax = Math.max(...study.trials.map((t) => { var _a; return (_a = t.values) === null || _a === void 0 ? void 0 : _a[objectiveYId]; }));
    const layout = {
        margin: {
            l: 50,
            t: 0,
            r: 50,
            b: 0,
        },
        template: colorTheme,
        uirevision: "true",
        xaxis: {
            range: selectedTrials
                ? [xmin - (xmax - xmin) * 0.1, xmax + (xmax - xmin) * 0.1]
                : undefined,
        },
        yaxis: {
            range: selectedTrials
                ? [ymin - (ymax - ymin) * 0.1, ymax + (ymax - ymin) * 0.1]
                : undefined,
        },
    };
    const trials = study ? study.trials : [];
    if (selectedTrials === null || selectedTrials.length === 0) {
        selectedTrials = trials.map((t) => t.number);
    }
    const filteredTrials = trials.filter((t) => filterFunc(t, selectedTrials, study.directions));
    if (filteredTrials.length === 0) {
        plotly.react(plotDomId, [], layout);
        return;
    }
    const { feasibleTrials, infeasibleTrials } = getFeasibleTrials(filteredTrials, study);
    const normalizedValues = [];
    feasibleTrials.forEach((t) => {
        if (t.values && t.values.length === study.directions.length) {
            const trialValues = t.values.map((v, i) => {
                return study.directions[i] === "minimize"
                    ? v
                    : -v;
            });
            normalizedValues.push(trialValues);
        }
    });
    const isDominated = getIsDominated(normalizedValues);
    const plotData = [
        makeScatterObject(feasibleTrials.filter((t, i) => isDominated[i]), objectiveXId, objectiveYId, infeasibleTrials.length === 0
            ? "%{text}<extra>Trial</extra>"
            : "%{text}<extra>Feasible Trial</extra>", true, true, mode),
        makeScatterObject(feasibleTrials.filter((t, i) => !isDominated[i]), objectiveXId, objectiveYId, "%{text}<extra>Best Trial</extra>", false, true, mode),
        makeScatterObject(infeasibleTrials, objectiveXId, objectiveYId, "%{text}<extra>Infeasible Trial</extra>", false, false, mode),
    ];
    plotly.react(plotDomId, plotData, layout);
};
//# sourceMappingURL=GraphParetoFront.js.map