import { useQuery } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useAPIClient } from "../apiClientProvider";
export const useParamImportance = ({ numCompletedTrials, studyId, }) => {
    const { apiClient } = useAPIClient();
    const { enqueueSnackbar } = useSnackbar();
    const { data, isLoading, error } = useQuery({
        queryKey: ["paramImportance", studyId, numCompletedTrials],
        queryFn: () => apiClient.getParamImportances(studyId),
        staleTime: Infinity,
        gcTime: 30 * 60 * 1000, // 30 minutes
    });
    useEffect(() => {
        var _a;
        if (error) {
            const reason = (_a = error.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to load hyperparameter importance (reason=${reason})`, {
                variant: "error",
            });
        }
    }, [error]);
    return {
        importances: data,
        isLoading,
        error,
    };
};
//# sourceMappingURL=useParamImportance.js.map