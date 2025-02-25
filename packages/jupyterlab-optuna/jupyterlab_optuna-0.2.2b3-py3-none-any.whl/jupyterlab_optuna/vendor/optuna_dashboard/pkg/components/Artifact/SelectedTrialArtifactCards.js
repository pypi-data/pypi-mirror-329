import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";
import FullscreenIcon from "@mui/icons-material/Fullscreen";
import { Box, Card, CardContent, FormControl, FormLabel, IconButton, MenuItem, Select, Stack, Typography, useTheme, } from "@mui/material";
import React, { useMemo, useState } from "react";
import { ArtifactCardMedia } from "./ArtifactCardMedia";
import { useDeleteTrialArtifactDialog } from "./DeleteArtifactDialog";
import { isTableArtifact, useTableArtifactModal } from "./TableArtifactViewer";
import { isThreejsArtifact, useThreejsArtifactModal, } from "./ThreejsArtifactViewer";
export const SelectedTrialArtifactCards = ({ study, selectedTrials }) => {
    const theme = useTheme();
    const [openDeleteArtifactDialog, renderDeleteArtifactDialog] = useDeleteTrialArtifactDialog();
    const [openThreejsArtifactModal, renderThreejsArtifactModal] = useThreejsArtifactModal();
    const [openTableArtifactModal, renderTableArtifactModal] = useTableArtifactModal();
    const isArtifactModifiable = (trial) => {
        return trial.state === "Running" || trial.state === "Waiting";
    };
    const [targetArtifactId, setTargetArtifactId] = useState(0);
    const [targetValueId, setTargetValueId] = useState(0);
    const handleTargetArtifactChange = (event) => {
        setTargetArtifactId(event.target.value);
    };
    const handleTargetValueChange = (event) => {
        setTargetValueId(event.target.value);
    };
    const trials = useMemo(() => {
        if (!selectedTrials || selectedTrials.length === 0) {
            return study.trials;
        }
        const selectedTrialsSet = new Set(selectedTrials);
        return study.trials.filter((t) => selectedTrialsSet.has(t.number));
    }, [selectedTrials, study.trials]);
    const width = "200px";
    const height = "150px";
    const metricNames = (study === null || study === void 0 ? void 0 : study.metric_names) || [];
    const valueRanges = calculateMinMax(trials.map((trial) => trial.values));
    const direction = study.directions[targetValueId];
    return (React.createElement(React.Fragment, null,
        React.createElement(Stack, { direction: { xs: "column", sm: "row" }, spacing: 3, sx: { width: "100%" } },
            React.createElement(Typography, { variant: "h5", sx: { fontWeight: theme.typography.fontWeightBold } }, "Artifacts"),
            React.createElement(FormControl, { component: "fieldset" },
                React.createElement(FormLabel, { component: "legend" }, "Target Artifact Index:"),
                React.createElement(Select, { value: targetArtifactId, onChange: handleTargetArtifactChange }, study.trials[0].artifacts.map((_d, i) => (React.createElement(MenuItem, { value: i, key: i },
                    "artifact: ",
                    i))))),
            React.createElement(FormControl, { component: "fieldset" },
                React.createElement(FormLabel, { component: "legend" }, "Border Color Objective Value:"),
                React.createElement(Select, { value: targetValueId, onChange: handleTargetValueChange }, study.directions.map((_d, i) => (React.createElement(MenuItem, { value: i, key: i }, metricNames.length === (study === null || study === void 0 ? void 0 : study.directions.length)
                    ? metricNames[i]
                    : `${i}`)))))),
        React.createElement(Box, { component: "div", sx: { display: "flex", flexWrap: "wrap", p: theme.spacing(1, 0) } }, trials.map((trial) => {
            const artifact = trial.artifacts[targetArtifactId];
            if (!artifact || !artifact.artifact_id) {
                return null;
            }
            const urlPath = `/artifacts/${trial.study_id}/${trial.trial_id}/${artifact.artifact_id}`;
            const value = trial.values
                ? trial.values[targetValueId]
                : valueRanges.min[targetValueId];
            const borderValue = calculateBorderColor(value, valueRanges.min[targetValueId], valueRanges.max[targetValueId], direction);
            const border = `5px solid ${borderValue}`;
            return (React.createElement(Card, { key: artifact.artifact_id, sx: {
                    marginBottom: theme.spacing(2),
                    width: width,
                    margin: theme.spacing(0, 1, 1, 0),
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    border: border,
                } },
                React.createElement(ArtifactCardMedia, { artifact: artifact, urlPath: urlPath, height: height }),
                React.createElement(CardContent, { sx: {
                        display: "flex",
                        flexDirection: "row",
                        padding: `${theme.spacing(1)} !important`,
                    } },
                    React.createElement(Typography, { sx: {
                            p: theme.spacing(0.5, 0),
                            flexGrow: 1,
                            wordBreak: "break-all",
                            maxWidth: `calc(100% - ${theme.spacing(4 +
                                (isThreejsArtifact(artifact) ? 4 : 0) +
                                (isArtifactModifiable(trial) ? 4 : 0))})`,
                        } }, "Trial id: " + trial.number),
                    isThreejsArtifact(artifact) ? (React.createElement(IconButton, { "aria-label": "show artifact 3d model", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                            openThreejsArtifactModal(urlPath, artifact);
                        } },
                        React.createElement(FullscreenIcon, null))) : null,
                    isTableArtifact(artifact) ? (React.createElement(IconButton, { "aria-label": "show artifact table", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                            openTableArtifactModal(urlPath, artifact);
                        } },
                        React.createElement(FullscreenIcon, null))) : null,
                    isArtifactModifiable(trial) ? (React.createElement(IconButton, { "aria-label": "delete artifact", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                            openDeleteArtifactDialog(trial.study_id, trial.trial_id, artifact);
                        } },
                        React.createElement(DeleteIcon, null))) : null,
                    React.createElement(IconButton, { "aria-label": "download artifact", size: "small", color: "inherit", download: artifact.filename, sx: { margin: "auto 0" }, href: urlPath },
                        React.createElement(DownloadIcon, null)))));
        })),
        renderDeleteArtifactDialog(),
        renderThreejsArtifactModal(),
        renderTableArtifactModal()));
};
function calculateMinMax(values) {
    if (values.length === 0) {
        return { min: [], max: [] };
    }
    const firstValidArray = values.find((arr) => arr !== undefined);
    if (!firstValidArray) {
        return { min: [], max: [] };
    }
    const length = firstValidArray.length;
    const mins = new Array(length).fill(Infinity);
    const maxs = new Array(length).fill(-Infinity);
    values.forEach((arr) => {
        if (arr === undefined)
            return;
        arr.forEach((value, index) => {
            if (index < length) {
                mins[index] = Math.min(mins[index], value);
                maxs[index] = Math.max(maxs[index], value);
            }
        });
    });
    const result = {
        min: mins.map((val) => (val === Infinity ? 0 : val)),
        max: maxs.map((val) => (val === -Infinity ? 0 : val)),
    };
    return result;
}
function calculateBorderColor(value, minValue, maxValue, direction = "minimize") {
    if (minValue === maxValue) {
        return "rgb(255, 255, 255)";
    }
    let normalizedValue = (value - minValue) / (maxValue - minValue);
    if (direction === "maximize") {
        normalizedValue = 1 - normalizedValue;
    }
    const red = Math.round(255 * normalizedValue);
    const green = Math.round(255 * normalizedValue);
    const blue = 255;
    return `rgb(${red}, ${green}, ${blue})`;
}
//# sourceMappingURL=SelectedTrialArtifactCards.js.map