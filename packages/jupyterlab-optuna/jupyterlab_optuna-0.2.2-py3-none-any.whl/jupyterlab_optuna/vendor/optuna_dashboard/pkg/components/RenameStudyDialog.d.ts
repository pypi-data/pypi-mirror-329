import { ReactNode } from "react";
import { StudySummary } from "ts/types/optuna";
export declare const useRenameStudyDialog: (studies: StudySummary[]) => [(studyId: number, studyName: string) => void, () => ReactNode];
