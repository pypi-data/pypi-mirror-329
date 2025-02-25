import ClearIcon from "@mui/icons-material/Clear";
import DeleteIcon from "@mui/icons-material/Delete";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import RestoreFromTrashIcon from "@mui/icons-material/RestoreFromTrash";
import { Box, Card, CardActions, CardContent, Typography, useTheme, } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import { red } from "@mui/material/colors";
import React, { useState } from "react";
import { actionCreator } from "../../action";
import { formatDate } from "../../dateUtil";
import { useArtifactBaseUrlPath } from "../../hooks/useArtifactBaseUrlPath";
import { useStudyDetailValue } from "../../state";
import { getTrialArtifactUrlPath } from "../Artifact/TrialArtifactCards";
import { TrialListDetail } from "../TrialList";
import { PreferentialOutputComponent } from "./PreferentialOutputComponent";
const CandidateTrial = ({ trial, type }) => {
    var _a;
    const theme = useTheme();
    const trialWidth = 300;
    const trialHeight = 300;
    const studyDetail = useStudyDetailValue(trial.study_id);
    const artifactBaseUrl = useArtifactBaseUrlPath();
    const [detailShown, setDetailShown] = useState(false);
    if (studyDetail === null) {
        return null;
    }
    const componentType = studyDetail.feedback_component_type;
    const artifactId = componentType.output_type === "artifact"
        ? (_a = trial.user_attrs.find((a) => a.key === componentType.artifact_key)) === null || _a === void 0 ? void 0 : _a.value
        : undefined;
    const artifact = trial.artifacts.find((a) => a.artifact_id === artifactId);
    const urlPath = artifactId !== undefined
        ? getTrialArtifactUrlPath(artifactBaseUrl, trial.study_id, trial.trial_id, artifactId)
        : "";
    const cardComponentSx = {
        padding: 0,
        position: "relative",
        overflow: "hidden",
        "::before": {},
    };
    if (type !== "none") {
        cardComponentSx["::before"] = {
            content: '""',
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: theme.palette.mode === "dark" ? "white" : "black",
            opacity: 0.2,
            zIndex: 1,
            transition: "opacity 0.3s ease-out",
        };
    }
    return (React.createElement(Card, { sx: {
            width: trialWidth,
            minHeight: trialHeight,
            margin: theme.spacing(2),
            padding: 0,
        } },
        React.createElement(CardActions, null,
            React.createElement(Typography, { variant: "h5" },
                "Trial ",
                trial.number),
            React.createElement(IconButton, { sx: {
                    marginLeft: "auto",
                }, onClick: () => setDetailShown(true), "aria-label": "show detail" },
                React.createElement(OpenInFullIcon, null))),
        React.createElement(CardContent, { "aria-label": "trial", sx: cardComponentSx },
            React.createElement(Box, { component: "div", sx: {
                    padding: theme.spacing(2),
                } },
                React.createElement(PreferentialOutputComponent, { trial: trial, artifact: artifact, componentType: componentType, urlPath: urlPath })),
            type === "worst" ? (React.createElement(ClearIcon, { sx: {
                    position: "absolute",
                    width: "100%",
                    height: "100%",
                    top: 0,
                    left: 0,
                    color: red[600],
                    zIndex: 1,
                    opacity: 0.3,
                    filter: theme.palette.mode === "dark"
                        ? "brightness(1.1)"
                        : "brightness(1.7)",
                } })) : null),
        React.createElement(Modal, { open: detailShown, onClose: () => setDetailShown(false) },
            React.createElement(Box, { component: "div", sx: {
                    position: "absolute",
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    width: "80%",
                    maxHeight: "90%",
                    margin: "auto",
                    overflow: "hidden",
                    backgroundColor: theme.palette.mode === "dark" ? "black" : "white",
                    borderRadius: theme.spacing(3),
                } },
                React.createElement(Box, { component: "div", sx: {
                        width: "100%",
                        height: "100%",
                        overflow: "auto",
                    } },
                    React.createElement(IconButton, { sx: {
                            position: "absolute",
                            top: theme.spacing(2),
                            right: theme.spacing(2),
                        }, onClick: () => setDetailShown(false) },
                        React.createElement(ClearIcon, null)),
                    React.createElement(TrialListDetail, { trial: trial, isBestTrial: () => false, directions: [], metricNames: [] }))))));
};
const ChoiceTrials = ({ choice, trials, studyId }) => {
    const [isRemoved, setRemoved] = useState(choice.is_removed);
    const theme = useTheme();
    const worst_trials = new Set([choice.clicked]);
    const action = actionCreator();
    return (React.createElement(Box, { component: "div", sx: {
            marginBottom: theme.spacing(4),
            position: "relative",
        } },
        React.createElement(Box, { component: "div", sx: {
                display: "flex",
                flexDirection: "row",
                flexWrap: "wrap",
            } },
            React.createElement(Typography, { variant: "h6", sx: {
                    fontWeight: theme.typography.fontWeightLight,
                    margin: "auto 0",
                } }, formatDate(choice.timestamp)),
            choice.is_removed ? (React.createElement(IconButton, { disabled: !isRemoved, onClick: () => {
                    setRemoved(false);
                    action.restorePreferentialHistory(studyId, choice.id);
                }, sx: {
                    margin: `auto ${theme.spacing(2)}`,
                } },
                React.createElement(RestoreFromTrashIcon, null))) : (React.createElement(IconButton, { disabled: isRemoved, onClick: () => {
                    setRemoved(true);
                    action.removePreferentialHistory(studyId, choice.id);
                }, sx: {
                    margin: `auto ${theme.spacing(2)}`,
                } },
                React.createElement(DeleteIcon, null)))),
        React.createElement(Box, { component: "div", sx: {
                display: "flex",
                flexDirection: "row",
                flexWrap: "wrap",
                filter: choice.is_removed ? "brightness(0.4)" : undefined,
                backgroundColor: theme.palette.background.paper,
            } }, choice.candidates.map((trial_num, index) => (React.createElement(CandidateTrial, { key: index, trial: trials[trial_num], type: worst_trials.has(trial_num) ? "worst" : "none" }))))));
};
export const PreferentialHistory = ({ studyDetail, }) => {
    if (studyDetail === null ||
        !studyDetail.is_preferential ||
        studyDetail.preference_history === undefined) {
        return null;
    }
    const theme = useTheme();
    const preference_histories = [...studyDetail.preference_history];
    if (preference_histories.length === 0) {
        return (React.createElement(Typography, { variant: "h5", sx: {
                margin: theme.spacing(4),
                fontWeight: theme.typography.fontWeightBold,
            } }, "No feedback history"));
    }
    return (React.createElement(Box, { component: "div", padding: theme.spacing(2), sx: { display: "flex", flexDirection: "column" } }, preference_histories.reverse().map((choice) => (React.createElement(ChoiceTrials, { key: choice.id, choice: choice, trials: studyDetail.trials, studyId: studyDetail.id })))));
};
//# sourceMappingURL=PreferentialHistory.js.map