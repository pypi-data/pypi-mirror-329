import { AxiosError } from "axios";
import { ParamImportance } from "ts/types/optuna";
export declare const useParamImportance: ({ numCompletedTrials, studyId, }: {
    numCompletedTrials: number;
    studyId: number;
}) => {
    importances: ParamImportance[][] | undefined;
    isLoading: boolean;
    error: AxiosError<{
        reason: string;
    }, any> | null;
};
