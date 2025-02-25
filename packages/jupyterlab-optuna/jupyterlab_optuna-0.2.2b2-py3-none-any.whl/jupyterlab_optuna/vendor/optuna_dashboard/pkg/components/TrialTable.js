import DownloadIcon from "@mui/icons-material/Download";
import LinkIcon from "@mui/icons-material/Link";
import { Button, IconButton, useTheme } from "@mui/material";
import React from "react";
import { DataGrid } from "@optuna/react";
import { Link } from "react-router-dom";
import { createColumnHelper, } from "@tanstack/react-table";
import { useConstants } from "../constantsProvider";
const multiValueFilter = (row, columnId, filterValue) => {
    const rowValue = row.getValue(columnId);
    return !filterValue.includes(rowValue);
};
export const TrialTable = ({ studyDetail }) => {
    const { url_prefix } = useConstants();
    const theme = useTheme();
    const trials = studyDetail !== null ? studyDetail.trials : [];
    const objectiveNames = (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.objective_names) || [];
    const columnHelper = createColumnHelper();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const columns = [
        columnHelper.accessor("number", {
            header: "Number",
            enableColumnFilter: false,
        }),
        columnHelper.accessor("state", {
            header: "State",
            enableSorting: false,
            enableColumnFilter: true,
            filterFn: multiValueFilter,
        }),
    ];
    if (studyDetail === null || studyDetail.directions.length === 1) {
        columns.push(columnHelper.accessor("values", {
            header: "Value",
            enableSorting: true,
            enableColumnFilter: false,
            sortUndefined: "last",
        }));
    }
    else {
        columns.push(...studyDetail.directions.map((s, objectiveId) => columnHelper.accessor((row) => { var _a; return (_a = row["values"]) === null || _a === void 0 ? void 0 : _a[objectiveId]; }, {
            id: `values_${objectiveId}`,
            header: objectiveNames.length === (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.directions.length)
                ? objectiveNames[objectiveId]
                : `Objective ${objectiveId}`,
            enableSorting: true,
            enableColumnFilter: false,
            sortUndefined: "last",
        })));
    }
    const isDynamicSpace = (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.union_search_space.length) !==
        (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.intersection_search_space.length);
    studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.union_search_space.forEach((s) => {
        const sortable = s.distribution.type !== "CategoricalDistribution";
        const filterChoices = s.distribution.type === "CategoricalDistribution"
            ? s.distribution.choices.map((c) => { var _a; return (_a = c === null || c === void 0 ? void 0 : c.toString()) !== null && _a !== void 0 ? _a : "null"; })
            : undefined;
        const hasMissingValue = trials.some((t) => !t.params.some((p) => p.name === s.name));
        if (filterChoices !== undefined && isDynamicSpace && hasMissingValue) {
            filterChoices.push(null);
        }
        columns.push(columnHelper.accessor((row) => {
            var _a;
            return ((_a = row["params"].find((p) => p.name === s.name)) === null || _a === void 0 ? void 0 : _a.param_external_value) ||
                null;
        }, {
            id: `params_${s.name}`,
            header: `Param ${s.name}`,
            enableSorting: sortable,
            sortUndefined: "last",
            enableColumnFilter: filterChoices !== undefined,
            filterFn: multiValueFilter,
        }));
    });
    studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.union_user_attrs.forEach((attr_spec) => {
        columns.push(columnHelper.accessor((row) => { var _a; return ((_a = row["user_attrs"].find((a) => a.key === attr_spec.key)) === null || _a === void 0 ? void 0 : _a.value) || null; }, {
            id: `user_attrs_${attr_spec.key}`,
            header: `UserAttribute ${attr_spec.key}`,
            enableSorting: attr_spec.sortable,
            enableColumnFilter: false,
            sortUndefined: "last",
        }));
    });
    columns.push(columnHelper.accessor((row) => row, {
        header: "Detail",
        cell: (info) => (React.createElement(IconButton, { component: Link, to: url_prefix +
                `/studies/${info.getValue().study_id}/trials?numbers=${info.getValue().number}`, color: "inherit", title: "Go to the trial's detail page", size: "small" },
            React.createElement(LinkIcon, null))),
        enableSorting: false,
        enableColumnFilter: false,
    }));
    return (React.createElement(React.Fragment, null,
        React.createElement(DataGrid, { data: trials, columns: columns }),
        React.createElement(Button, { variant: "outlined", startIcon: React.createElement(DownloadIcon, null), download: true, href: `/csv/${studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.id}`, sx: { marginRight: theme.spacing(2), minWidth: "120px" } }, "Download CSV File")));
};
//# sourceMappingURL=TrialTable.js.map