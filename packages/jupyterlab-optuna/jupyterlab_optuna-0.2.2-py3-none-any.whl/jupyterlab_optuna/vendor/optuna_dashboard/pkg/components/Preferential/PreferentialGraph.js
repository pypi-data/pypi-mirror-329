import { Box, Card, CardContent, Chip, Typography, useTheme, } from "@mui/material";
import ELK from "elkjs/lib/elk.bundled.js";
import React, { useState, useCallback, useEffect } from "react";
import ReactFlow, { applyNodeChanges, MiniMap, Position, Handle, } from "reactflow";
import "reactflow/dist/style.css";
import { useArtifactBaseUrlPath } from "../../hooks/useArtifactBaseUrlPath";
import { useStudyDetailValue } from "../../state";
import { getTrialArtifactUrlPath } from "../Artifact/TrialArtifactCards";
import { PreferentialOutputComponent } from "./PreferentialOutputComponent";
const elk = new ELK();
const nodeWidth = 400;
const nodeHeight = 300;
const nodeMargin = 60;
const GraphNode = ({ data, isConnectable }) => {
    var _a;
    const theme = useTheme();
    const artifactBaseUrl = useArtifactBaseUrlPath();
    const trial = data.trial;
    if (trial === undefined) {
        return null;
    }
    const studyDetail = useStudyDetailValue(trial.study_id);
    const componentType = studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.feedback_component_type;
    if (componentType === undefined) {
        return null;
    }
    const artifactId = componentType.output_type === "artifact"
        ? (_a = trial.user_attrs.find((a) => a.key === componentType.artifact_key)) === null || _a === void 0 ? void 0 : _a.value
        : undefined;
    const artifact = trial.artifacts.find((a) => a.artifact_id === artifactId);
    const urlPath = artifactId !== undefined
        ? getTrialArtifactUrlPath(artifactBaseUrl, trial.study_id, trial.trial_id, artifactId)
        : "";
    return (React.createElement(Card, { sx: {
            width: nodeWidth,
            height: nodeHeight,
            overflow: "hidden",
        } },
        React.createElement(Box, { component: "div", sx: {
                display: "flex",
                displayDirection: "row",
                margin: theme.spacing(2),
            } },
            React.createElement(Typography, { variant: "h5" },
                "Trial ",
                trial.number),
            data.isBest && (React.createElement(Chip, { label: "Best Trial", color: "secondary", variant: "outlined", sx: {
                    marginLeft: "auto",
                } }))),
        React.createElement(Handle, { type: "target", position: Position.Top, style: { background: "#555" }, isConnectable: isConnectable }),
        React.createElement(CardContent, { sx: {
                position: "relative",
                margin: 0,
                padding: theme.spacing(1),
                width: nodeWidth,
                height: nodeHeight - 72,
            } },
            React.createElement(PreferentialOutputComponent, { trial: trial, artifact: artifact, componentType: componentType, urlPath: urlPath })),
        React.createElement(Handle, { type: "source", position: Position.Bottom, style: { background: "#555" }, isConnectable: isConnectable })));
};
const nodeTypes = {
    note: GraphNode,
};
const defaultEdgeOptions = {
    animated: true,
};
const reductionPreference = (input_preferences) => {
    const preferences = [];
    let n = 0;
    for (const [source, target] of input_preferences) {
        if (preferences.find((p) => p[0] === source && p[1] === target) !==
            undefined ||
            input_preferences.find((p) => p[0] === target && p[1] === source) !==
                undefined) {
            continue;
        }
        n = Math.max(n - 1, source, target) + 1;
        preferences.push([source, target]);
    }
    if (n === 0) {
        return [];
    }
    const graph = Array.from({ length: n }, () => []);
    const reverseGraph = Array.from({ length: n }, () => []);
    const degree = Array.from({ length: n }, () => 0);
    for (const [source, target] of preferences) {
        graph[source].push(target);
        reverseGraph[target].push(source);
        degree[target]++;
    }
    const topologicalOrder = [];
    const q = [];
    for (let i = 0; i < n; i++) {
        if (degree[i] === 0) {
            q.push(i);
        }
    }
    while (q.length > 0) {
        const v = q.pop();
        if (v === undefined)
            break;
        topologicalOrder.push(v);
        graph[v].forEach((u) => {
            degree[u]--;
            if (degree[u] === 0) {
                q.push(u);
            }
        });
    }
    if (topologicalOrder.length !== n) {
        console.error("cycle detected");
        return preferences;
    }
    const response = [];
    const descendants = Array.from({ length: n }, () => new Set());
    topologicalOrder.reverse().forEach((v) => {
        const descendant = new Set([v]);
        graph[v].forEach((u) => {
            descendants[u].forEach((d) => descendant.add(d));
        });
        graph[v].forEach((u) => {
            if (reverseGraph[u].filter((d) => descendant.has(d)).length === 1) {
                response.push([v, u]);
            }
        });
        descendants[v] = descendant;
    });
    return response;
};
export const PreferentialGraph = ({ studyDetail }) => {
    const theme = useTheme();
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const onNodesChange = useCallback((changes) => setNodes((nds) => applyNodeChanges(changes, nds)), [setNodes]);
    useEffect(() => {
        var _a;
        if (studyDetail === null)
            return;
        if (!studyDetail.is_preferential || studyDetail.preferences === undefined)
            return;
        const preferences = reductionPreference(studyDetail.preferences);
        const trialNodes = Array.from(new Set(preferences.flat()));
        const graph = {
            id: "root",
            layoutOptions: {
                "elk.algorithm": "layered",
                "elk.direction": "DOWN",
                "elk.layered.spacing.nodeNodeBetweenLayers": nodeMargin.toString(),
                "elk.spacing.nodeNode": nodeMargin.toString(),
            },
            children: trialNodes.map((trial) => ({
                id: `${trial}`,
                targetPosition: "top",
                sourcePosition: "bottom",
                width: nodeWidth,
                height: nodeHeight,
            })),
            edges: preferences.map(([source, target]) => ({
                id: `e${source}-${target}`,
                sources: [`${source}`],
                targets: [`${target}`],
            })),
        };
        elk
            .layout(graph)
            .then((layoutedGraph) => {
            var _a, _b;
            setNodes((_b = (_a = layoutedGraph.children) === null || _a === void 0 ? void 0 : _a.map((node, index) => {
                var _a, _b;
                const trial = studyDetail.trials[trialNodes[index]];
                return {
                    id: `${trial.number}`,
                    type: "note",
                    data: {
                        label: `Trial ${trial.number}`,
                        trial: trial,
                        isBest: studyDetail.best_trials.find((t) => t.number === trial.number) !== undefined,
                    },
                    position: {
                        x: (_a = node.x) !== null && _a !== void 0 ? _a : 0,
                        y: (_b = node.y) !== null && _b !== void 0 ? _b : 0,
                    },
                    style: {
                        width: nodeWidth,
                        height: nodeHeight,
                        padding: 0,
                    },
                    deletable: false,
                    connectable: false,
                    draggable: false,
                };
            })) !== null && _b !== void 0 ? _b : []);
        })
            .catch(console.error);
        setEdges((_a = preferences.map((p) => {
            return {
                id: `e${p[0]}-${p[1]}`,
                source: `${p[0]}`,
                target: `${p[1]}`,
                style: { stroke: theme.palette.text.primary },
            };
        })) !== null && _a !== void 0 ? _a : []);
    }, [studyDetail, theme.palette.text.primary]);
    if (studyDetail === null || !studyDetail.is_preferential) {
        return null;
    }
    return (React.createElement(ReactFlow, { nodes: nodes, edges: edges, onNodesChange: onNodesChange, defaultEdgeOptions: defaultEdgeOptions, nodeTypes: nodeTypes, zoomOnScroll: false, panOnScroll: true, minZoom: 0.1, defaultViewport: {
            x: 0,
            y: 0,
            zoom: 0.5,
        } },
        React.createElement(MiniMap, { nodeStrokeWidth: 1, zoomable: true, pannable: true })));
};
//# sourceMappingURL=PreferentialGraph.js.map