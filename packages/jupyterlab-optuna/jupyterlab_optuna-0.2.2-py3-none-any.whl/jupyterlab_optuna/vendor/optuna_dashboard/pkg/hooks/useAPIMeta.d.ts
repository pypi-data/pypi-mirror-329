import { AxiosError } from "axios";
import { APIMeta } from "../apiClient";
export declare const useAPIMeta: () => {
    apiMeta: APIMeta | undefined;
    isLoading: boolean;
    error: AxiosError<{
        reason: string;
    }, any> | null;
};
