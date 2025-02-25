import { useSnackbar } from "notistack";
import { useRecoilState, useSetRecoilState } from "recoil";
import { useAPIClient } from "./apiClientProvider";
import { getDominatedTrials } from "./dominatedTrials";
import { artifactIsAvailable, isFileUploading, plotlypyIsAvailableState, reloadIntervalState, studyDetailLoadingState, studyDetailsState, studySummariesLoadingState, studySummariesState, trialsUpdatingState, } from "./state";
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const actionCreator = () => {
    const { apiClient } = useAPIClient();
    const { enqueueSnackbar } = useSnackbar();
    const [studySummaries, setStudySummaries] = useRecoilState(studySummariesState);
    const [studyDetails, setStudyDetails] = useRecoilState(studyDetailsState);
    const setReloadInterval = useSetRecoilState(reloadIntervalState);
    const setUploading = useSetRecoilState(isFileUploading);
    const setTrialsUpdating = useSetRecoilState(trialsUpdatingState);
    const setArtifactIsAvailable = useSetRecoilState(artifactIsAvailable);
    const setPlotlypyIsAvailable = useSetRecoilState(plotlypyIsAvailableState);
    const setStudySummariesLoading = useSetRecoilState(studySummariesLoadingState);
    const [studyDetailLoading, setStudyDetailLoading] = useRecoilState(studyDetailLoadingState);
    const setStudyDetailState = (studyId, study) => {
        setStudyDetails((prevVal) => {
            const newVal = Object.assign({}, prevVal);
            newVal[studyId] = study;
            return newVal;
        });
    };
    const setTrial = (studyId, trialIndex, trial) => {
        const newTrials = [...studyDetails[studyId].trials];
        newTrials[trialIndex] = trial;
        const newStudy = Object.assign({}, studyDetails[studyId]);
        newStudy.trials = newTrials;
        setStudyDetailState(studyId, newStudy);
    };
    const setTrialUpdating = (trialId, updating) => {
        setTrialsUpdating((prev) => {
            const newVal = Object.assign({}, prev);
            newVal[trialId] = updating;
            return newVal;
        });
    };
    const setTrialNote = (studyId, index, note) => {
        const newTrial = Object.assign({}, studyDetails[studyId].trials[index]);
        newTrial.note = note;
        setTrial(studyId, index, newTrial);
    };
    const setTrialArtifacts = (studyId, trialIndex, artifacts) => {
        const newTrial = Object.assign({}, studyDetails[studyId].trials[trialIndex]);
        newTrial.artifacts = artifacts;
        setTrial(studyId, trialIndex, newTrial);
    };
    const setStudyArtifacts = (studyId, artifacts) => {
        const newStudy = Object.assign({}, studyDetails[studyId]);
        newStudy.artifacts = artifacts;
        setStudyDetailState(studyId, newStudy);
    };
    const deleteTrialArtifactState = (studyId, trialId, artifact_id) => {
        const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
        if (index === -1) {
            return;
        }
        const artifacts = studyDetails[studyId].trials[index].artifacts;
        const artifactIndex = artifacts.findIndex((a) => a.artifact_id === artifact_id);
        const newArtifacts = [
            ...artifacts.slice(0, artifactIndex),
            ...artifacts.slice(artifactIndex + 1, artifacts.length),
        ];
        setTrialArtifacts(studyId, index, newArtifacts);
    };
    const deleteStudyArtifactState = (studyId, artifact_id) => {
        const artifacts = studyDetails[studyId].artifacts;
        const artifactIndex = artifacts.findIndex((a) => a.artifact_id === artifact_id);
        const newArtifacts = [
            ...artifacts.slice(0, artifactIndex),
            ...artifacts.slice(artifactIndex + 1, artifacts.length),
        ];
        setStudyArtifacts(studyId, newArtifacts);
    };
    const setTrialStateValues = (studyId, index, state, values) => {
        var _a, _b;
        const newTrial = Object.assign({}, studyDetails[studyId].trials[index]);
        newTrial.state = state;
        newTrial.values = values;
        const newTrials = [...studyDetails[studyId].trials];
        newTrials[index] = newTrial;
        const newStudy = Object.assign({}, studyDetails[studyId]);
        newStudy.trials = newTrials;
        // Update Best Trials
        if (state === "Complete" && newStudy.directions.length === 1) {
            // Single objective optimization
            const bestValue = (_b = (_a = newStudy.best_trials.at(0)) === null || _a === void 0 ? void 0 : _a.values) === null || _b === void 0 ? void 0 : _b.at(0);
            const currentValue = values === null || values === void 0 ? void 0 : values.at(0);
            if (newStudy.best_trials.length === 0) {
                newStudy.best_trials = [newTrial];
            }
            else if (bestValue !== undefined && currentValue !== undefined) {
                if (newStudy.directions[0] === "minimize" && currentValue < bestValue) {
                    newStudy.best_trials = [newTrial];
                }
                else if (newStudy.directions[0] === "maximize" &&
                    currentValue > bestValue) {
                    newStudy.best_trials = [newTrial];
                }
                else if (currentValue === bestValue) {
                    newStudy.best_trials = [...newStudy.best_trials, newTrial];
                }
            }
        }
        else if (state === "Complete") {
            // Multi objective optimization
            newStudy.best_trials = getDominatedTrials(newStudy.trials, newStudy.directions);
        }
        setStudyDetailState(studyId, newStudy);
    };
    const setTrialUserAttrs = (studyId, index, user_attrs) => {
        const newTrial = Object.assign({}, studyDetails[studyId].trials[index]);
        newTrial.user_attrs = Object.keys(user_attrs).map((key) => ({
            key: key,
            value: user_attrs[key].toString(),
        }));
        const newTrials = [...studyDetails[studyId].trials];
        newTrials[index] = newTrial;
        const newStudy = Object.assign({}, studyDetails[studyId]);
        newStudy.trials = newTrials;
        setStudyDetailState(studyId, newStudy);
    };
    const updateAPIMeta = () => {
        apiClient.getMetaInfo().then((r) => {
            setArtifactIsAvailable(r.artifact_is_available);
            setPlotlypyIsAvailable(r.plotlypy_is_available);
        });
    };
    const updateStudySummaries = (successMsg) => {
        setStudySummariesLoading(true);
        apiClient
            .getStudySummaries()
            .then((studySummaries) => {
            setStudySummariesLoading(false);
            setStudySummaries(studySummaries);
            if (successMsg) {
                enqueueSnackbar(successMsg, { variant: "success" });
            }
        })
            .catch((err) => {
            setStudySummariesLoading(false);
            enqueueSnackbar(`Failed to fetch study list.`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const updateStudyDetail = (studyId) => {
        if (studyDetailLoading[studyId]) {
            return;
        }
        setStudyDetailLoading(Object.assign(Object.assign({}, studyDetailLoading), { [studyId]: true }));
        let nLocalFixedTrials = 0;
        if (studyId in studyDetails) {
            const currentTrials = studyDetails[studyId].trials;
            const firstUpdatable = currentTrials.findIndex((trial) => ["Running", "Waiting"].includes(trial.state));
            nLocalFixedTrials =
                firstUpdatable === -1 ? currentTrials.length : firstUpdatable;
        }
        apiClient
            .getStudyDetail(studyId, nLocalFixedTrials)
            .then((study) => {
            setStudyDetailLoading(Object.assign(Object.assign({}, studyDetailLoading), { [studyId]: false }));
            const currentFixedTrials = studyId in studyDetails
                ? studyDetails[studyId].trials.slice(0, nLocalFixedTrials)
                : [];
            study.trials = currentFixedTrials.concat(study.trials);
            setStudyDetailState(studyId, study);
        })
            .catch((err) => {
            var _a;
            setStudyDetailLoading(Object.assign(Object.assign({}, studyDetailLoading), { [studyId]: false }));
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            if (reason !== undefined) {
                enqueueSnackbar(`Failed to fetch study (reason=${reason})`, {
                    variant: "error",
                });
            }
            console.log(err);
        });
    };
    const createNewStudy = (studyName, directions) => {
        apiClient
            .createNewStudy(studyName, directions)
            .then((study_summary) => {
            const newVal = [...studySummaries, study_summary];
            setStudySummaries(newVal);
            enqueueSnackbar(`Success to create a study (study_name=${studyName})`, {
                variant: "success",
            });
        })
            .catch((err) => {
            enqueueSnackbar(`Failed to create a study (study_name=${studyName})`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const deleteStudy = (studyId, removeAssociatedArtifacts) => {
        apiClient
            .deleteStudy(studyId, removeAssociatedArtifacts)
            .then(() => {
            setStudySummaries(studySummaries.filter((s) => s.study_id !== studyId));
            enqueueSnackbar(`Success to delete a study (id=${studyId})`, {
                variant: "success",
            });
        })
            .catch((err) => {
            enqueueSnackbar(`Failed to delete study (id=${studyId})`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const renameStudy = (studyId, studyName) => {
        apiClient
            .renameStudy(studyId, studyName)
            .then((study) => {
            const newStudySummaries = [
                ...studySummaries.filter((s) => s.study_id !== studyId),
                study,
            ];
            setStudySummaries(newStudySummaries);
            enqueueSnackbar(`Success to delete a study (id=${studyId})`, {
                variant: "success",
            });
        })
            .catch((err) => {
            enqueueSnackbar(`Failed to rename study (id=${studyId})`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const saveReloadInterval = (interval) => {
        setReloadInterval(interval);
    };
    const saveStudyNote = (studyId, note) => {
        return apiClient
            .saveStudyNote(studyId, note)
            .then(() => {
            const newStudy = Object.assign({}, studyDetails[studyId]);
            newStudy.note = note;
            setStudyDetailState(studyId, newStudy);
            enqueueSnackbar(`Success to save the note`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            if (err.response.status === 409) {
                const newStudy = Object.assign({}, studyDetails[studyId]);
                newStudy.note = err.response.data.note;
                setStudyDetailState(studyId, newStudy);
            }
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            if (reason !== undefined) {
                enqueueSnackbar(`Failed: ${reason}`, {
                    variant: "error",
                });
            }
            throw err;
        });
    };
    const saveTrialNote = (studyId, trialId, note) => {
        return apiClient
            .saveTrialNote(studyId, trialId, note)
            .then(() => {
            const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
            if (index === -1) {
                enqueueSnackbar(`Unexpected error happens. Please reload the page.`, {
                    variant: "error",
                });
                return;
            }
            setTrialNote(studyId, index, note);
            enqueueSnackbar(`Success to save the note`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            if (err.response.status === 409) {
                const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
                if (index === -1) {
                    enqueueSnackbar(`Unexpected error happens. Please reload the page.`, {
                        variant: "error",
                    });
                    return;
                }
                setTrialNote(studyId, index, err.response.data.note);
            }
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            if (reason !== undefined) {
                enqueueSnackbar(`Failed: ${reason}`, {
                    variant: "error",
                });
            }
            throw err;
        });
    };
    const uploadTrialArtifact = (studyId, trialId, file) => {
        const reader = new FileReader();
        setUploading(true);
        reader.readAsDataURL(file);
        reader.onload = (upload) => {
            var _a;
            apiClient
                .uploadTrialArtifact(studyId, trialId, file.name, (_a = upload.target) === null || _a === void 0 ? void 0 : _a.result)
                .then((res) => {
                setUploading(false);
                const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
                if (index === -1) {
                    return;
                }
                setTrialArtifacts(studyId, index, res.artifacts);
            })
                .catch((err) => {
                var _a;
                setUploading(false);
                const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
                enqueueSnackbar(`Failed to upload ${reason}`, { variant: "error" });
            });
        };
        reader.onerror = (error) => {
            enqueueSnackbar(`Failed to read the file ${error}`, { variant: "error" });
            console.log(error);
        };
    };
    const uploadStudyArtifact = (studyId, file) => {
        const reader = new FileReader();
        setUploading(true);
        reader.readAsDataURL(file);
        reader.onload = (upload) => {
            var _a;
            apiClient
                .uploadStudyArtifact(studyId, file.name, (_a = upload.target) === null || _a === void 0 ? void 0 : _a.result)
                .then((res) => {
                setUploading(false);
                setStudyArtifacts(studyId, res.artifacts);
            })
                .catch((err) => {
                var _a;
                setUploading(false);
                const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
                enqueueSnackbar(`Failed to upload ${reason}`, { variant: "error" });
            });
        };
        reader.onerror = (error) => {
            enqueueSnackbar(`Failed to read the file ${error}`, { variant: "error" });
            console.log(error);
        };
    };
    const deleteTrialArtifact = (studyId, trialId, artifactId) => {
        apiClient
            .deleteTrialArtifact(studyId, trialId, artifactId)
            .then(() => {
            deleteTrialArtifactState(studyId, trialId, artifactId);
            enqueueSnackbar(`Success to delete an artifact.`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to delete ${reason}.`, {
                variant: "error",
            });
        });
    };
    const deleteStudyArtifact = (studyId, artifactId) => {
        apiClient
            .deleteStudyArtifact(studyId, artifactId)
            .then(() => {
            deleteStudyArtifactState(studyId, artifactId);
            enqueueSnackbar(`Success to delete an artifact.`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to delete ${reason}.`, {
                variant: "error",
            });
        });
    };
    const makeTrialFail = (studyId, trialId) => {
        const message = `id=${trialId}, state=Fail`;
        setTrialUpdating(trialId, true);
        apiClient
            .tellTrial(trialId, "Fail")
            .then(() => {
            const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
            if (index === -1) {
                enqueueSnackbar(`Unexpected error happens. Please reload the page.`, {
                    variant: "error",
                });
                return;
            }
            setTrialStateValues(studyId, index, "Fail");
            enqueueSnackbar(`Successfully updated trial (${message})`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            setTrialUpdating(trialId, false);
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to update trial (${message}). Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const makeTrialComplete = (studyId, trialId, values) => {
        const message = `id=${trialId}, state=Complete, values=${values}`;
        setTrialUpdating(trialId, true);
        apiClient
            .tellTrial(trialId, "Complete", values)
            .then(() => {
            const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
            if (index === -1) {
                enqueueSnackbar(`Unexpected error happens. Please reload the page.`, {
                    variant: "error",
                });
                return;
            }
            setTrialStateValues(studyId, index, "Complete", values);
        })
            .catch((err) => {
            var _a;
            setTrialUpdating(trialId, false);
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to update trial (${message}). Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const saveTrialUserAttrs = (studyId, trialId, user_attrs) => {
        const message = `id=${trialId}, user_attrs=${JSON.stringify(user_attrs)}`;
        setTrialUpdating(trialId, true);
        apiClient
            .saveTrialUserAttrs(trialId, user_attrs)
            .then(() => {
            const index = studyDetails[studyId].trials.findIndex((t) => t.trial_id === trialId);
            if (index === -1) {
                enqueueSnackbar(`Unexpected error happens. Please reload the page.`, {
                    variant: "error",
                });
                return;
            }
            setTrialUserAttrs(studyId, index, user_attrs);
            enqueueSnackbar(`Successfully updated trial (${message})`, {
                variant: "success",
            });
        })
            .catch((err) => {
            var _a;
            setTrialUpdating(trialId, false);
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to update trial (${message}). Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const updatePreference = (studyId, candidates, clicked) => {
        apiClient.reportPreference(studyId, candidates, clicked).catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to report preference. Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const skipPreferentialTrial = (studyId, trialId) => {
        apiClient.skipPreferentialTrial(studyId, trialId).catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to skip trial. Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const updateFeedbackComponent = (studyId, compoennt_type) => {
        apiClient
            .reportFeedbackComponent(studyId, compoennt_type)
            .then(() => {
            const newStudy = Object.assign({}, studyDetails[studyId]);
            newStudy.feedback_component_type = compoennt_type;
            setStudyDetailState(studyId, newStudy);
        })
            .catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to report feedback component. Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const removePreferentialHistory = (studyId, historyId) => {
        apiClient
            .removePreferentialHistory(studyId, historyId)
            .then(() => {
            var _a, _b, _c, _d;
            const newStudy = Object.assign({}, studyDetails[studyId]);
            newStudy.preference_history = (_a = newStudy.preference_history) === null || _a === void 0 ? void 0 : _a.map((h) => h.id === historyId ? Object.assign(Object.assign({}, h), { is_removed: true }) : h);
            const removed = (_c = (_b = newStudy.preference_history) === null || _b === void 0 ? void 0 : _b.filter((h) => h.id === historyId).pop()) === null || _c === void 0 ? void 0 : _c.preferences;
            newStudy.preferences = (_d = newStudy.preferences) === null || _d === void 0 ? void 0 : _d.filter((p) => !(removed === null || removed === void 0 ? void 0 : removed.some((r) => r[0] === p[0] && r[1] === p[1])));
            setStudyDetailState(studyId, newStudy);
        })
            .catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to switch history. Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    const restorePreferentialHistory = (studyId, historyId) => {
        apiClient
            .restorePreferentialHistory(studyId, historyId)
            .then(() => {
            var _a, _b, _c, _d;
            const newStudy = Object.assign({}, studyDetails[studyId]);
            newStudy.preference_history = (_a = newStudy.preference_history) === null || _a === void 0 ? void 0 : _a.map((h) => h.id === historyId ? Object.assign(Object.assign({}, h), { is_removed: false }) : h);
            const restored = (_c = (_b = newStudy.preference_history) === null || _b === void 0 ? void 0 : _b.filter((h) => h.id === historyId).pop()) === null || _c === void 0 ? void 0 : _c.preferences;
            newStudy.preferences = (_d = newStudy.preferences) === null || _d === void 0 ? void 0 : _d.concat(restored !== null && restored !== void 0 ? restored : []);
            setStudyDetailState(studyId, newStudy);
        })
            .catch((err) => {
            var _a;
            const reason = (_a = err.response) === null || _a === void 0 ? void 0 : _a.data.reason;
            enqueueSnackbar(`Failed to switch history. Reason: ${reason}`, {
                variant: "error",
            });
            console.log(err);
        });
    };
    return {
        updateAPIMeta,
        updateStudyDetail,
        updateStudySummaries,
        createNewStudy,
        deleteStudy,
        renameStudy,
        saveReloadInterval,
        saveStudyNote,
        saveTrialNote,
        uploadTrialArtifact,
        uploadStudyArtifact,
        deleteTrialArtifact,
        deleteStudyArtifact,
        makeTrialComplete,
        makeTrialFail,
        saveTrialUserAttrs,
        updatePreference,
        skipPreferentialTrial,
        removePreferentialHistory,
        restorePreferentialHistory,
        updateFeedbackComponent,
    };
};
//# sourceMappingURL=action.js.map