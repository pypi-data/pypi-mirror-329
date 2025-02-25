import { Box } from "@mui/material";
import * as plotly from "plotly.js-dist-min";
import React, { useEffect } from "react";
export const UserDefinedPlot = ({ graphObject }) => {
    const plotDomId = `user-defined-plot:${graphObject.id}`;
    useEffect(() => {
        try {
            const parsed = JSON.parse(graphObject.graph_object);
            plotly.react(plotDomId, parsed.data, parsed.layout);
        }
        catch (e) {
            // Avoid to crash the whole page when given invalid grpah objects.
            console.error(e);
        }
    }, [graphObject]);
    return React.createElement(Box, { component: "div", id: plotDomId, sx: { height: "450px" } });
};
//# sourceMappingURL=UserDefinedPlot.js.map