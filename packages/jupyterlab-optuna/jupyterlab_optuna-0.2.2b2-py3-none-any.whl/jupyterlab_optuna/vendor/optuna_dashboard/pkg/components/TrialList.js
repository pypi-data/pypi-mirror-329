import CheckBoxIcon from "@mui/icons-material/CheckBox";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import FilterListIcon from "@mui/icons-material/FilterList";
import StopCircleIcon from "@mui/icons-material/StopCircle";
import { Box, Button, IconButton, Menu, MenuItem, Typography, useTheme, } from "@mui/material";
import Chip from "@mui/material/Chip";
import Divider from "@mui/material/Divider";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import React, { useMemo } from "react";
import ListItemIcon from "@mui/material/ListItemIcon";
import { useVirtualizer } from "@tanstack/react-virtual";
import { useNavigate } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { actionCreator } from "../action";
import { useConstants } from "../constantsProvider";
import { artifactIsAvailable } from "../state";
import { useQuery } from "../urlQuery";
import { TrialArtifactCards } from "./Artifact/TrialArtifactCards";
import { TrialNote } from "./Note";
import { TrialFormWidgets } from "./TrialFormWidgets";
const states = [
    "Complete",
    "Pruned",
    "Fail",
    "Running",
    "Waiting",
];
const getChipColor = (state) => {
    if (state === "Complete") {
        return "primary";
    }
    else if (state === "Running") {
        return "default";
    }
    else if (state === "Waiting") {
        return "default";
    }
    else if (state === "Pruned") {
        return "warning";
    }
    else if (state === "Fail") {
        return "error";
    }
    return "default";
};
const useExcludedStates = (query) => {
    return useMemo(() => {
        const exclude = query.get("exclude");
        if (exclude === null) {
            return [];
        }
        const excluded = exclude
            .split(",")
            .map((s) => {
            return states.find((state) => state.toUpperCase() === s.toUpperCase());
        })
            .filter((s) => s !== undefined);
        return excluded;
    }, [query]);
};
const useTrials = (studyDetail, excludedStates) => {
    return useMemo(() => {
        let result = studyDetail !== null ? studyDetail.trials : [];
        if (excludedStates.length === 0) {
            return result;
        }
        excludedStates.forEach((s) => {
            result = result.filter((t) => t.state !== s);
        });
        return result;
    }, [studyDetail, excludedStates]);
};
const useQueriedTrials = (trials, query) => {
    return useMemo(() => {
        const queried = query.get("numbers");
        if (queried === null) {
            return [];
        }
        const numbers = queried
            .split(",")
            .map((s) => parseInt(s))
            .filter((n) => !isNaN(n));
        return trials.filter((t) => numbers.findIndex((n) => n === t.number) !== -1);
    }, [trials, query]);
};
const useIsBestTrial = (studyDetail) => {
    return useMemo(() => {
        const bestTrialIDs = (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.best_trials.map((t) => t.trial_id)) || [];
        return (trialId) => bestTrialIDs.findIndex((a) => a === trialId) !== -1;
    }, [studyDetail]);
};
export const TrialListDetail = ({ trial, isBestTrial, directions, metricNames, formWidgets }) => {
    var _a, _b, _c;
    const theme = useTheme();
    const action = actionCreator();
    const artifactEnabled = useRecoilValue(artifactIsAvailable);
    const startMs = (_a = trial.datetime_start) === null || _a === void 0 ? void 0 : _a.getTime();
    const completeMs = (_b = trial.datetime_complete) === null || _b === void 0 ? void 0 : _b.getTime();
    const params = trial.state === "Waiting" ? trial.fixed_params : trial.params;
    const info = [
        ["Value", ((_c = trial.values) === null || _c === void 0 ? void 0 : _c.map((v) => v.toString()).join(", ")) || "None"],
        [
            "Intermediate Values",
            React.createElement(Box, { component: "div" }, trial.intermediate_values.map((v) => (React.createElement(Typography, { key: v.step },
                v.step,
                " ",
                v.value)))),
        ],
        [
            "Parameter",
            React.createElement(Box, { component: "div" }, params.map((p) => (React.createElement(Typography, { key: p.name },
                p.name,
                " ",
                p.param_external_value)))),
        ],
        [
            "Started At",
            (trial === null || trial === void 0 ? void 0 : trial.datetime_start) ? trial === null || trial === void 0 ? void 0 : trial.datetime_start.toString() : null,
        ],
        [
            "Completed At",
            (trial === null || trial === void 0 ? void 0 : trial.datetime_complete) ? trial === null || trial === void 0 ? void 0 : trial.datetime_complete.toString() : null,
        ],
        [
            "Duration (ms)",
            startMs !== undefined && completeMs !== undefined
                ? (completeMs - startMs).toString()
                : null,
        ],
        [
            "User Attributes",
            React.createElement(Box, { component: "div" }, trial.user_attrs.map((t) => (React.createElement(Typography, { key: t.key },
                t.key,
                " ",
                t.value)))),
        ],
    ];
    const renderInfo = (key, value) => (React.createElement(Box, { component: "div", key: key, sx: {
            display: "flex",
            flexDirection: "row",
            marginBottom: theme.spacing(0.5),
        } },
        React.createElement(Typography, { sx: { p: theme.spacing(1) }, color: "text.secondary", minWidth: "200px", fontWeight: theme.typography.fontWeightLight, fontSize: theme.typography.fontSize }, key),
        React.createElement(Box, { component: "div", sx: {
                bgcolor: theme.palette.mode === "dark"
                    ? "rgba(255, 255, 255, 0.05)"
                    : "rgba(0, 0, 0, 0.05)",
                width: "100%",
                maxHeight: "150px",
                overflow: "auto",
                p: theme.spacing(0.5, 1),
                borderRadius: theme.shape.borderRadius * 0.2,
                display: "flex",
                whiteSpace: "nowrap",
            } }, value)));
    return (React.createElement(Box, { component: "div", sx: { width: "100%", padding: theme.spacing(2, 2, 0, 2) } },
        React.createElement(Typography, { variant: "h4", sx: {
                marginBottom: theme.spacing(2),
                fontWeight: theme.typography.fontWeightBold,
            } },
            "Trial ",
            trial.number,
            " (trial_id=",
            trial.trial_id,
            ")"),
        React.createElement(Box, { component: "div", sx: {
                marginBottom: theme.spacing(1),
                display: "flex",
                flexDirection: "row",
            } },
            React.createElement(Chip, { color: getChipColor(trial.state), label: trial.state, sx: { marginRight: theme.spacing(1) }, variant: "outlined" }),
            isBestTrial(trial.trial_id) ? (React.createElement(Chip, { label: "Best Trial", color: "secondary", variant: "outlined" })) : null,
            React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
            trial.state === "Running" ? (React.createElement(Button, { variant: "outlined", size: "small", color: "error", startIcon: React.createElement(StopCircleIcon, null), onClick: () => {
                    action.makeTrialFail(trial.study_id, trial.trial_id);
                } }, "Fail Trial")) : null),
        React.createElement(Typography, { variant: "h5", sx: {
                fontWeight: theme.typography.fontWeightBold,
                marginBottom: theme.spacing(1),
            } }, "Note"),
        React.createElement(TrialNote, { studyId: trial.study_id, trialId: trial.trial_id, latestNote: trial.note, cardSx: { marginBottom: theme.spacing(2) } }),
        React.createElement(TrialFormWidgets, { trial: trial, directions: directions, metricNames: metricNames, formWidgets: formWidgets }),
        React.createElement(Box, { component: "div", sx: {
                marginBottom: theme.spacing(2),
                display: "flex",
                flexDirection: "column",
            } }, info.map(([key, value]) => value !== null ? renderInfo(key, value) : null)),
        artifactEnabled && React.createElement(TrialArtifactCards, { trial: trial })));
};
const getTrialListLink = (studyId, exclude, numbers, URL_PREFIX) => {
    const base = URL_PREFIX + `/studies/${studyId}/trials`;
    if (exclude.length > 0 && numbers.length > 0) {
        return (base +
            `?exclude=${exclude.join(",")}&numbers=${numbers
                .map((n) => n.toString())
                .join(",")}`);
    }
    else if (exclude.length > 0) {
        return base + "?exclude=" + exclude.join(",");
    }
    else if (numbers.length > 0) {
        return base + "?numbers=" + numbers.map((n) => n.toString()).join(",");
    }
    return base;
};
export const TrialList = ({ studyDetail, }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const query = useQuery();
    const navigate = useNavigate();
    const excludedStates = useExcludedStates(query);
    const trials = useTrials(studyDetail, excludedStates);
    const isBestTrial = useIsBestTrial(studyDetail);
    const queried = useQueriedTrials(trials, query);
    const [filterMenuAnchorEl, setFilterMenuAnchorEl] = React.useState(null);
    const openFilterMenu = Boolean(filterMenuAnchorEl);
    const trialCounts = useMemo(() => {
        const allTrials = (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.trials) || [];
        return states.map((state) => allTrials.filter((t) => t.state === state).length);
    }, [studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.trials]);
    const listParentRef = React.useRef(null);
    const rowVirtualizer = useVirtualizer({
        count: trials.length,
        getScrollElement: () => listParentRef.current,
        estimateSize: () => 73.31,
        overscan: 10,
    });
    const trialListWidth = 200;
    const selected = queried.length > 0 ? queried : trials.length > 0 ? [trials[0]] : [];
    return (React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", width: "100%" } },
        React.createElement(Box, { component: "div", ref: listParentRef, sx: {
                minWidth: trialListWidth,
                overflow: "auto",
                height: `calc(100vh - ${theme.spacing(8)})`,
            } },
            React.createElement(List, { sx: { position: "relative" } },
                React.createElement(ListSubheader, { sx: { display: "flex", flexDirection: "row" } },
                    React.createElement(Typography, { sx: { p: theme.spacing(1, 0) } },
                        trials.length,
                        " Trials"),
                    React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
                    React.createElement(IconButton, { "aria-label": "Filter", "aria-controls": openFilterMenu ? "filter-trials" : undefined, "aria-haspopup": "true", "aria-expanded": openFilterMenu ? "true" : undefined, onClick: (e) => {
                            setFilterMenuAnchorEl(e.currentTarget);
                        } },
                        React.createElement(FilterListIcon, { fontSize: "small" })),
                    React.createElement(Menu, { anchorEl: filterMenuAnchorEl, id: "filter-trials", open: openFilterMenu, onClose: () => {
                            setFilterMenuAnchorEl(null);
                        } }, states.map((state, i) => (React.createElement(MenuItem, { key: state, onClick: () => {
                            if (studyDetail === null) {
                                return;
                            }
                            const index = excludedStates.findIndex((s) => s === state);
                            if (index === -1) {
                                excludedStates.push(state);
                            }
                            else {
                                excludedStates.splice(index, 1);
                            }
                            const numbers = selected.map((t) => t.number);
                            navigate(getTrialListLink(studyDetail.id, excludedStates, numbers, url_prefix));
                        }, disabled: trialCounts[i] === 0 },
                        React.createElement(ListItemIcon, null, excludedStates.find((s) => s === state) !== undefined ? (React.createElement(CheckBoxOutlineBlankIcon, { color: "primary" })) : (React.createElement(CheckBoxIcon, { color: "primary" }))),
                        state,
                        " (",
                        trialCounts[i],
                        ")"))))),
                React.createElement(Divider, null),
                React.createElement(Box, { component: "div", sx: {
                        width: "100%",
                        height: `${rowVirtualizer.getTotalSize()}px`,
                        position: "relative",
                    } }, rowVirtualizer.getVirtualItems().map((virtualItem) => {
                    const trial = trials[virtualItem.index];
                    return (React.createElement(ListItem, { key: trial.trial_id, sx: {
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "flex-start",
                            position: "absolute",
                            top: 0,
                            left: 0,
                            transform: `translateY(${virtualItem.start}px)`,
                        }, disablePadding: true },
                        React.createElement(ListItemButton, { onClick: (e) => {
                                if (e.shiftKey) {
                                    let next;
                                    const selectedNumbers = selected.map((t) => t.number);
                                    const alreadySelected = selectedNumbers.findIndex((n) => n === trial.number) >= 0;
                                    if (alreadySelected) {
                                        next = selectedNumbers.filter((n) => n !== trial.number);
                                    }
                                    else {
                                        next = [...selectedNumbers, trial.number];
                                    }
                                    navigate(getTrialListLink(trial.study_id, excludedStates, next, url_prefix));
                                }
                                else {
                                    navigate(getTrialListLink(trial.study_id, excludedStates, [trial.number], url_prefix));
                                }
                            }, selected: selected.findIndex((t) => t.number === trial.number) !==
                                -1, sx: {
                                width: "100%",
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "flex-start",
                            } },
                            React.createElement(ListItemText, { primary: `Trial ${trial.number}` }),
                            React.createElement(Box, { component: "div" },
                                React.createElement(Chip, { color: getChipColor(trial.state), label: trial.state, sx: { margin: theme.spacing(0) }, size: "small", variant: "outlined" }),
                                isBestTrial(trial.trial_id) ? (React.createElement(Chip, { label: "Best Trial", color: "secondary", sx: { marginLeft: theme.spacing(1) }, size: "small", variant: "outlined" })) : null))));
                })))),
        React.createElement(Divider, { orientation: "vertical", flexItem: true }),
        React.createElement(Box, { component: "div", sx: {
                flexGrow: 1,
                overflow: "auto",
                height: `calc(100vh - ${theme.spacing(8)})`,
            } },
            React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", width: "100%" } }, selected.length === 0
                ? null
                : selected.map((t) => (React.createElement(TrialListDetail, { key: t.trial_id, trial: t, isBestTrial: isBestTrial, directions: (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.directions) || [], metricNames: (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.metric_names) || [], formWidgets: studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.form_widgets })))))));
};
//# sourceMappingURL=TrialList.js.map