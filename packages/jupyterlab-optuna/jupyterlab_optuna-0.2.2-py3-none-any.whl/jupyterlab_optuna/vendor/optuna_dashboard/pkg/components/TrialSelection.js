import DownloadIcon from "@mui/icons-material/Download";
import { Box, Button, Card, CardContent, FormControl, FormControlLabel, Switch, Typography, useTheme, } from "@mui/material";
import { PlotParallelCoordinate, TrialTable } from "@optuna/react";
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useConstants } from "../constantsProvider";
import { studyDetailToStudy } from "../graphUtil";
import { SelectedTrialArtifactCards } from "./Artifact/SelectedTrialArtifactCards";
import { GraphHistory } from "./GraphHistory";
import { GraphParetoFront } from "./GraphParetoFront";
export const TrialSelection = ({ studyDetail, }) => {
    const theme = useTheme();
    const { url_prefix } = useConstants();
    const [selectedTrials, setSelectedTrials] = useState([]);
    const [includeInfeasibleTrials, setIncludeInfeasibleTrials] = useState(true);
    const [includeDominatedTrials, setIncludeDominatedTrials] = useState(true);
    const [showArtifacts, setShowArtifacts] = useState(false);
    const handleSelectionChange = (selectedTrials) => {
        setSelectedTrials(selectedTrials);
    };
    const handleIncludeInfeasibleTrialsChange = () => {
        setIncludeInfeasibleTrials(!includeInfeasibleTrials);
    };
    const handleShowArtifactsChange = () => {
        setShowArtifacts(!showArtifacts);
    };
    const handleIncludeDominatedTrialsChange = () => {
        if (includeDominatedTrials) {
            setIncludeInfeasibleTrials(false);
        }
        setIncludeDominatedTrials(!includeDominatedTrials);
    };
    const study = studyDetailToStudy(studyDetail);
    const linkURL = (studyId, trialNumber) => {
        return url_prefix + `/studies/${studyId}/trials?numbers=${trialNumber}`;
    };
    const width = window.innerWidth - 100;
    return (React.createElement(Box, { component: "div", sx: { display: "flex", width: width, flexDirection: "column" } },
        React.createElement(Typography, { variant: "h5", sx: {
                margin: theme.spacing(2),
                marginTop: theme.spacing(4),
                fontWeight: theme.typography.fontWeightBold,
            } }, "Trial (Selection)"),
        React.createElement(Card, { sx: { margin: theme.spacing(2) } },
            React.createElement(FormControl, { component: "fieldset", sx: {
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "flex-end",
                    padding: theme.spacing(2),
                } },
                studyDetail && (React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: includeInfeasibleTrials, onChange: handleIncludeInfeasibleTrialsChange, value: "enable" }), label: "Include Infeasible trials" })),
                studyDetail && (React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: includeDominatedTrials, onChange: handleIncludeDominatedTrialsChange, disabled: !(studyDetail.directions.length > 1), value: "enable" }), label: "Include dominated trials" })),
                studyDetail && (React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: showArtifacts, onChange: handleShowArtifactsChange, disabled: studyDetail.trials[0].artifacts.length === 0, value: "enable" }), label: "Show Artifacts" }))),
            React.createElement(CardContent, null,
                React.createElement(PlotParallelCoordinate, { study: studyDetail, includeDominatedTrials: includeDominatedTrials, includeInfeasibleTrials: includeInfeasibleTrials, onSelectionChange: handleSelectionChange }))),
        (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.directions.length) === 1 ? (React.createElement(Card, { sx: { margin: theme.spacing(2) } },
            React.createElement(CardContent, null,
                React.createElement(GraphHistory, { studies: studyDetail !== null ? [studyDetail] : [], logScale: false, includePruned: false, selectedTrials: selectedTrials })))) : (React.createElement(Card, { sx: { margin: theme.spacing(2) } },
            React.createElement(CardContent, null,
                React.createElement(GraphParetoFront, { study: studyDetail, selectedTrials: selectedTrials })))),
        studyDetail != null && showArtifacts ? (React.createElement(Card, { sx: { margin: theme.spacing(2) } },
            React.createElement(CardContent, null,
                React.createElement(SelectedTrialArtifactCards, { study: studyDetail, selectedTrials: selectedTrials })))) : null,
        study && (React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "column" } },
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(TrialTable, { study: study, selectedTrials: selectedTrials, linkComponent: Link, linkURL: linkURL }),
                    React.createElement(Button, { variant: "outlined", startIcon: React.createElement(DownloadIcon, null), download: true, href: selectedTrials.length !== study.trials.length
                            ? `/csv/${studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.id}?trial_ids=${selectedTrials.join()}`
                            : `/csv/${studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.id}`, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Download CSV File")))))));
};
//# sourceMappingURL=TrialSelection.js.map