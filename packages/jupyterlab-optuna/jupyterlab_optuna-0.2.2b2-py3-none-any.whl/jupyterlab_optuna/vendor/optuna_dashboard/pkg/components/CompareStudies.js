import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import HomeIcon from "@mui/icons-material/Home";
import { Box, Card, CardContent, FormControl, IconButton, Switch, Typography, useTheme, } from "@mui/material";
import Chip from "@mui/material/Chip";
import Divider from "@mui/material/Divider";
import FormControlLabel from "@mui/material/FormControlLabel";
import Grid from "@mui/material/Grid";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import { useSnackbar } from "notistack";
import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { useNavigate } from "react-router-dom";
import { actionCreator } from "../action";
import { useConstants } from "../constantsProvider";
import { studyDetailsState, studySummariesState } from "../state";
import { useQuery } from "../urlQuery";
import { AppDrawer } from "./AppDrawer";
import { GraphEdf } from "./GraphEdf";
import { GraphHistory } from "./GraphHistory";
const useQueriedStudies = (studies, query) => {
    return useMemo(() => {
        const queried = query.get("ids");
        if (queried === null) {
            return [];
        }
        const ids = queried
            .split(",")
            .map((s) => parseInt(s))
            .filter((n) => !isNaN(n));
        return studies.filter((t) => ids.findIndex((n) => n === t.study_id) !== -1);
    }, [studies, query]);
};
const getStudyListLink = (ids, url_prefix) => {
    const base = url_prefix + "/compare-studies";
    if (ids.length > 0) {
        return base + "?ids=" + ids.map((n) => n.toString()).join(",");
    }
    return base;
};
const isEqualDirections = (array1, array2) => {
    let i = array1.length;
    if (i !== array2.length)
        return false;
    while (i--) {
        if (array1[i] !== array2[i])
            return false;
    }
    return true;
};
export const CompareStudies = ({ toggleColorMode }) => {
    const { url_prefix } = useConstants();
    const { enqueueSnackbar } = useSnackbar();
    const theme = useTheme();
    const query = useQuery();
    const navigate = useNavigate();
    const action = actionCreator();
    const studies = useRecoilValue(studySummariesState);
    const queried = useQueriedStudies(studies, query);
    const selected = useMemo(() => {
        return queried.length > 0 ? queried : studies.length > 0 ? [studies[0]] : [];
    }, [studies, query]);
    const studyListWidth = 200;
    const title = "Compare Studies (Experimental)";
    useEffect(() => {
        action.updateStudySummaries();
    }, []);
    const toolbar = (React.createElement(React.Fragment, null,
        React.createElement(IconButton, { component: Link, to: url_prefix + "/", sx: { marginRight: theme.spacing(1) }, color: "inherit", title: "Return to the top page" },
            React.createElement(HomeIcon, null)),
        React.createElement(ChevronRightIcon, { sx: { marginRight: theme.spacing(1) } }),
        React.createElement(Typography, { noWrap: true, component: "div", sx: { fontWeight: theme.typography.fontWeightBold } }, title)));
    return (React.createElement(Box, { component: "div", sx: { display: "flex" } },
        React.createElement(AppDrawer, { toggleColorMode: toggleColorMode, toolbar: toolbar },
            React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", width: "100%" } },
                React.createElement(Box, { component: "div", sx: {
                        minWidth: studyListWidth,
                        overflow: "auto",
                        height: `calc(100vh - ${theme.spacing(8)})`,
                    } },
                    React.createElement(List, null,
                        React.createElement(ListSubheader, { sx: { display: "flex", flexDirection: "row" } },
                            React.createElement(Typography, { sx: { p: theme.spacing(1, 0) } }, "Compare studies with Shift+Click"),
                            React.createElement(Box, { component: "div", sx: { flexGrow: 1 } })),
                        React.createElement(Divider, null),
                        studies.map((study) => {
                            return (React.createElement(ListItem, { key: study.study_id, disablePadding: true },
                                React.createElement(ListItemButton, { onClick: (e) => {
                                        if (e.shiftKey) {
                                            let next;
                                            const selectedIds = selected.map((s) => s.study_id);
                                            const alreadySelected = selectedIds.findIndex((n) => n === study.study_id) >= 0;
                                            if (alreadySelected) {
                                                next = selectedIds.filter((n) => n !== study.study_id);
                                            }
                                            else {
                                                if (selected.length > 0 &&
                                                    selected[0].directions.length !==
                                                        study.directions.length) {
                                                    enqueueSnackbar("You can only compare studies that has the same number of objectives.", {
                                                        variant: "info",
                                                    });
                                                    next = selectedIds;
                                                }
                                                else if (selected.length > 0 &&
                                                    !isEqualDirections(selected[0].directions, study.directions)) {
                                                    enqueueSnackbar("You can only compare studies that has the same directions.", {
                                                        variant: "info",
                                                    });
                                                    next = selectedIds;
                                                }
                                                else {
                                                    next = [...selectedIds, study.study_id];
                                                }
                                            }
                                            navigate(getStudyListLink(next, url_prefix));
                                        }
                                        else {
                                            navigate(getStudyListLink([study.study_id], url_prefix));
                                        }
                                    }, selected: selected.findIndex((s) => s.study_id === study.study_id) !== -1, sx: {
                                        display: "flex",
                                        flexDirection: "column",
                                        alignItems: "flex-start",
                                    } },
                                    React.createElement(ListItemText, { primary: `${study.study_id}. ${study.study_name}` }),
                                    React.createElement(Box, { component: "div", sx: {
                                            display: "flex",
                                            flexDirection: "row",
                                            width: "100%",
                                        } },
                                        React.createElement(Chip, { color: "primary", label: study.directions.length === 1
                                                ? `${study.directions.length} objective`
                                                : `${study.directions.length} objectives`, size: "small", variant: "outlined" }),
                                        React.createElement("span", { style: { margin: theme.spacing(0.5) } }),
                                        React.createElement(Chip, { color: "secondary", label: study.directions
                                                .map((d) => (d === "maximize" ? "max" : "min"))
                                                .join(", "), size: "small", variant: "outlined" })))));
                        }))),
                React.createElement(Divider, { orientation: "vertical", flexItem: true }),
                React.createElement(Box, { component: "div", sx: {
                        flexGrow: 1,
                        overflow: "auto",
                        height: `calc(100vh - ${theme.spacing(8)})`,
                    } },
                    React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", width: "100%" } },
                        React.createElement(StudiesGraph, { studies: selected })))))));
};
const StudiesGraph = ({ studies }) => {
    const theme = useTheme();
    const action = actionCreator();
    const studyDetails = useRecoilValue(studyDetailsState);
    const [logScale, setLogScale] = useState(false);
    const [includePruned, setIncludePruned] = useState(true);
    const handleLogScaleChange = () => {
        setLogScale(!logScale);
    };
    const handleIncludePrunedChange = () => {
        setIncludePruned(!includePruned);
    };
    useEffect(() => {
        studies.forEach((study) => {
            action.updateStudyDetail(study.study_id);
        });
    }, [studies]);
    const showStudyDetails = studies.map((study) => studyDetails[study.study_id]);
    return (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%", flexDirection: "column" } },
        React.createElement(FormControl, { component: "fieldset", sx: {
                display: "flex",
                flexDirection: "row",
                justifyContent: "flex-end",
                padding: theme.spacing(2),
            } },
            React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: logScale, onChange: handleLogScaleChange, value: "enable" }), label: "Log y scale" }),
            React.createElement(FormControlLabel, { control: React.createElement(Switch, { checked: includePruned, onChange: handleIncludePrunedChange, value: "enable" }), label: "Include PRUNED trials" })),
        showStudyDetails !== null &&
            showStudyDetails.length > 0 &&
            showStudyDetails.every((s) => s) ? (React.createElement(Card, { sx: {
                margin: theme.spacing(2),
            } },
            React.createElement(CardContent, null,
                React.createElement(GraphHistory, { studies: showStudyDetails, includePruned: includePruned, logScale: logScale })))) : null,
        React.createElement(Grid, { container: true, spacing: 2, sx: { padding: theme.spacing(0, 2) } }, showStudyDetails !== null &&
            showStudyDetails.length > 0 &&
            showStudyDetails.every((s) => s)
            ? showStudyDetails[0].directions.map((d, i) => (React.createElement(Grid, { item: true, xs: 6, key: i },
                React.createElement(Card, null,
                    React.createElement(CardContent, null,
                        React.createElement(GraphEdf, { studies: showStudyDetails, objectiveId: i }))))))
            : null)));
};
//# sourceMappingURL=CompareStudies.js.map