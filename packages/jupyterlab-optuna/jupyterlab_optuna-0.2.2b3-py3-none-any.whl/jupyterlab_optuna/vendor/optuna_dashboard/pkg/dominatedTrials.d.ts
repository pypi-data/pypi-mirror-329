import * as Optuna from "@optuna/types";
import { Trial } from "./types/optuna";
export declare const getDominatedTrials: (trials: Trial[], directions: Optuna.StudyDirection[]) => Trial[];
