import React, { ReactNode } from "react";
import { Artifact } from "ts/types/optuna";
export declare const isThreejsArtifact: (artifact: Artifact) => boolean;
interface ThreejsArtifactViewerProps {
    src: string;
    width: string;
    height: string;
    hasGizmo: boolean;
    filetype: string | undefined;
}
export declare const ThreejsArtifactViewer: React.FC<ThreejsArtifactViewerProps>;
export declare const useThreejsArtifactModal: () => [(path: string, artifact: Artifact) => void, () => ReactNode];
export {};
