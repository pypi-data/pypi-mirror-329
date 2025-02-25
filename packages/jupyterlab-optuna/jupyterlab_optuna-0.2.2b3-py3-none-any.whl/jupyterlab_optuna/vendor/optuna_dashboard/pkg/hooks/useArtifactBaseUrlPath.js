import { useQuery } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useAPIClient } from "../apiClientProvider";
export const useArtifactBaseUrlPath = () => {
    var _a, _b;
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
    if (isLoading || error !== null) {
        return "";
    }
    return (_b = (_a = data === null || data === void 0 ? void 0 : data.jupyterlab_extension_context) === null || _a === void 0 ? void 0 : _a.base_url) !== null && _b !== void 0 ? _b : "";
};
//# sourceMappingURL=useArtifactBaseUrlPath.js.map