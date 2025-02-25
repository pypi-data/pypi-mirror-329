import { SearchSpaceItem, Trial } from "./types/optuna";
export type AxisInfo = {
    name: string;
    isLog: boolean;
    isCat: boolean;
    indices: (string | number)[];
    values: (string | number | null)[];
};
export declare const getAxisInfo: (trials: Trial[], param: SearchSpaceItem) => AxisInfo;
export declare const makeHovertext: (trial: Trial) => string;
