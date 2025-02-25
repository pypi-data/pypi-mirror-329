import { Box } from "@mui/material";
import React, { useCallback, useEffect, useState, useRef } from "react";
import WaveSurfer from "wavesurfer.js";
const useWavesurfer = (containerRef, options) => {
    const [wavesurfer, setWavesurfer] = useState(null);
    useEffect(() => {
        if (!containerRef.current)
            return;
        const ws = WaveSurfer.create(Object.assign(Object.assign({}, options), { container: containerRef.current }));
        setWavesurfer(ws);
        return () => {
            ws.destroy();
        };
    }, [containerRef]);
    return wavesurfer;
};
// Create a React component of wavesurfer.
export const WaveSurferArtifactViewer = (props) => {
    const containerRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const wavesurfer = useWavesurfer(containerRef, props);
    const onPlayClick = useCallback(() => {
        if (!wavesurfer)
            return;
        wavesurfer.isPlaying() ? wavesurfer.pause() : wavesurfer.play();
    }, [wavesurfer]);
    useEffect(() => {
        if (!wavesurfer)
            return;
        setIsPlaying(false);
        const subscriptions = [
            wavesurfer.on("play", () => setIsPlaying(true)),
            wavesurfer.on("pause", () => setIsPlaying(false)),
        ];
        return () => {
            subscriptions.forEach((unsub) => unsub());
        };
    }, [wavesurfer]);
    return (React.createElement(Box, { component: "div", style: { width: "100%", display: "flex", flexDirection: "column" } },
        React.createElement("div", { ref: containerRef, style: { minHeight: "120px", width: "100%" } }),
        React.createElement("button", { onClick: onPlayClick, style: { marginTop: "1em" } }, isPlaying ? "Pause" : "Play")));
};
//# sourceMappingURL=WaveSurferArtifactViewer.js.map