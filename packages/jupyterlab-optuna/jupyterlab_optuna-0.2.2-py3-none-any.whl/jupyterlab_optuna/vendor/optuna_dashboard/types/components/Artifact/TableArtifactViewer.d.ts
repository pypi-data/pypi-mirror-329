import React, { ReactNode } from "react";
import { Artifact } from "ts/types/optuna";
export declare const isTableArtifact: (artifact: Artifact) => boolean;
interface TableArtifactViewerProps {
    src: string;
    filetype: string | undefined;
}
export declare const TableArtifactViewer: React.FC<TableArtifactViewerProps>;
export declare const useTableArtifactModal: () => [(path: string, artifact: Artifact) => void, () => ReactNode];
export {};
