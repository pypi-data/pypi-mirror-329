import ClearIcon from "@mui/icons-material/Clear";
import { Box, IconButton, Link, MenuItem, Select, Stack, Switch, Typography, useTheme, } from "@mui/material";
import React from "react";
import { useRecoilValue } from "recoil";
import { plotlypyIsAvailableState, usePlotBackendRendering, usePlotlyColorThemeState, useShowExperimentalFeature, } from "../state";
export const Settings = ({ handleClose }) => {
    const theme = useTheme();
    const [plotlyColorTheme, setPlotlyColorTheme] = usePlotlyColorThemeState();
    const [plotBackendRendering, setPlotBackendRendering] = usePlotBackendRendering();
    const plotlypyIsAvailable = useRecoilValue(plotlypyIsAvailableState);
    const [showExperimentalFeature, setShowExperimentalFeature] = useShowExperimentalFeature();
    const handleDarkModeColorChange = (event) => {
        const dark = event.target.value;
        setPlotlyColorTheme((cur) => (Object.assign(Object.assign({}, cur), { dark })));
    };
    const handleLightModeColorChange = (event) => {
        const light = event.target.value;
        setPlotlyColorTheme((cur) => (Object.assign(Object.assign({}, cur), { light })));
    };
    const togglePlotBackendRendering = () => {
        setPlotBackendRendering((cur) => !cur);
    };
    const toggleShowExperimentalFeature = () => {
        setShowExperimentalFeature((cur) => !cur);
    };
    return (React.createElement(Box, { component: "div", sx: { position: "relative" } },
        React.createElement(Stack, { spacing: 4, sx: {
                p: "2rem",
            } },
            React.createElement(Typography, { variant: "h4", sx: { fontWeight: theme.typography.fontWeightBold } }, "Settings"),
            React.createElement(Stack, { spacing: 2 },
                React.createElement(Typography, { variant: "h5", sx: { fontWeight: theme.typography.fontWeightBold } }, "Plotly Color Scales"),
                theme.palette.mode === "dark" ? (React.createElement(React.Fragment, null,
                    React.createElement(Typography, { variant: "h6" }, "Dark Mode"),
                    React.createElement(Typography, { color: "textSecondary" }, "Only the \"Default\" color scale is supported in dark mode"),
                    React.createElement(Select, { disabled: true, value: plotlyColorTheme.dark, onChange: handleDarkModeColorChange }, [{ value: "default", label: "Default" }].map((v) => (React.createElement(MenuItem, { key: v.value, value: v.value }, v.label)))))) : (React.createElement(React.Fragment, null,
                    React.createElement(Typography, { variant: "h6" }, "Light Mode"),
                    React.createElement(Select, { value: plotlyColorTheme.light, onChange: handleLightModeColorChange }, [
                        { value: "default", label: "Default" },
                        { value: "seaborn", label: "Seaborn" },
                        { value: "presentation", label: "Presentation" },
                        { value: "ggplot2", label: "GGPlot2" },
                    ].map((v) => (React.createElement(MenuItem, { key: v.value, value: v.value }, v.label))))))),
            React.createElement(Stack, null,
                React.createElement(Typography, { variant: "h5", sx: { fontWeight: theme.typography.fontWeightBold } }, "Use Plotly Python library"),
                React.createElement(Typography, { color: "textSecondary" },
                    "If enabled, the plots will be rendered using the ",
                    React.createElement(Link, { href: "https://optuna.readthedocs.io/en/stable/reference/visualization/index.html" }, "optuna.visualization module"),
                    "."),
                React.createElement(Switch, { checked: plotBackendRendering, onChange: togglePlotBackendRendering, value: "enable", disabled: !plotlypyIsAvailable })),
            React.createElement(Stack, null,
                React.createElement(Typography, { variant: "h5", sx: { fontWeight: theme.typography.fontWeightBold } }, "Show Experimental Feature"),
                React.createElement(Typography, { color: "textSecondary" }, 'If enabled, show experimental features "Trial (Selection)" in the UI.'),
                React.createElement(Switch, { checked: showExperimentalFeature, onChange: toggleShowExperimentalFeature, value: "enable" }))),
        React.createElement(IconButton, { sx: {
                position: "absolute",
                top: "1rem",
                right: "1rem",
                width: "2rem",
                height: "2rem",
            }, onClick: handleClose },
            React.createElement(ClearIcon, null))));
};
//# sourceMappingURL=Settings.js.map