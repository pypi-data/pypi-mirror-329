import { Box, Card, CardContent, FormControl, Switch, Typography, useTheme, } from "@mui/material";
import FormControlLabel from "@mui/material/FormControlLabel";
import Grid from "@mui/material/Grid";
import { DataGrid } from "@optuna/react";
import React, { useState } from "react";
import { useRecoilValue } from "recoil";
import { useStudyDetailValue, useStudyDirections, useStudySummaryValue, } from "../state";
import { artifactIsAvailable } from "../state";
import { StudyArtifactCards } from "./Artifact/StudyArtifactCards";
import { BestTrialsCard } from "./BestTrialsCard";
import { GraphHistory } from "./GraphHistory";
import { GraphHyperparameterImportance } from "./GraphHyperparameterImportances";
import { GraphIntermediateValues } from "./GraphIntermediateValues";
import { GraphParetoFront } from "./GraphParetoFront";
import { GraphTimeline } from "./GraphTimeline";
import { UserDefinedPlot } from "./UserDefinedPlot";
import { createColumnHelper } from "@tanstack/react-table";
export const StudyHistory = ({ studyId }) => {
    const theme = useTheme();
    const directions = useStudyDirections(studyId);
    const studySummary = useStudySummaryValue(studyId);
    const studyDetail = useStudyDetailValue(studyId);
    const [logScale, setLogScale] = useState(false);
    const [includePruned, setIncludePruned] = useState(true);
    const artifactEnabled = useRecoilValue(artifactIsAvailable);
    const handleLogScaleChange = () => {
        setLogScale(!logScale);
    };
    const handleIncludePrunedChange = () => {
        setIncludePruned(!includePruned);
    };
    const userAttrs = (studySummary === null || studySummary === void 0 ? void 0 : studySummary.user_attrs) || (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.user_attrs) || [];
    const columnHelper = createColumnHelper();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const columns = [
        columnHelper.accessor("key", {
            header: "Key",
            enableSorting: true,
            enableColumnFilter: false,
        }),
        columnHelper.accessor("value", {
            header: "Value",
            enableSorting: true,
            enableColumnFilter: false,
        }),
    ];
    const trials = (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.trials) || [];
    return (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%", flexDirection: "column" } },
        React.createElement(FormControl, { component: "fieldset", sx: {
                display: "flex",
                flexDirection: "row",
                justifyContent: "flex-end",
                padding: theme.spacing(2),
            } },
            React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: logScale, onChange: handleLogScaleChange, value: "enable" }), label: "Log y scale" }),
            React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: studyDetail
                        ? studyDetail.has_intermediate_values && includePruned
                        : false, onChange: handleIncludePrunedChange, disabled: !(studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.has_intermediate_values), value: "enable" }), label: "Include PRUNED trials" })),
        directions !== null && directions.length > 1 ? (React.createElement(Card, { sx: { margin: theme.spacing(2) } },
            React.createElement(CardContent, null,
                React.createElement(GraphParetoFront, { study: studyDetail })))) : null,
        React.createElement(Card, { sx: {
                margin: theme.spacing(2),
            } },
            React.createElement(CardContent, null,
                React.createElement(GraphHistory, { studies: studyDetail !== null ? [studyDetail] : [], includePruned: includePruned, logScale: logScale }))),
        React.createElement(Grid, { container: true, spacing: 2, sx: { padding: theme.spacing(0, 2) } },
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(GraphHyperparameterImportance, { studyId: studyId, study: studyDetail, graphHeight: "450px" })),
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(GraphTimeline, { study: studyDetail })),
            studyDetail !== null &&
                studyDetail.plotly_graph_objects.map((go) => (React.createElement(Grid, { xs: 6, key: go.id },
                    React.createElement(Card, null,
                        React.createElement(CardContent, null,
                            React.createElement(UserDefinedPlot, { graphObject: go })))))),
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(BestTrialsCard, { studyDetail: studyDetail })),
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(Card, null,
                    React.createElement(CardContent, { sx: {
                            display: "flex",
                            flexDirection: "column",
                        } },
                        React.createElement(Typography, { variant: "h6", sx: {
                                margin: "1em 0",
                                fontWeight: theme.typography.fontWeightBold,
                            } }, "Study User Attributes"),
                        React.createElement(DataGrid, { data: userAttrs, columns: columns })))),
            studyDetail !== null &&
                studyDetail.directions.length === 1 &&
                studyDetail.has_intermediate_values ? (React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(GraphIntermediateValues, { trials: trials, includePruned: includePruned, logScale: logScale }))) : null),
        artifactEnabled && studyDetail !== null && (React.createElement(Grid, { container: true, spacing: 2, sx: { padding: theme.spacing(2) } },
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(Card, null,
                    React.createElement(CardContent, { sx: {
                            display: "flex",
                            flexDirection: "column",
                        } },
                        React.createElement(Typography, { variant: "h6", sx: {
                                margin: "1em 0",
                                fontWeight: theme.typography.fontWeightBold,
                            } }, "Study Artifacts"),
                        React.createElement(StudyArtifactCards, { study: studyDetail }))))))));
};
//# sourceMappingURL=StudyHistory.js.map