import { Box, CssBaseline, ThemeProvider, createTheme, useMediaQuery, } from "@mui/material";
import blue from "@mui/material/colors/blue";
import pink from "@mui/material/colors/pink";
import { SnackbarProvider } from "notistack";
import React, { useMemo, useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { RecoilRoot } from "recoil";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useConstants } from "../constantsProvider";
import { CompareStudies } from "./CompareStudies";
import { StudyDetail } from "./StudyDetail";
import { StudyList } from "./StudyList";
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: false,
            refetchOnMount: false,
            refetchOnReconnect: false,
            refetchOnWindowFocus: false,
        },
    },
});
export const App = () => {
    const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
    const [colorMode, setColorMode] = useState("light");
    useEffect(() => {
        setColorMode(prefersDarkMode ? "dark" : "light");
    }, [prefersDarkMode]);
    const theme = useMemo(() => createTheme({
        palette: {
            mode: colorMode,
            primary: blue,
            secondary: pink,
        },
    }), [colorMode]);
    const toggleColorMode = () => {
        setColorMode(colorMode === "dark" ? "light" : "dark");
    };
    const { url_prefix } = useConstants();
    return (React.createElement(QueryClientProvider, { client: queryClient },
        React.createElement(RecoilRoot, null,
            React.createElement(ThemeProvider, { theme: theme },
                React.createElement(CssBaseline, null),
                React.createElement(Box, { component: "div", sx: {
                        backgroundColor: colorMode === "dark" ? "#121212" : "#ffffff",
                        width: "100%",
                        minHeight: "100vh",
                    } },
                    React.createElement(SnackbarProvider, { maxSnack: 3 },
                        React.createElement(Router, null,
                            React.createElement(Routes, null,
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/analytics", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "analytics" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/trials", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "trialList" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/trialTable", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "trialTable" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/trialSelection", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "trialSelection" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/note", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "note" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/graph", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "graph" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "top" }) }),
                                React.createElement(Route, { path: url_prefix + "/studies/:studyId/preference-history", element: React.createElement(StudyDetail, { toggleColorMode: toggleColorMode, page: "preferenceHistory" }) }),
                                React.createElement(Route, { path: url_prefix + "/compare-studies", element: React.createElement(CompareStudies, { toggleColorMode: toggleColorMode }) }),
                                React.createElement(Route, { path: url_prefix + "/", element: React.createElement(StudyList, { toggleColorMode: toggleColorMode }) })))))))));
};
//# sourceMappingURL=App.js.map