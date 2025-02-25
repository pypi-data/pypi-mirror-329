import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import RateReviewIcon from "@mui/icons-material/RateReview";
import RuleIcon from "@mui/icons-material/Rule";
import SettingsIcon from "@mui/icons-material/Settings";
import SyncIcon from "@mui/icons-material/Sync";
import SyncDisabledIcon from "@mui/icons-material/SyncDisabled";
import TableViewIcon from "@mui/icons-material/TableView";
import ViewListIcon from "@mui/icons-material/ViewList";
import MuiAppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import MuiDrawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Modal from "@mui/material/Modal";
import Toolbar from "@mui/material/Toolbar";
import { styled, useTheme, } from "@mui/material/styles";
import React from "react";
import { Link } from "react-router-dom";
import { useRecoilState, useRecoilValue } from "recoil";
import { drawerOpenState, reloadIntervalState, useShowExperimentalFeature, useStudyIsPreferential, } from "../state";
import { Settings } from "./Settings";
import GitHubIcon from "@mui/icons-material/GitHub";
import HistoryIcon from "@mui/icons-material/History";
import LanIcon from "@mui/icons-material/Lan";
import MenuIcon from "@mui/icons-material/Menu";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import QueryStatsIcon from "@mui/icons-material/QueryStats";
import ThumbUpAltIcon from "@mui/icons-material/ThumbUpAlt";
import { Switch } from "@mui/material";
import { actionCreator } from "../action";
import { useConstants } from "../constantsProvider";
const drawerWidth = 240;
const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: "hidden",
});
const closedMixin = (theme) => ({
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up("sm")]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});
const DrawerHeader = styled("div")(({ theme }) => (Object.assign({ display: "flex", alignItems: "center", justifyContent: "flex-end", padding: theme.spacing(0, 1) }, theme.mixins.toolbar)));
const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => (Object.assign({ zIndex: theme.zIndex.drawer + 1, transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }) }, (open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
}))));
const Drawer = styled(MuiDrawer, {
    shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => (Object.assign(Object.assign({ width: drawerWidth, flexShrink: 0, whiteSpace: "nowrap", boxSizing: "border-box" }, (open && Object.assign(Object.assign({}, openedMixin(theme)), { "& .MuiDrawer-paper": openedMixin(theme) }))), (!open && Object.assign(Object.assign({}, closedMixin(theme)), { "& .MuiDrawer-paper": closedMixin(theme) })))));
export const AppDrawer = ({ studyId, toggleColorMode, page, toolbar, children }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const constants = useConstants();
    const action = actionCreator();
    const [open, setOpen] = useRecoilState(drawerOpenState);
    const reloadInterval = useRecoilValue(reloadIntervalState);
    const isPreferential = studyId !== undefined ? useStudyIsPreferential(studyId) : null;
    const [showExperimentalFeatures] = useShowExperimentalFeature();
    const styleListItem = {
        display: "block",
    };
    const styleListItemButton = {
        minHeight: 48,
        justifyContent: open ? "initial" : "center",
        px: 2.5,
    };
    const styleListItemIcon = {
        minWidth: 0,
        mr: open ? 3 : "auto",
        justifyContent: "center",
    };
    const styleListItemText = {
        opacity: open ? 1 : 0,
    };
    const styleSwitch = {
        display: open ? "inherit" : "none",
    };
    const mainSx = {
        flexGrow: 1,
    };
    if (constants.environment === "jupyterlab") {
        // 100vh - (the height of Optuna Dashboard toolbar) - (the height of JupyterLab toolbar)
        mainSx.height = `calc(100vh - ${theme.mixins.toolbar.minHeight}px - 29px)`;
        mainSx.overflow = "auto";
    }
    const handleDrawerOpen = () => {
        setOpen(true);
    };
    const handleDrawerClose = () => {
        setOpen(false);
    };
    const [settingOpen, setSettingOpen] = React.useState(false);
    const handleSettingOpen = () => {
        setSettingOpen(true);
    };
    const handleSettingClose = () => {
        setSettingOpen(false);
    };
    return (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%" } },
        React.createElement(AppBar, { position: "fixed", open: open },
            React.createElement(Toolbar, null,
                React.createElement(IconButton, { color: "inherit", "aria-label": "open drawer", onClick: handleDrawerOpen, edge: "start", sx: Object.assign({ marginRight: 5 }, (open && { display: "none" })) },
                    React.createElement(MenuIcon, null)),
                toolbar)),
        React.createElement(Drawer, { variant: "permanent", open: open },
            React.createElement(DrawerHeader, null,
                React.createElement(IconButton, { onClick: handleDrawerClose }, theme.direction === "rtl" ? (React.createElement(ChevronRightIcon, null)) : (React.createElement(ChevronLeftIcon, null)))),
            React.createElement(Divider, null),
            studyId !== undefined && page && (React.createElement(List, null,
                React.createElement(ListItem, { key: "Top", disablePadding: true, sx: styleListItem, title: isPreferential ? "Feedback Preference" : "History" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}`, sx: styleListItemButton, selected: page === "top" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon }, isPreferential ? React.createElement(ThumbUpAltIcon, null) : React.createElement(AutoGraphIcon, null)),
                        React.createElement(ListItemText, { primary: isPreferential ? "Feedback Preference" : "History", sx: styleListItemText }))),
                isPreferential && (React.createElement(ListItem, { key: "PreferenceHistory", disablePadding: true, sx: styleListItem, title: "Preference (History)" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/preference-history`, sx: styleListItemButton, selected: page === "preferenceHistory" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(HistoryIcon, null)),
                        React.createElement(ListItemText, { primary: "Preferences (History)", sx: styleListItemText })))),
                React.createElement(ListItem, { key: "Analytics", disablePadding: true, sx: styleListItem, title: "Analytics" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/analytics`, sx: styleListItemButton, selected: page === "analytics" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(QueryStatsIcon, null)),
                        React.createElement(ListItemText, { primary: "Analytics", sx: styleListItemText }))),
                isPreferential && (React.createElement(ListItem, { key: "PreferenceGraph", disablePadding: true, sx: styleListItem, title: "Preference (Graph)" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/graph`, sx: styleListItemButton, selected: page === "graph" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(LanIcon, null)),
                        React.createElement(ListItemText, { primary: "Preferences (Graph)", sx: styleListItemText })))),
                React.createElement(ListItem, { key: "TableList", disablePadding: true, sx: styleListItem, title: "Trials (List)" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/trials`, sx: styleListItemButton, selected: page === "trialList" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(ViewListIcon, null)),
                        React.createElement(ListItemText, { primary: "Trials (List)", sx: styleListItemText }))),
                React.createElement(ListItem, { key: "TrialTable", disablePadding: true, sx: styleListItem, title: "Trials (Table)" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/trialTable`, sx: styleListItemButton, selected: page === "trialTable" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(TableViewIcon, null)),
                        React.createElement(ListItemText, { primary: "Trials (Table)", sx: styleListItemText }))),
                showExperimentalFeatures && (React.createElement(ListItem, { key: "TrialSelection", disablePadding: true, sx: styleListItem, title: "Trials (Selection)" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/trialSelection`, sx: styleListItemButton, selected: page === "trialSelection" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(RuleIcon, null)),
                        React.createElement(ListItemText, { primary: "Trials (Selection)", sx: styleListItemText })))),
                React.createElement(ListItem, { key: "Note", disablePadding: true, sx: styleListItem, title: "Note" },
                    React.createElement(ListItemButton, { component: Link, to: `${url_prefix}/studies/${studyId}/note`, sx: styleListItemButton, selected: page === "note" },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(RateReviewIcon, null)),
                        React.createElement(ListItemText, { primary: "Note", sx: styleListItemText }))))),
            React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
            React.createElement(Divider, null),
            React.createElement(List, null,
                studyId !== undefined && (React.createElement(ListItem, { key: "LiveUpdate", disablePadding: true, sx: styleListItem, title: "Live Update" },
                    React.createElement(ListItemButton, { sx: styleListItemButton, onClick: () => {
                            action.saveReloadInterval(reloadInterval === -1 ? 10 : -1);
                        } },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon }, reloadInterval === -1 ? React.createElement(SyncDisabledIcon, null) : React.createElement(SyncIcon, null)),
                        React.createElement(ListItemText, { primary: "Live Update", sx: styleListItemText }),
                        React.createElement(Switch, { edge: "end", checked: reloadInterval !== -1, sx: styleSwitch, inputProps: {
                                "aria-labelledby": "switch-list-label-live-update",
                            } })))),
                React.createElement(ListItem, { key: "Settings", disablePadding: true, sx: styleListItem, title: "Settings" },
                    React.createElement(ListItemButton, { sx: styleListItemButton, onClick: handleSettingOpen },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(SettingsIcon, null)),
                        React.createElement(ListItemText, { primary: "Settings", sx: styleListItemText })),
                    React.createElement(Modal, { open: settingOpen, onClose: handleSettingClose, "aria-labelledby": "modal-modal-title", "aria-describedby": "modal-modal-description" },
                        React.createElement(Box, { component: "div", sx: {
                                position: "absolute",
                                top: "50%",
                                left: "50%",
                                transform: "translate(-50%, -50%)",
                                overflow: "scroll",
                                width: "600px",
                                height: "600px",
                                bgcolor: "background.paper",
                            } },
                            React.createElement(Settings, { handleClose: handleSettingClose })))),
                React.createElement(ListItem, { key: "DarkMode", disablePadding: true, sx: styleListItem, title: "Dark Mode" },
                    React.createElement(ListItemButton, { sx: styleListItemButton, onClick: () => {
                            toggleColorMode();
                        } },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon }, theme.palette.mode === "dark" ? (React.createElement(Brightness4Icon, null)) : (React.createElement(Brightness7Icon, null))),
                        React.createElement(ListItemText, { primary: "Dark Mode", sx: styleListItemText }),
                        React.createElement(Switch, { edge: "end", checked: theme.palette.mode === "dark", sx: styleSwitch, inputProps: {
                                "aria-labelledby": "switch-list-label-dark-mode",
                            } }))),
                React.createElement(Divider, null),
                React.createElement(ListItem, { key: "Feedback", disablePadding: true, sx: styleListItem, title: "Send Feedback" },
                    React.createElement(ListItemButton, { target: "_blank", href: "https://github.com/optuna/optuna-dashboard/discussions/new/choose", sx: styleListItemButton },
                        React.createElement(ListItemIcon, { sx: styleListItemIcon },
                            React.createElement(GitHubIcon, null)),
                        React.createElement(ListItemText, { primary: "Send Feedback", sx: styleListItemText }),
                        React.createElement(OpenInNewIcon, { sx: styleSwitch }))))),
        React.createElement(Box, { component: "main", sx: mainSx },
            React.createElement(DrawerHeader, null),
            children || null)));
};
//# sourceMappingURL=AppDrawer.js.map