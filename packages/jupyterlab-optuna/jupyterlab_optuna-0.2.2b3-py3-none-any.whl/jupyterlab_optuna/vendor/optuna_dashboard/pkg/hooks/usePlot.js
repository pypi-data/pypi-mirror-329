import { useTheme } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { useAPIClient } from "../apiClientProvider";
import { usePlotlyColorTheme } from "../state";
export const usePlot = ({ numCompletedTrials, studyId, plotType, }) => {
    const theme = useTheme();
    const colorTheme = usePlotlyColorTheme(theme.palette.mode);
    const { apiClient } = useAPIClient();
    const { data, isLoading, error } = useQuery({
        enabled: studyId !== undefined,
        queryKey: ["plot", studyId, numCompletedTrials, plotType],
        queryFn: () => {
            if (studyId === undefined) {
                return Promise.reject(new Error("Invalid studyId"));
            }
            return apiClient.getPlot(studyId, plotType);
        },
        staleTime: Infinity,
        gcTime: 30 * 60 * 1000, // 30 minutes
    });
    return {
        data: data === null || data === void 0 ? void 0 : data.data,
        layout: Object.assign(Object.assign({}, data === null || data === void 0 ? void 0 : data.layout), { template: colorTheme }),
        isLoading,
        error,
    };
};
//# sourceMappingURL=usePlot.js.map