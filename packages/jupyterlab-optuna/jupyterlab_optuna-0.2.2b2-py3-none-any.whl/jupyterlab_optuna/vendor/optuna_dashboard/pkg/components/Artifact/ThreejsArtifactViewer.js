import ClearIcon from "@mui/icons-material/Clear";
import { Box, Modal, useTheme } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import { GizmoHelper, GizmoViewport, OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React, { useEffect, useState } from "react";
import * as THREE from "three";
import { Rhino3dmLoader } from "three/examples/jsm/loaders/3DMLoader";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
export const isThreejsArtifact = (artifact) => {
    return (artifact.filename.endsWith(".stl") ||
        artifact.filename.endsWith(".3dm") ||
        artifact.filename.endsWith(".obj"));
};
const CustomGizmoHelper = () => {
    return (React.createElement(GizmoHelper, { alignment: "bottom-right", margin: [80, 80] },
        React.createElement(GizmoViewport, { axisColors: ["red", "green", "skyblue"], labelColor: "black" })));
};
const computeBoundingBox = (geometries) => {
    const boundingBox = new THREE.Box3();
    geometries.forEach((geometry) => {
        const mesh = new THREE.Mesh(geometry);
        boundingBox.expandByObject(mesh);
    });
    return boundingBox;
};
export const ThreejsArtifactViewer = (props) => {
    const [geometry, setGeometry] = useState([]);
    const [boundingBox, setBoundingBox] = useState(new THREE.Box3(new THREE.Vector3(-10, -10, -10), new THREE.Vector3(10, 10, 10)));
    const [cameraSettings, setCameraSettings] = useState(new THREE.PerspectiveCamera());
    const handleLoadedGeometries = (geometries) => {
        setGeometry(geometries);
        const boundingBox = computeBoundingBox(geometries);
        if (boundingBox !== null) {
            setBoundingBox(boundingBox);
        }
        return boundingBox;
    };
    useEffect(() => {
        if ("stl" === props.filetype) {
            loadSTL(props, handleLoadedGeometries);
        }
        else if ("3dm" === props.filetype) {
            loadRhino3dm(props, handleLoadedGeometries);
        }
        else if ("obj" === props.filetype) {
            loadOBJ(props, handleLoadedGeometries);
        }
    }, []);
    useEffect(() => {
        const cameraSet = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, boundingBox.getSize(new THREE.Vector3()).length() * 100);
        const maxPosition = Math.max(boundingBox.max.x, boundingBox.max.y, boundingBox.max.z);
        cameraSet.position.set(maxPosition * 1.5, maxPosition * 1.5, maxPosition * 1.5);
        const center = boundingBox.getCenter(new THREE.Vector3());
        cameraSet.lookAt(center.x, center.y, center.z);
        setCameraSettings(cameraSet);
    }, [boundingBox]);
    return (React.createElement(Canvas, { frameloop: "demand", camera: cameraSettings, style: { width: props.width, height: props.height } },
        React.createElement("ambientLight", null),
        React.createElement(OrbitControls, null),
        React.createElement("gridHelper", { args: [Math.max(boundingBox.max.x, boundingBox.max.y) * 5] }),
        props.hasGizmo && React.createElement(CustomGizmoHelper, null),
        React.createElement("axesHelper", null),
        geometry.length > 0 &&
            geometry.map((geo, index) => (React.createElement("mesh", { key: index, geometry: geo },
                React.createElement("meshNormalMaterial", { side: THREE.DoubleSide }))))));
};
export const useThreejsArtifactModal = () => {
    const [open, setOpen] = useState(false);
    const [target, setTarget] = useState(["", null]);
    const theme = useTheme();
    const openModal = (artifactUrlPath, artifact) => {
        setTarget([artifactUrlPath, artifact]);
        setOpen(true);
    };
    const renderDeleteStudyDialog = () => {
        var _a;
        return (React.createElement(Modal, { open: open, onClose: () => {
                setOpen(false);
                setTarget(["", null]);
            } },
            React.createElement(Box, { component: "div", sx: {
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    bgcolor: "background.paper",
                    borderRadius: "15px",
                } },
                React.createElement(IconButton, { sx: {
                        position: "absolute",
                        top: theme.spacing(2),
                        right: theme.spacing(2),
                    }, onClick: () => {
                        setOpen(false);
                        setTarget(["", null]);
                    } },
                    React.createElement(ClearIcon, null)),
                React.createElement(ThreejsArtifactViewer, { src: target[0], width: `${innerWidth * 0.8}px`, height: `${innerHeight * 0.8}px`, hasGizmo: true, filetype: (_a = target[1]) === null || _a === void 0 ? void 0 : _a.filename.split(".").pop() }))));
    };
    return [openModal, renderDeleteStudyDialog];
};
function loadSTL(props, handleLoadedGeometries) {
    const stlLoader = new STLLoader();
    stlLoader.load(props.src, (stlGeometries) => {
        if (stlGeometries) {
            handleLoadedGeometries([stlGeometries]);
        }
    });
}
function loadRhino3dm(props, handleLoadedGeometries) {
    const rhino3dmLoader = new Rhino3dmLoader();
    rhino3dmLoader.setLibraryPath("https://cdn.jsdelivr.net/npm/rhino3dm@8.4.0/");
    rhino3dmLoader.load(props.src, (object) => {
        const meshes = object.children;
        const rhinoGeometries = meshes.map((mesh) => mesh.geometry);
        THREE.Object3D.DEFAULT_UP.set(0, 0, 1);
        if (rhinoGeometries.length > 0) {
            handleLoadedGeometries(rhinoGeometries);
        }
    });
}
function loadOBJ(props, handleLoadedGeometries) {
    const objLoader = new OBJLoader();
    objLoader.load(props.src, (object) => {
        const meshes = object.children;
        const objGeometries = meshes.map((mesh) => mesh.geometry);
        if (objGeometries.length > 0) {
            handleLoadedGeometries(objGeometries);
        }
    });
}
//# sourceMappingURL=ThreejsArtifactViewer.js.map