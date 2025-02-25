import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DownloadIcon from "@mui/icons-material/Download";
import HomeIcon from "@mui/icons-material/Home";
import { Box, Button, Card, CardContent, IconButton, Typography, useTheme, } from "@mui/material";
import Grid from "@mui/material/Grid";
import React, { useEffect, useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { TrialTable } from "@optuna/react";
import { actionCreator } from "../action";
import { useConstants } from "../constantsProvider";
import { studyDetailToStudy } from "../graphUtil";
import { reloadIntervalState, useStudyDetailValue, useStudyIsPreferential, useStudyName, } from "../state";
import { AppDrawer } from "./AppDrawer";
import { Contour } from "./GraphContour";
import { GraphEdf } from "./GraphEdf";
import { GraphParallelCoordinate } from "./GraphParallelCoordinate";
import { GraphRank } from "./GraphRank";
import { GraphSlice } from "./GraphSlice";
import { StudyNote } from "./Note";
import { PreferentialAnalytics } from "./Preferential/PreferentialAnalytics";
import { PreferentialGraph } from "./Preferential/PreferentialGraph";
import { PreferentialHistory } from "./Preferential/PreferentialHistory";
import { PreferentialTrials } from "./Preferential/PreferentialTrials";
import { StudyHistory } from "./StudyHistory";
import { TrialList } from "./TrialList";
import { TrialSelection } from "./TrialSelection";
export const useURLVars = () => {
    const { studyId } = useParams();
    if (studyId === undefined) {
        throw new Error("studyId is not defined");
    }
    return useMemo(() => parseInt(studyId, 10), [studyId]);
};
export const StudyDetail = ({ toggleColorMode, page }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const action = actionCreator();
    const studyId = useURLVars();
    const studyDetail = useStudyDetailValue(studyId);
    const reloadInterval = useRecoilValue(reloadIntervalState);
    const studyName = useStudyName(studyId);
    const isPreferential = useStudyIsPreferential(studyId);
    const study = studyDetailToStudy(studyDetail);
    const title = studyName !== null ? `${studyName} (id=${studyId})` : `Study #${studyId}`;
    useEffect(() => {
        action.updateStudyDetail(studyId);
        action.updateAPIMeta();
    }, []);
    useEffect(() => {
        if (reloadInterval < 0) {
            return;
        }
        const nTrials = studyDetail ? studyDetail.trials.length : 0;
        let interval = reloadInterval * 1000;
        // For Human-in-the-loop Optimization, the interval is set to 2 seconds
        // when the number of trials is small, and the page is "trialList" or top page of preferential.
        if ((!isPreferential && page === "trialList") ||
            (isPreferential && page === "top")) {
            if (nTrials < 100) {
                interval = 2000;
            }
            else if (nTrials < 500) {
                interval = 5000;
            }
        }
        const intervalId = setInterval(() => {
            action.updateStudyDetail(studyId);
        }, interval);
        return () => clearInterval(intervalId);
    }, [reloadInterval, studyDetail, page]);
    let content = null;
    if (page === "top") {
        content = isPreferential ? (React.createElement(PreferentialTrials, { studyDetail: studyDetail })) : (React.createElement(StudyHistory, { studyId: studyId }));
    }
    else if (page === "analytics") {
        content = isPreferential ? (React.createElement(PreferentialAnalytics, { studyId: studyId })) : (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%", flexDirection: "column" } },
            React.createElement(Typography, { variant: "h5", sx: {
                    margin: theme.spacing(2),
                    marginTop: theme.spacing(4),
                    fontWeight: theme.typography.fontWeightBold,
                } }, "Hyperparameter Relationships"),
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(GraphSlice, { study: studyDetail }))),
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(GraphParallelCoordinate, { study: studyDetail }))),
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(Contour, { study: studyDetail }))),
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(GraphRank, { study: studyDetail }))),
            React.createElement(Typography, { variant: "h5", sx: {
                    margin: theme.spacing(2),
                    marginTop: theme.spacing(4),
                    fontWeight: theme.typography.fontWeightBold,
                } }, "Empirical Distribution of the Objective Value"),
            React.createElement(Grid, { container: true, spacing: 2, sx: { padding: theme.spacing(2) } }, studyDetail !== null
                ? studyDetail.directions.map((d, i) => (React.createElement(Grid, { item: true, xs: 6, key: i },
                    React.createElement(Card, null,
                        React.createElement(CardContent, null,
                            React.createElement(GraphEdf, { studies: [studyDetail], objectiveId: i }))))))
                : null)));
    }
    else if (page === "trialList") {
        content = React.createElement(TrialList, { studyDetail: studyDetail });
    }
    else if (page === "trialSelection") {
        content = React.createElement(TrialSelection, { studyDetail: studyDetail });
    }
    else if (page === "trialTable" && study !== null) {
        const linkURL = (studyId, trialNumber) => {
            return url_prefix + `/studies/${studyId}/trials?numbers=${trialNumber}`;
        };
        content = (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%", flexDirection: "column" } },
            React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                React.createElement(CardContent, null,
                    React.createElement(TrialTable, { study: study, linkComponent: Link, linkURL: linkURL }),
                    React.createElement(Button, { variant: "outlined", startIcon: React.createElement(DownloadIcon, null), download: true, href: `/csv/${studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.id}`, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Download CSV File")))));
    }
    else if (page === "note" && studyDetail !== null) {
        content = (React.createElement(Box, { component: "div", sx: {
                height: `calc(100vh - ${theme.spacing(8)})`,
                display: "flex",
                flexDirection: "column",
                padding: theme.spacing(2),
            } },
            React.createElement(Typography, { variant: "h5", sx: {
                    fontWeight: theme.typography.fontWeightBold,
                    margin: theme.spacing(2, 0),
                } }, "Note"),
            React.createElement(StudyNote, { studyId: studyId, latestNote: studyDetail.note, cardSx: { flexGrow: 1 } })));
    }
    else if (page === "graph") {
        content = (React.createElement(Box, { component: "div", sx: {
                height: `calc(100vh - ${theme.spacing(8)})`,
                padding: theme.spacing(2),
            } },
            React.createElement(PreferentialGraph, { studyDetail: studyDetail })));
    }
    else if (page === "preferenceHistory") {
        content = React.createElement(PreferentialHistory, { studyDetail: studyDetail });
    }
    const toolbar = (React.createElement(React.Fragment, null,
        React.createElement(IconButton, { component: Link, to: url_prefix + "/", sx: { marginRight: theme.spacing(1) }, color: "inherit", title: "Return to the top page" },
            React.createElement(HomeIcon, null)),
        React.createElement(ChevronRightIcon, { sx: { marginRight: theme.spacing(1) } }),
        React.createElement(Typography, { noWrap: true, component: "div", sx: { fontWeight: theme.typography.fontWeightBold } }, title)));
    return (React.createElement(Box, { component: "div", sx: { display: "flex" } },
        React.createElement(AppDrawer, { studyId: studyId, page: page, toggleColorMode: toggleColorMode, toolbar: toolbar }, content)));
};
//# sourceMappingURL=StudyDetail.js.map