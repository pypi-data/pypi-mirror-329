import { Box, Card, CardContent, Paper, Typography, useTheme, } from "@mui/material";
import Grid from "@mui/material/Grid";
import { DataGrid } from "@optuna/react";
import React from "react";
import { useStudyDetailValue, useStudySummaryValue } from "../../state";
import { BestTrialsCard } from "../BestTrialsCard";
import { Contour } from "../GraphContour";
import { createColumnHelper } from "@tanstack/react-table";
export const PreferentialAnalytics = ({ studyId }) => {
    const theme = useTheme();
    const studySummary = useStudySummaryValue(studyId);
    const studyDetail = useStudyDetailValue(studyId);
    const userAttrs = (studySummary === null || studySummary === void 0 ? void 0 : studySummary.user_attrs) || (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.user_attrs) || [];
    const columnHelper = createColumnHelper();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const columns = [
        columnHelper.accessor("key", {
            header: "Key",
            enableSorting: true,
            enableColumnFilter: false,
        }),
        columnHelper.accessor("value", {
            header: "Value",
            enableSorting: true,
            enableColumnFilter: false,
        }),
    ];
    return (React.createElement(Box, { component: "div", sx: { display: "flex", width: "100%", flexDirection: "column" } },
        React.createElement(Grid, { container: true, spacing: 2, sx: { padding: theme.spacing(0, 2) } },
            React.createElement(Grid, { item: true, xs: 14 },
                React.createElement(Paper, { elevation: 2, sx: { padding: theme.spacing(2) } },
                    React.createElement(Contour, { study: studyDetail }))),
            React.createElement(Grid, { item: true, xs: 6, spacing: 2 },
                React.createElement(BestTrialsCard, { studyDetail: studyDetail })),
            React.createElement(Grid, { item: true, xs: 6 },
                React.createElement(Card, null,
                    React.createElement(CardContent, { sx: {
                            display: "flex",
                            flexDirection: "column",
                        } },
                        React.createElement(Typography, { variant: "h6", sx: {
                                margin: "1em 0",
                                fontWeight: theme.typography.fontWeightBold,
                            } }, "Study User Attributes"),
                        React.createElement(DataGrid, { data: userAttrs, columns: columns })))))));
};
//# sourceMappingURL=PreferentialAnalytics.js.map