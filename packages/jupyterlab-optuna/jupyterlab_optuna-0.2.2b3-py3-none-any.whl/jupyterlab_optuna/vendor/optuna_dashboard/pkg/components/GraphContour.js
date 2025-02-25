import { Box, FormControl, FormLabel, Grid, Link, MenuItem, Select, Stack, Typography, useTheme, } from "@mui/material";
import blue from "@mui/material/colors/blue";
import { GraphContainer, useGraphComponentState, useMergedUnionSearchSpace, } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect, useMemo, useState } from "react";
import { PlotType } from "../apiClient";
import { getAxisInfo } from "../graphUtil";
import { usePlot } from "../hooks/usePlot";
import { usePlotlyColorTheme } from "../state";
import { useBackendRender } from "../state";
const plotDomId = "graph-contour";
const CONTOUR_DISABLED_THRESHOLD = 100;
export const Contour = ({ study = null }) => {
    const isBackendRender = useBackendRender();
    const [loadAnyway, setLoadAnyway] = useState(false);
    const shouldContourDisabled = useMemo(() => { var _a; return ((_a = study === null || study === void 0 ? void 0 : study.trials.length) !== null && _a !== void 0 ? _a : 0) > CONTOUR_DISABLED_THRESHOLD; }, [study]);
    if (shouldContourDisabled && !loadAnyway) {
        return React.createElement(DisabledContour, { onLoadAnywayClicked: () => setLoadAnyway(true) });
    }
    if (isBackendRender) {
        return React.createElement(ContourBackend, { study: study });
    }
    return React.createElement(ContourFrontend, { study: study });
};
const DisabledContour = ({ onLoadAnywayClicked }) => {
    const theme = useTheme();
    return (React.createElement(Box, { component: "div", id: plotDomId },
        React.createElement(Typography, { variant: "h6", sx: { margin: "1em 0", fontWeight: theme.typography.fontWeightBold } }, "Contour"),
        React.createElement(Stack, { direction: "column", spacing: 1, alignItems: "center", sx: {
                margin: "1em 0",
            } },
            React.createElement(Typography, { variant: "body1", color: theme.palette.grey[700] }, "High number of trials makes processing this plot slow; disabled by default."),
            React.createElement(Link, { component: "button", sx: { fontWeight: theme.typography.fontWeightBold }, onClick: onLoadAnywayClicked }, "Load plot anyway"))));
};
const ContourBackend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.Contour,
    });
    useEffect(() => {
        if (data && layout && graphComponentState !== "componentWillMount") {
            plotly.react(plotDomId, data, layout).then(notifyGraphDidRender);
        }
    }, [data, layout, graphComponentState]);
    useEffect(() => {
        if (error) {
            console.error(error);
        }
    }, [error]);
    return (React.createElement(GraphContainer, { plotDomId: plotDomId, graphComponentState: graphComponentState }));
};
const ContourFrontend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const [objectiveId, setObjectiveId] = useState(0);
    const searchSpace = useMergedUnionSearchSpace(study === null || study === void 0 ? void 0 : study.union_search_space);
    const [xParam, setXParam] = useState(null);
    const [yParam, setYParam] = useState(null);
    const metricNames = (study === null || study === void 0 ? void 0 : study.metric_names) || [];
    if (xParam === null && searchSpace.length > 0) {
        setXParam(searchSpace[0]);
    }
    if (yParam === null && searchSpace.length > 1) {
        setYParam(searchSpace[1]);
    }
    const handleObjectiveChange = (event) => {
        setObjectiveId(event.target.value);
    };
    const handleXParamChange = (event) => {
        const param = searchSpace.find((s) => s.name === event.target.value);
        setXParam(param || null);
    };
    const handleYParamChange = (event) => {
        const param = searchSpace.find((s) => s.name === event.target.value);
        setYParam(param || null);
    };
    useEffect(() => {
        var _a;
        if (study != null && graphComponentState !== "componentWillMount") {
            (_a = plotContour(study, objectiveId, xParam, yParam, colorTheme)) === null || _a === void 0 ? void 0 : _a.then(notifyGraphDidRender);
        }
    }, [study, objectiveId, xParam, yParam, colorTheme, graphComponentState]);
    const space = study ? study.union_search_space : [];
    return (React.createElement(Grid, { container: true, direction: "row" },
        React.createElement(Grid, { item: true, xs: 3, container: true, direction: "column", sx: { paddingRight: theme.spacing(2) } },
            React.createElement(Typography, { variant: "h6", sx: { margin: "1em 0", fontWeight: theme.typography.fontWeightBold } }, "Contour"),
            study !== null && study.directions.length !== 1 ? (React.createElement(FormControl, { component: "fieldset" },
                React.createElement(FormLabel, { component: "legend" }, "Objective:"),
                React.createElement(Select, { value: objectiveId, onChange: handleObjectiveChange }, study.directions.map((d, i) => (React.createElement(MenuItem, { value: i, key: i }, metricNames.length === (study === null || study === void 0 ? void 0 : study.directions.length)
                    ? metricNames[i]
                    : `${i}`)))))) : null,
            study !== null && space.length > 0 ? (React.createElement(Grid, { container: true, direction: "column", gap: 1 },
                React.createElement(FormControl, { component: "fieldset", fullWidth: true },
                    React.createElement(FormLabel, { component: "legend" }, "x:"),
                    React.createElement(Select, { value: (xParam === null || xParam === void 0 ? void 0 : xParam.name) || "", onChange: handleXParamChange }, space.map((d) => (React.createElement(MenuItem, { value: d.name, key: d.name }, d.name))))),
                React.createElement(FormControl, { component: "fieldset", fullWidth: true },
                    React.createElement(FormLabel, { component: "legend" }, "y:"),
                    React.createElement(Select, { value: (yParam === null || yParam === void 0 ? void 0 : yParam.name) || "", onChange: handleYParamChange }, space.map((d) => (React.createElement(MenuItem, { value: d.name, key: d.name }, d.name))))))) : null),
        React.createElement(Grid, { item: true, xs: 9 },
            React.createElement(GraphContainer, { plotDomId: plotDomId, graphComponentState: graphComponentState }))));
};
const filterFunc = (trial) => {
    return trial.state === "Complete" && trial.values !== undefined;
};
const plotContour = (study, objectiveId, xParam, yParam, colorTheme) => {
    if (document.getElementById(plotDomId) === null) {
        return;
    }
    const trials = study ? study.trials : [];
    const filteredTrials = trials.filter((t) => filterFunc(t));
    if (filteredTrials.length < 2 || xParam === null || yParam === null) {
        return plotly.react(plotDomId, [], {
            template: colorTheme,
        });
    }
    const xAxis = getAxisInfo(trials, xParam);
    const yAxis = getAxisInfo(trials, yParam);
    const xIndices = xAxis.indices;
    const yIndices = yAxis.indices;
    const layout = {
        xaxis: {
            title: xParam.name,
            type: xAxis.isCat ? "category" : xAxis.isLog ? "log" : "linear",
        },
        yaxis: {
            title: yParam.name,
            type: yAxis.isCat ? "category" : yAxis.isLog ? "log" : "linear",
        },
        margin: {
            l: 50,
            t: 0,
            r: 50,
            b: 50,
        },
        uirevision: "true",
        template: colorTheme,
    };
    // TODO(c-bata): Support parameters that only have the single value
    if (xIndices.length <= 1 || yIndices.length <= 1) {
        return plotly.react(plotDomId, [], layout);
    }
    const xValues = [];
    const yValues = [];
    const zValues = new Array(yIndices.length);
    const feasibleXY = new Set();
    for (let j = 0; j < yIndices.length; j++) {
        zValues[j] = new Array(xIndices.length).fill(null);
    }
    filteredTrials.forEach((trial, i) => {
        if (xAxis.values[i] && yAxis.values[i] && trial.values) {
            if (trial.constraints.every((c) => c <= 0)) {
                feasibleXY.add(xValues.length);
            }
            const xValue = xAxis.values[i];
            const yValue = yAxis.values[i];
            xValues.push(xValue);
            yValues.push(yValue);
            const xi = xIndices.indexOf(xValue);
            const yi = yIndices.indexOf(yValue);
            const zValue = trial.values[objectiveId];
            zValues[yi][xi] = zValue;
        }
    });
    if (!study.is_preferential) {
        const plotData = [
            {
                type: "contour",
                x: xIndices,
                y: yIndices,
                z: zValues,
                colorscale: "Blues",
                connectgaps: true,
                hoverinfo: "none",
                line: {
                    smoothing: 1.3,
                },
                reversescale: study.directions[objectiveId] !== "minimize",
                // https://github.com/plotly/react-plotly.js/issues/251
                // @ts-ignore
                contours: {
                    coloring: "heatmap",
                },
            },
            {
                type: "scatter",
                x: xValues.filter((_, i) => feasibleXY.has(i)),
                y: yValues.filter((_, i) => feasibleXY.has(i)),
                marker: { line: { width: 2.0, color: "Grey" }, color: "black" },
                mode: "markers",
                showlegend: false,
            },
            {
                type: "scatter",
                x: xValues.filter((_, i) => !feasibleXY.has(i)),
                y: yValues.filter((_, i) => !feasibleXY.has(i)),
                marker: { line: { width: 2.0, color: "Grey" }, color: "#cccccc" },
                mode: "markers",
                showlegend: false,
            },
        ];
        return plotly.react(plotDomId, plotData, layout);
    }
    layout.legend = {
        y: 0.8,
    };
    const bestTrialIndices = study.best_trials.map((trial) => trial.number);
    const plotData = [
        {
            type: "scatter",
            x: xValues.filter((_, i) => bestTrialIndices.includes(i)),
            y: yValues.filter((_, i) => bestTrialIndices.includes(i)),
            marker: {
                line: { width: 2.0, color: "Grey" },
                color: blue[200],
            },
            name: "best trials",
            mode: "markers",
        },
        {
            type: "scatter",
            x: xValues.filter((_, i) => !bestTrialIndices.includes(i)),
            y: yValues.filter((_, i) => !bestTrialIndices.includes(i)),
            marker: { line: { width: 2.0, color: "Grey" }, color: "black" },
            name: "others",
            mode: "markers",
        },
    ];
    return plotly.react(plotDomId, plotData, layout);
};
//# sourceMappingURL=GraphContour.js.map