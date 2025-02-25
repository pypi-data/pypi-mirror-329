import { Delete, HourglassTop, Refresh, Search } from "@mui/icons-material";
import AddBoxIcon from "@mui/icons-material/AddBox";
import CompareIcon from "@mui/icons-material/Compare";
import DriveFileRenameOutlineIcon from "@mui/icons-material/DriveFileRenameOutline";
import HomeIcon from "@mui/icons-material/Home";
import SortIcon from "@mui/icons-material/Sort";
import { Box, Button, Card, CardActionArea, CardActions, CardContent, Container, IconButton, InputAdornment, MenuItem, SvgIcon, TextField, Typography, useTheme, } from "@mui/material";
import React, { useEffect, useState, useDeferredValue, useMemo, } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { styled } from "@mui/system";
import { actionCreator } from "../action";
import { useConstants } from "../constantsProvider";
import { studySummariesLoadingState, studySummariesState } from "../state";
import { useQuery } from "../urlQuery";
import { AppDrawer } from "./AppDrawer";
import { useCreateStudyDialog } from "./CreateStudyDialog";
import { useDeleteStudyDialog } from "./DeleteStudyDialog";
import { useRenameStudyDialog } from "./RenameStudyDialog";
export const StudyList = ({ toggleColorMode }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const action = actionCreator();
    const [_studyFilterText, setStudyFilterText] = React.useState("");
    const studyFilterText = useDeferredValue(_studyFilterText);
    const studyFilter = (row) => {
        const keywords = studyFilterText.split(" ");
        return !keywords.every((k) => {
            if (k === "") {
                return true;
            }
            return row.study_name.indexOf(k) >= 0;
        });
    };
    const studies = useRecoilValue(studySummariesState);
    const [openCreateStudyDialog, renderCreateStudyDialog] = useCreateStudyDialog();
    const [openDeleteStudyDialog, renderDeleteStudyDialog] = useDeleteStudyDialog();
    const [openRenameStudyDialog, renderRenameStudyDialog] = useRenameStudyDialog(studies);
    const isLoading = useRecoilValue(studySummariesLoadingState);
    const navigate = useNavigate();
    const query = useQuery();
    const initialSortBy = query.get("studies_order_by") === "asc" ? "asc" : "desc";
    const [sortBy, setSortBy] = useState(initialSortBy);
    const filteredStudies = useMemo(() => {
        let filteredStudies = studies.filter((s) => !studyFilter(s));
        if (sortBy === "desc") {
            filteredStudies = filteredStudies.reverse();
        }
        return filteredStudies;
    }, [studyFilterText, studies, sortBy]);
    useEffect(() => {
        action.updateStudySummaries();
    }, []);
    useEffect(() => {
        query.set("studies_order_by", sortBy);
        navigate(`${location.pathname}?${query.toString()}`, {
            replace: true,
        });
    }, [sortBy]);
    const Select = styled(TextField)(({ theme }) => ({
        "& .MuiInputBase-input": {
            // vertical padding + font size from searchIcon
            paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        },
    }));
    const sortBySelect = (React.createElement(Box, { component: "div", sx: {
            position: "relative",
            borderRadius: theme.shape.borderRadius,
            margin: theme.spacing(0, 2),
        } },
        React.createElement(Box, { component: "div", sx: {
                padding: theme.spacing(0, 2),
                height: "100%",
                position: "absolute",
                pointerEvents: "none",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            } },
            React.createElement(SortIcon, null)),
        React.createElement(Select, { select: true, value: sortBy, onChange: (e) => {
                setSortBy(e.target.value);
            } },
            React.createElement(MenuItem, { value: "asc" }, "Sort ascending"),
            React.createElement(MenuItem, { value: "desc" }, "Sort descending"))));
    const toolbar = React.createElement(HomeIcon, { sx: { margin: theme.spacing(0, 1) } });
    let studyListContent;
    if (isLoading) {
        studyListContent = (React.createElement(Box, { component: "div", sx: { margin: theme.spacing(2) } },
            React.createElement(SvgIcon, { fontSize: "small", color: "action" },
                React.createElement(HourglassTop, null)),
            "Loading studies..."));
    }
    else {
        studyListContent = filteredStudies.map((study) => (React.createElement(Card, { key: study.study_id, sx: { margin: theme.spacing(2), width: "500px" } },
            React.createElement(CardActionArea, { component: Link, to: `${url_prefix}/studies/${study.study_id}` },
                React.createElement(CardContent, null,
                    React.createElement(Typography, { variant: "h5", sx: { wordBreak: "break-all" } },
                        study.study_id,
                        ". ",
                        study.study_name),
                    React.createElement(Typography, { variant: "subtitle1", color: "text.secondary", component: "div" }, study.is_preferential
                        ? "Preferential Optimization"
                        : "Direction: " +
                            study.directions
                                .map((d) => d.toString().toUpperCase())
                                .join(", ")))),
            React.createElement(CardActions, { disableSpacing: true, sx: { paddingTop: 0 } },
                React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
                React.createElement(IconButton, { "aria-label": "rename study", size: "small", color: "inherit", onClick: () => {
                        openRenameStudyDialog(study.study_id, study.study_name);
                    } },
                    React.createElement(DriveFileRenameOutlineIcon, null)),
                React.createElement(IconButton, { "aria-label": "delete study", size: "small", color: "inherit", onClick: () => {
                        openDeleteStudyDialog(study.study_id);
                    } },
                    React.createElement(Delete, null))))));
    }
    return (React.createElement(Box, { component: "div", sx: { display: "flex" } },
        React.createElement(AppDrawer, { toggleColorMode: toggleColorMode, toolbar: toolbar },
            React.createElement(Container, { sx: {
                    ["@media (min-width: 1280px)"]: {
                        maxWidth: "100%",
                    },
                } },
                React.createElement(Card, { sx: { margin: theme.spacing(2) } },
                    React.createElement(CardContent, null,
                        React.createElement(Box, { component: "div", sx: { display: "flex" } },
                            React.createElement(TextField, { onChange: (e) => {
                                    setStudyFilterText(e.target.value);
                                }, id: "search-study", variant: "outlined", placeholder: "Search study", fullWidth: true, sx: { maxWidth: 500 }, InputProps: {
                                    startAdornment: (React.createElement(InputAdornment, { position: "start" },
                                        React.createElement(SvgIcon, { fontSize: "small", color: "action" },
                                            React.createElement(Search, null)))),
                                } }),
                            sortBySelect,
                            React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
                            React.createElement(Button, { variant: "outlined", startIcon: React.createElement(Refresh, null), onClick: () => {
                                    action.updateStudySummaries("Success to reload");
                                }, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Reload"),
                            React.createElement(Button, { variant: "outlined", startIcon: React.createElement(AddBoxIcon, null), onClick: () => {
                                    openCreateStudyDialog();
                                }, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Create"),
                            React.createElement(Button, { variant: "outlined", startIcon: React.createElement(CompareIcon, null), component: Link, to: `${url_prefix}/compare-studies`, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Compare")))),
                React.createElement(Box, { component: "div", sx: { display: "flex", flexWrap: "wrap" } }, studyListContent))),
        renderCreateStudyDialog(),
        renderDeleteStudyDialog(),
        renderRenameStudyDialog()));
};
//# sourceMappingURL=StudyList.js.map