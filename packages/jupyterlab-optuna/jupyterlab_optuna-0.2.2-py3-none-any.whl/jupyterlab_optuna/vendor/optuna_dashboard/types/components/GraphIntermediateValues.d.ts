import { FC } from "react";
import { Trial } from "ts/types/optuna";
export declare const GraphIntermediateValues: FC<{
    trials: Trial[];
    includePruned: boolean;
    logScale: boolean;
}>;
