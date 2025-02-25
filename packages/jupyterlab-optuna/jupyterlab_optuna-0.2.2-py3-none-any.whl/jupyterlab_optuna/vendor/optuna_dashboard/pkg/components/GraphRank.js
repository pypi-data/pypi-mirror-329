import { FormControl, FormLabel, Grid, MenuItem, Select, Typography, useTheme, } from "@mui/material";
import { GraphContainer, useGraphComponentState, useMergedUnionSearchSpace, } from "@optuna/react";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect, useState } from "react";
import { PlotType } from "../apiClient";
import { getAxisInfo, makeHovertext } from "../graphUtil";
import { usePlot } from "../hooks/usePlot";
import { useBackendRender, usePlotlyColorTheme } from "../state";
const plotDomId = "graph-rank";
export const GraphRank = ({ study = null }) => {
    if (useBackendRender()) {
        return React.createElement(GraphRankBackend, { study: study });
    }
    else {
        return React.createElement(GraphRankFrontend, { study: study });
    }
};
const GraphRankBackend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const studyId = study === null || study === void 0 ? void 0 : study.id;
    const numCompletedTrials = (study === null || study === void 0 ? void 0 : study.trials.filter((t) => t.state === "Complete").length) || 0;
    const { data, layout, error } = usePlot({
        numCompletedTrials,
        studyId,
        plotType: PlotType.Rank,
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
const GraphRankFrontend = ({ study = null }) => {
    const { graphComponentState, notifyGraphDidRender } = useGraphComponentState();
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const [objectiveId, setobjectiveId] = useState(0);
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
        setobjectiveId(Number(event.target.value));
    };
    const handleXParamChange = (event) => {
        const param = searchSpace.find((item) => item.name === event.target.value);
        setXParam(param || null);
    };
    const handleYParamChange = (event) => {
        const param = searchSpace.find((item) => item.name === event.target.value);
        setYParam(param || null);
    };
    useEffect(() => {
        var _a;
        if (study != null && graphComponentState !== "componentWillMount") {
            const rankPlotInfo = getRankPlotInfo(study, objectiveId, xParam, yParam);
            (_a = plotRank(rankPlotInfo, colorTheme)) === null || _a === void 0 ? void 0 : _a.then(notifyGraphDidRender);
        }
    }, [
        study,
        objectiveId,
        xParam,
        yParam,
        theme.palette.mode,
        colorTheme,
        graphComponentState,
    ]);
    const space = study ? study.union_search_space : [];
    return (React.createElement(Grid, { container: true, direction: "row" },
        React.createElement(Grid, { item: true, xs: 3, container: true, direction: "column", sx: { paddingRight: theme.spacing(2) } },
            React.createElement(Typography, { variant: "h6", sx: { margin: "1em 0", fontWeight: theme.typography.fontWeightBold } }, "Rank"),
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
const getRankPlotInfo = (study, objectiveId, xParam, yParam) => {
    if (study === null) {
        return null;
    }
    const trials = study.trials;
    const filteredTrials = trials.filter(filterFunc);
    if (filteredTrials.length < 2 || xParam === null || yParam === null) {
        return null;
    }
    const xAxis = getAxisInfo(filteredTrials, xParam);
    const yAxis = getAxisInfo(filteredTrials, yParam);
    let xValues = [];
    let yValues = [];
    const zValues = [];
    const isFeasible = [];
    const hovertext = [];
    filteredTrials.forEach((trial, i) => {
        const xValue = xAxis.values[i];
        const yValue = yAxis.values[i];
        if (xValue && yValue && trial.values) {
            xValues.push(xValue);
            yValues.push(yValue);
            const zValue = trial.values[objectiveId];
            zValues.push(zValue);
            const feasibility = trial.constraints.every((c) => c <= 0);
            isFeasible.push(feasibility);
            hovertext.push(makeHovertext(trial));
        }
    });
    const colors = getColors(zValues);
    if (xAxis.isCat && !yAxis.isCat) {
        const indices = Array.from(Array(xValues.length).keys()).sort((a, b) => xValues[a]
            .toString()
            .toLowerCase()
            .localeCompare(xValues[b].toString().toLowerCase()));
        xValues = indices.map((i) => xValues[i]);
        yValues = indices.map((i) => yValues[i]);
    }
    else if (!xAxis.isCat && yAxis.isCat) {
        const indices = Array.from(Array(yValues.length).keys()).sort((a, b) => yValues[a]
            .toString()
            .toLowerCase()
            .localeCompare(yValues[b].toString().toLowerCase()));
        xValues = indices.map((i) => xValues[i]);
        yValues = indices.map((i) => yValues[i]);
    }
    else if (xAxis.isCat && yAxis.isCat) {
        const indices = Array.from(Array(xValues.length).keys()).sort((a, b) => {
            const xComp = xValues[a]
                .toString()
                .toLowerCase()
                .localeCompare(xValues[b].toString().toLowerCase());
            if (xComp !== 0) {
                return xComp;
            }
            return yValues[a]
                .toString()
                .toLowerCase()
                .localeCompare(yValues[b].toString().toLowerCase());
        });
        xValues = indices.map((i) => xValues[i]);
        yValues = indices.map((i) => yValues[i]);
    }
    return {
        xtitle: xAxis.name,
        ytitle: yAxis.name,
        xtype: xAxis.isCat ? "category" : xAxis.isLog ? "log" : "linear",
        ytype: yAxis.isCat ? "category" : yAxis.isLog ? "log" : "linear",
        xvalues: xValues,
        yvalues: yValues,
        colors,
        is_feasible: isFeasible,
        hovertext,
    };
};
const filterFunc = (trial) => {
    return trial.state === "Complete" && trial.values !== undefined;
};
const getColors = (values) => {
    const rawRanks = getOrderWithSameOrderAveraging(values);
    let colorIdxs = [];
    if (values.length > 2) {
        colorIdxs = rawRanks.map((rank) => rank / (values.length - 1));
    }
    else {
        colorIdxs = [0.5];
    }
    return colorIdxs;
};
const getOrderWithSameOrderAveraging = (values) => {
    const sortedValues = values.slice().sort((a, b) => a - b);
    const ranks = [];
    values.forEach((value) => {
        const firstIndex = sortedValues.indexOf(value);
        const lastIndex = sortedValues.lastIndexOf(value);
        const sumOfTheValue = ((firstIndex + lastIndex) * (lastIndex - firstIndex + 1)) / 2;
        const rank = sumOfTheValue / (lastIndex - firstIndex + 1);
        ranks.push(rank);
    });
    return ranks;
};
const plotRank = (rankPlotInfo, colorTheme) => {
    if (document.getElementById(plotDomId) === null) {
        return;
    }
    if (rankPlotInfo === null) {
        return plotly.react(plotDomId, [], {
            template: colorTheme,
        });
    }
    const layout = {
        xaxis: {
            title: rankPlotInfo.xtitle,
            type: rankPlotInfo.xtype,
        },
        yaxis: {
            title: rankPlotInfo.ytitle,
            type: rankPlotInfo.ytype,
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
    const xValues = rankPlotInfo.xvalues;
    const yValues = rankPlotInfo.yvalues;
    const plotData = [
        {
            type: "scatter",
            x: xValues.filter((_, i) => rankPlotInfo.is_feasible[i]),
            y: yValues.filter((_, i) => rankPlotInfo.is_feasible[i]),
            marker: {
                color: rankPlotInfo.colors.filter((_, i) => rankPlotInfo.is_feasible[i]),
                colorscale: "Portland",
                colorbar: {
                    title: "Rank",
                },
                size: 10,
                line: {
                    color: "Grey",
                    width: 0.5,
                },
            },
            mode: "markers",
            showlegend: false,
            hovertemplate: "%{hovertext}<extra></extra>",
            hovertext: rankPlotInfo.hovertext.filter((_, i) => rankPlotInfo.is_feasible[i]),
        },
        {
            type: "scatter",
            x: xValues.filter((_, i) => !rankPlotInfo.is_feasible[i]),
            y: yValues.filter((_, i) => !rankPlotInfo.is_feasible[i]),
            marker: {
                color: "#cccccc",
                size: 10,
                line: {
                    color: "Grey",
                    width: 0.5,
                },
            },
            mode: "markers",
            showlegend: false,
            hovertemplate: "%{hovertext}<extra></extra>",
            hovertext: rankPlotInfo.hovertext.filter((_, i) => !rankPlotInfo.is_feasible[i]),
        },
    ];
    return plotly.react(plotDomId, plotData, layout);
};
//# sourceMappingURL=GraphRank.js.map