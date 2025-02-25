import LinkIcon from "@mui/icons-material/Link";
import { Box, Button, Card, CardContent, Divider, List, ListItem, ListItemButton, ListItemText, Typography, useTheme, } from "@mui/material";
import React, { useMemo } from "react";
import { Link } from "react-router-dom";
import { useConstants } from "../constantsProvider";
const useBestTrials = (studyDetail) => {
    return useMemo(() => (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.best_trials) || [], [studyDetail]);
};
export const BestTrialsCard = ({ studyDetail }) => {
    var _a;
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const bestTrials = useBestTrials(studyDetail);
    let header = "Best Trials";
    let content = null;
    if (bestTrials.length === 1) {
        const bestTrial = bestTrials[0];
        header = `Best Trial (number=${bestTrial.number})`;
        content = (React.createElement(React.Fragment, null,
            !(studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.is_preferential) &&
                (bestTrial.values === undefined || bestTrial.values.length === 1 ? (React.createElement(Typography, { variant: "h3", sx: {
                        fontWeight: theme.typography.fontWeightBold,
                        marginBottom: theme.spacing(2),
                    }, color: "secondary" }, bestTrial.values)) : (React.createElement(Typography, null,
                    "Objective Values = [", (_a = bestTrial.values) === null || _a === void 0 ? void 0 :
                    _a.join(", "),
                    "]"))),
            React.createElement(Typography, null,
                "Params = [",
                bestTrial.params
                    .map((p) => `${p.name}: ${p.param_external_value}`)
                    .join(", "),
                "]"),
            React.createElement(Button, { variant: "outlined", startIcon: React.createElement(LinkIcon, null), component: Link, to: `${url_prefix}/studies/${bestTrial.study_id}/trials?numbers=${bestTrial.number}`, sx: { margin: theme.spacing(1) } }, "Details")));
    }
    else if (bestTrials.length > 1) {
        content = (React.createElement(React.Fragment, null,
            React.createElement(Divider, { sx: { paddingBottom: theme.spacing(1) }, orientation: "horizontal" }),
            React.createElement(Box, { component: "div", sx: {
                    overflow: "auto",
                    height: "450px",
                    width: "100%",
                } },
                React.createElement(List, null, bestTrials.map((trial) => {
                    var _a;
                    return (React.createElement(ListItem, { key: trial.number, disablePadding: true },
                        React.createElement(ListItemButton, { component: Link, to: url_prefix +
                                `/studies/${trial.study_id}/trials?numbers=${trial.number}`, sx: { flexDirection: "column", alignItems: "flex-start" } },
                            React.createElement(ListItemText, { primary: React.createElement(Typography, { variant: "h5" },
                                    "Trial ",
                                    trial.number) }),
                            (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.is_preferential) ? null : (React.createElement(Typography, null,
                                "Objective Values = [", (_a = trial.values) === null || _a === void 0 ? void 0 :
                                _a.join(", "),
                                "]")),
                            React.createElement(Typography, null,
                                "Params = [",
                                trial.params
                                    .map((p) => `${p.name}: ${p.param_external_value}`)
                                    .join(", "),
                                "]"))));
                })))));
    }
    return (React.createElement(Card, null,
        React.createElement(CardContent, { sx: {
                display: "inline-content",
                flexDirection: "column",
            } },
            React.createElement(Typography, { variant: "h6", sx: { margin: "1em 0", fontWeight: theme.typography.fontWeightBold } }, header),
            content)));
};
//# sourceMappingURL=BestTrialsCard.js.map