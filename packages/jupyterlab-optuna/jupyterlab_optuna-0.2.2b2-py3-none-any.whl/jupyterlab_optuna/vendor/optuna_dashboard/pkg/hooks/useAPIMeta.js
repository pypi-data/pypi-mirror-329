import { useQuery } from "@tanstack/react-query";
import { useAPIClient } from "../apiClientProvider";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
export const useAPIMeta = () => {
    const { apiClient } = useAPIClient();
    const { enqueueSnackbar } = useSnackbar();
    const { data, isLoading, error } = useQuery({
        queryKey: ["apiMeta"],
        queryFn: () => apiClient.getMetaInfo(),
        staleTime: Infinity,
        gcTime: 30 * 60 * 1000, // 30 minutes
    });
    useEffect(() => {
        var _a;
        if (error) {
            const reason = (_a = error.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to load API meta (reason=${reason})`, {
                variant: "error",
            });
        }
    }, [error]);
    return {
        apiMeta: data,
        isLoading,
        error,
    };
};
//# sourceMappingURL=useAPIMeta.js.map