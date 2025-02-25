import * as Optuna from "@optuna/types";
import { SearchSpaceItem, StudyDetail } from "./types/optuna";
export type AxisInfo = {
    name: string;
    isLog: boolean;
    isCat: boolean;
    indices: (string | number)[];
    values: (string | number | null)[];
};
export declare const getAxisInfo: (trials: Optuna.Trial[], param: SearchSpaceItem) => AxisInfo;
export declare const makeHovertext: (trial: Optuna.Trial) => string;
export declare const studyDetailToStudy: (studyDetail: StudyDetail | null) => Optuna.Study | null;
