import React, { useMemo } from "react";
import { ArtifactCardMedia } from "../Artifact/ArtifactCardMedia";
import { MarkdownRenderer } from "../Note";
export const PreferentialOutputComponent = ({ trial, artifact, componentType, urlPath }) => {
    const note = useMemo(() => {
        return React.createElement(MarkdownRenderer, { body: trial.note.body });
    }, [trial.note.body]);
    if (componentType === undefined || componentType.output_type === "note") {
        return note;
    }
    if (componentType.output_type === "artifact") {
        if (artifact === undefined) {
            return null;
        }
        return (React.createElement(ArtifactCardMedia, { artifact: artifact, urlPath: urlPath, height: "100%" }));
    }
    return null;
};
//# sourceMappingURL=PreferentialOutputComponent.js.map