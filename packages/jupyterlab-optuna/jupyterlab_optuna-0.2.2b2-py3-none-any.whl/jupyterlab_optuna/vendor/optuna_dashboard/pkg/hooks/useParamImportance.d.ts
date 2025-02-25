import * as Optuna from "@optuna/types";
import { AxiosError } from "axios";
export declare const useParamImportance: ({ numCompletedTrials, studyId, }: {
    numCompletedTrials: number;
    studyId: number;
}) => {
    importances: Optuna.ParamImportance[][] | undefined;
    isLoading: boolean;
    error: AxiosError<{
        reason: string;
    }, any> | null;
};
