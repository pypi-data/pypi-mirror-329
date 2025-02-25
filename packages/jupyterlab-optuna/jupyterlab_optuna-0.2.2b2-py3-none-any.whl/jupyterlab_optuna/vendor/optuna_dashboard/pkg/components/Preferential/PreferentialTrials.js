import ClearIcon from "@mui/icons-material/Clear";
import FullscreenIcon from "@mui/icons-material/Fullscreen";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import ReplayIcon from "@mui/icons-material/Replay";
import SettingsIcon from "@mui/icons-material/Settings";
import UndoIcon from "@mui/icons-material/Undo";
import { Box, Button, Card, CardActions, CardContent, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle, FormControl, FormLabel, MenuItem, Modal, Select, Typography, useTheme, } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import { red } from "@mui/material/colors";
import React, { useEffect, useState } from "react";
import { actionCreator } from "../../action";
import { useArtifactBaseUrlPath } from "../../hooks/useArtifactBaseUrlPath";
import { isThreejsArtifact, useThreejsArtifactModal, } from "../Artifact/ThreejsArtifactViewer";
import { getTrialArtifactUrlPath } from "../Artifact/TrialArtifactCards";
import { TrialListDetail } from "../TrialList";
import { PreferentialOutputComponent } from "./PreferentialOutputComponent";
const SettingsPage = ({ studyDetail, settingShown, setSettingShown }) => {
    const actions = actionCreator();
    const [outputComponentType, setOutputComponentType] = useState(studyDetail.feedback_component_type.output_type);
    const [artifactKey, setArtifactKey] = useState(studyDetail.feedback_component_type.output_type === "artifact"
        ? studyDetail.feedback_component_type.artifact_key
        : undefined);
    useEffect(() => {
        setOutputComponentType(studyDetail.feedback_component_type.output_type);
    }, [studyDetail.feedback_component_type.output_type]);
    useEffect(() => {
        if (studyDetail.feedback_component_type.output_type === "artifact") {
            setArtifactKey(studyDetail.feedback_component_type.artifact_key);
        }
    }, [
        studyDetail.feedback_component_type.output_type === "artifact"
            ? studyDetail.feedback_component_type.artifact_key
            : undefined,
    ]);
    const onClose = () => {
        setSettingShown(false);
    };
    const onApply = () => {
        setSettingShown(false);
        const outputComponent = outputComponentType === "note"
            ? { output_type: "note" }
            : {
                output_type: "artifact",
                artifact_key: artifactKey,
            };
        actions.updateFeedbackComponent(studyDetail.id, outputComponent);
    };
    return (React.createElement(Dialog, { open: settingShown, onClose: onClose, maxWidth: "sm", fullWidth: true },
        React.createElement(DialogTitle, null, "Settings"),
        React.createElement(DialogContent, { sx: {
                display: "flex",
                flexDirection: "column",
            } },
            React.createElement(FormControl, { component: "fieldset" },
                React.createElement(FormLabel, { component: "legend" }, "Output Component:"),
                React.createElement(Select, { value: outputComponentType, onChange: (e) => {
                        setOutputComponentType(e.target.value);
                    } },
                    React.createElement(MenuItem, { value: "note" }, "Note"),
                    React.createElement(MenuItem, { value: "artifact" }, "Artifact"))),
            outputComponentType === "artifact" ? (React.createElement(FormControl, { component: "fieldset", disabled: studyDetail.union_user_attrs.length === 0 },
                React.createElement(FormLabel, { component: "legend" }, "User Attribute Key Corresponding to Output Artifact Id:"),
                React.createElement(Select, { value: studyDetail.union_user_attrs.length !== 0
                        ? artifactKey !== null && artifactKey !== void 0 ? artifactKey : ""
                        : "error", onChange: (e) => {
                        setArtifactKey(e.target.value);
                    } },
                    studyDetail.union_user_attrs.length === 0 ? (React.createElement(MenuItem, { value: "error" }, "No user attributes")) : null,
                    studyDetail.union_user_attrs.map((attr, index) => {
                        return (React.createElement(MenuItem, { key: index, value: attr.key }, attr.key));
                    })))) : null),
        React.createElement(DialogActions, null,
            React.createElement(Button, { onClick: onClose, color: "primary" }, "Cancel"),
            React.createElement(Button, { onClick: onApply, color: "primary", disabled: outputComponentType === "artifact" && artifactKey === undefined }, "Apply"))));
};
const isComparisonReady = (trial, componentType) => {
    var _a;
    if (componentType === undefined || componentType.output_type === "note") {
        return trial.note.body !== "";
    }
    if (componentType.output_type === "artifact") {
        const artifactId = (_a = trial === null || trial === void 0 ? void 0 : trial.user_attrs.find((a) => a.key === componentType.artifact_key)) === null || _a === void 0 ? void 0 : _a.value;
        const artifact = trial === null || trial === void 0 ? void 0 : trial.artifacts.find((a) => a.artifact_id === artifactId);
        return artifact !== undefined;
    }
    return false;
};
const PreferentialTrial = ({ trial, studyDetail, candidates, hideTrial, openDetailTrial, openThreejsArtifactModal, }) => {
    var _a;
    const theme = useTheme();
    const artifactBaseUrl = useArtifactBaseUrlPath();
    const action = actionCreator();
    const [buttonHover, setButtonHover] = useState(false);
    const trialWidth = 400;
    const trialHeight = 300;
    const componentType = studyDetail.feedback_component_type;
    const artifactId = componentType.output_type === "artifact"
        ? (_a = trial === null || trial === void 0 ? void 0 : trial.user_attrs.find((a) => a.key === componentType.artifact_key)) === null || _a === void 0 ? void 0 : _a.value
        : undefined;
    const artifact = trial === null || trial === void 0 ? void 0 : trial.artifacts.find((a) => a.artifact_id === artifactId);
    const urlPath = trial !== undefined && artifactId !== undefined
        ? getTrialArtifactUrlPath(artifactBaseUrl, studyDetail.id, trial === null || trial === void 0 ? void 0 : trial.trial_id, artifactId)
        : "";
    const is3dModel = componentType.output_type === "artifact" &&
        artifact !== undefined &&
        isThreejsArtifact(artifact);
    if (trial === undefined) {
        return (React.createElement(Box, { component: "div", sx: {
                width: trialWidth,
                minHeight: trialHeight,
                margin: theme.spacing(2),
            } }));
    }
    const onFeedback = () => {
        hideTrial();
        action.updatePreference(trial.study_id, candidates, trial.number);
    };
    const isReady = isComparisonReady(trial, componentType);
    return (React.createElement(Card, { sx: {
            width: trialWidth,
            minHeight: trialHeight,
            margin: theme.spacing(2),
            padding: 0,
            display: "flex",
            flexDirection: "column",
        } },
        React.createElement(CardActions, null,
            React.createElement(Box, { component: "div", sx: {
                    margin: theme.spacing(0, 2),
                    maxWidth: `calc(${trialWidth}px - ${is3dModel ? theme.spacing(8) : theme.spacing(4)})`,
                    overflow: "hidden",
                    display: "flex",
                } },
                React.createElement(Typography, { variant: "h5" },
                    "Trial ",
                    trial.number),
                componentType.output_type === "artifact" &&
                    artifact !== undefined ? (React.createElement(Typography, { variant: "h6", sx: {
                        margin: theme.spacing(0, 2),
                    } }, `(${artifact.filename})`)) : null),
            is3dModel ? (React.createElement(IconButton, { "aria-label": "show artifact 3d model", size: "small", color: "inherit", sx: { marginLeft: "auto" }, onClick: () => {
                    openThreejsArtifactModal(urlPath, artifact);
                } },
                React.createElement(FullscreenIcon, null))) : null,
            React.createElement(IconButton, { sx: {
                    marginLeft: "auto",
                }, onClick: () => {
                    hideTrial();
                    action.skipPreferentialTrial(trial.study_id, trial.trial_id);
                }, "aria-label": "skip trial" },
                React.createElement(ReplayIcon, null)),
            React.createElement(IconButton, { sx: {
                    marginLeft: "auto",
                }, onClick: openDetailTrial, "aria-label": "show detail" },
                React.createElement(OpenInFullIcon, null))),
        React.createElement(CardContent, { "aria-label": "trial-button", onClick: (e) => {
                if (e.shiftKey)
                    onFeedback();
            }, sx: {
                position: "relative",
                padding: theme.spacing(2),
                overflow: "hidden",
                minHeight: theme.spacing(20),
            } }, isReady ? (React.createElement(React.Fragment, null,
            React.createElement(PreferentialOutputComponent, { trial: trial, artifact: artifact, componentType: componentType, urlPath: urlPath }),
            React.createElement(Box, { component: "div", sx: {
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "100%",
                    height: "100%",
                    backgroundColor: theme.palette.mode === "dark" ? "white" : "black",
                    opacity: buttonHover ? 0.2 : 0,
                    zIndex: 1,
                    transition: "opacity 0.3s ease-out",
                    pointerEvents: "none",
                } }),
            React.createElement(ClearIcon, { sx: {
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "100%",
                    height: "100%",
                    color: red[600],
                    opacity: buttonHover ? 0.3 : 0,
                    transition: "opacity 0.3s ease-out",
                    zIndex: 1,
                    filter: buttonHover
                        ? theme.palette.mode === "dark"
                            ? "brightness(1.1)"
                            : "brightness(1.7)"
                        : "none",
                    pointerEvents: "none",
                } }))) : (React.createElement(CircularProgress, { sx: {
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                margin: "auto",
            } }))),
        React.createElement(Button, { variant: "outlined", onClick: onFeedback, onMouseEnter: () => {
                setButtonHover(true);
            }, onMouseLeave: () => {
                setButtonHover(false);
            }, color: "error", disabled: !isReady && candidates.length > 0, sx: {
                marginTop: "auto",
            } },
            React.createElement(ClearIcon, null),
            "Worst")));
};
export const PreferentialTrials = ({ studyDetail, }) => {
    var _a, _b, _c, _d, _e;
    const theme = useTheme();
    const action = actionCreator();
    const [undoHistoryFlag, setUndoHistoryFlag] = useState(false);
    const [openThreejsArtifactModal, renderThreejsArtifactModal] = useThreejsArtifactModal();
    const [displayTrials, setDisplayTrials] = useState({
        display: [],
        clicked: [],
    });
    const [settingShown, setSettingShown] = useState(false);
    const [detailTrial, setDetailTrial] = useState(null);
    if (studyDetail === null || !studyDetail.is_preferential) {
        return null;
    }
    const hiddenTrials = new Set((_b = (_a = studyDetail.preference_history) === null || _a === void 0 ? void 0 : _a.filter((h) => !h.is_removed).map((p) => p.clicked).concat(studyDetail.skipped_trial_numbers)) !== null && _b !== void 0 ? _b : []);
    const activeTrials = studyDetail.trials.filter((t) => (t.state === "Running" || t.state === "Complete") &&
        !hiddenTrials.has(t.number));
    const newTrials = activeTrials.filter((t) => !displayTrials.display.includes(t.number) &&
        !displayTrials.clicked.includes(t.number));
    const deleteTrials = displayTrials.display.filter((t) => t !== -1 && !activeTrials.map((t) => t.number).includes(t));
    if (newTrials.length > 0 || deleteTrials.length > 0) {
        setDisplayTrials((prev) => {
            const display = [...prev.display].map((t) => deleteTrials.includes(t) ? -1 : t);
            const clicked = [...prev.clicked];
            newTrials.map((t) => {
                const index = display.findIndex((n) => n === -1);
                if (index === -1) {
                    display.push(t.number);
                    clicked.push(-1);
                }
                else {
                    display[index] = t.number;
                }
            });
            return {
                display: display,
                clicked: clicked,
            };
        });
    }
    const hideTrial = (num) => {
        setDisplayTrials((prev) => {
            const index = prev.display.findIndex((n) => n === num);
            if (index === -1) {
                return prev;
            }
            const display = [...prev.display];
            const clicked = [...prev.clicked];
            display[index] = -1;
            clicked[index] = num;
            return {
                display: display,
                clicked: clicked,
            };
        });
    };
    const visibleTrial = (num) => {
        setDisplayTrials((prev) => {
            const index = prev.clicked.findIndex((n) => n === num);
            if (index === -1) {
                return prev;
            }
            const clicked = [...prev.clicked];
            clicked[index] = -1;
            return {
                display: prev.display,
                clicked: clicked,
            };
        });
    };
    const latestHistoryId = (_e = (_d = (_c = studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.preference_history) === null || _c === void 0 ? void 0 : _c.filter((h) => !h.is_removed).pop()) === null || _d === void 0 ? void 0 : _d.id) !== null && _e !== void 0 ? _e : null;
    return (React.createElement(Box, { component: "div", padding: theme.spacing(2) },
        React.createElement(Box, { component: "div", display: "flex" },
            React.createElement(Typography, { variant: "h4", sx: {
                    fontWeight: theme.typography.fontWeightBold,
                } }, "Which trial is the worst?"),
            React.createElement(Box, { component: "div", display: "flex", sx: {
                    marginLeft: "auto",
                } },
                React.createElement(Button, { variant: "outlined", disabled: latestHistoryId === null || undoHistoryFlag, sx: {
                        marginRight: theme.spacing(2),
                    }, startIcon: React.createElement(UndoIcon, null), onClick: () => {
                        var _a, _b, _c;
                        if (latestHistoryId === null) {
                            return;
                        }
                        setUndoHistoryFlag(true);
                        const clicked = (_c = (_b = (_a = studyDetail.preference_history) === null || _a === void 0 ? void 0 : _a.filter((h) => h.id === latestHistoryId)) === null || _b === void 0 ? void 0 : _b.pop()) === null || _c === void 0 ? void 0 : _c.clicked;
                        if (clicked !== undefined)
                            visibleTrial(clicked);
                        action.removePreferentialHistory(studyDetail.id, latestHistoryId);
                        setUndoHistoryFlag(false);
                    } }, "Undo"),
                React.createElement(Button, { variant: "outlined", sx: {
                        marginRight: theme.spacing(2),
                    }, startIcon: React.createElement(SettingsIcon, null), onClick: () => setSettingShown(true) }, "Settings"))),
        React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", flexWrap: "wrap" } }, displayTrials.display.map((t, index) => {
            const trial = activeTrials.find((trial) => trial.number === t);
            const candidates = displayTrials.display.filter((n) => n !== -1 &&
                isComparisonReady(studyDetail.trials[n], studyDetail.feedback_component_type));
            return (React.createElement(PreferentialTrial, { key: t === -1 ? -index - 1 : t, trial: trial, studyDetail: studyDetail, candidates: candidates, hideTrial: () => hideTrial(t), openDetailTrial: () => setDetailTrial(t), openThreejsArtifactModal: openThreejsArtifactModal }));
        })),
        React.createElement(SettingsPage, { settingShown: settingShown, setSettingShown: setSettingShown, studyDetail: studyDetail }),
        detailTrial !== null && (React.createElement(Modal, { open: true, onClose: () => setDetailTrial(null) },
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
                    backgroundColor: theme.palette.background.default,
                    borderRadius: theme.spacing(3),
                } },
                React.createElement(Box, { component: "div", sx: {
                        width: "100%",
                        height: "100%",
                        overflow: "auto",
                        position: "relative",
                    } },
                    React.createElement(IconButton, { sx: {
                            position: "absolute",
                            top: theme.spacing(2),
                            right: theme.spacing(2),
                        }, onClick: () => setDetailTrial(null) },
                        React.createElement(ClearIcon, null)),
                    React.createElement(TrialListDetail, { trial: studyDetail.trials[detailTrial], isBestTrial: (trialId) => {
                            var _a, _b;
                            return (_b = ((_a = studyDetail.trials.find((t) => t.trial_id === trialId)) === null || _a === void 0 ? void 0 : _a.state) === "Complete") !== null && _b !== void 0 ? _b : false;
                        }, directions: [], metricNames: [] }))))),
        renderThreejsArtifactModal()));
};
//# sourceMappingURL=PreferentialTrials.js.map