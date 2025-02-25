import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  useTheme,
} from "@mui/material"
import React, { ReactNode, useState, FC } from "react"
import { Artifact } from "ts/types/optuna"
import { actionCreator } from "../../action"

export const useDeleteTrialArtifactDialog = (): [
  (studyId: number, trialId: number, artifact: Artifact) => void,
  () => ReactNode,
] => {
  const action = actionCreator()

  const [openDeleteArtifactDialog, setOpenDeleteArtifactDialog] =
    useState(false)
  const [target, setTarget] = useState<[number, number, Artifact | null]>([
    -1,
    -1,
    null,
  ])

  const handleCloseDeleteArtifactDialog = () => {
    setOpenDeleteArtifactDialog(false)
    setTarget([-1, -1, null])
  }

  const handleDeleteArtifact = () => {
    const [studyId, trialId, artifact] = target
    if (artifact === null) {
      return
    }
    action.deleteTrialArtifact(studyId, trialId, artifact.artifact_id)
    setOpenDeleteArtifactDialog(false)
    setTarget([-1, -1, null])
  }

  const openDialog = (studyId: number, trialId: number, artifact: Artifact) => {
    setTarget([studyId, trialId, artifact])
    setOpenDeleteArtifactDialog(true)
  }

  const renderDeleteArtifactDialog = () => {
    return (
      <DeleteDialog
        openDeleteArtifactDialog={openDeleteArtifactDialog}
        handleCloseDeleteArtifactDialog={handleCloseDeleteArtifactDialog}
        filename={target[2]?.filename}
        handleDeleteArtifact={handleDeleteArtifact}
      />
    )
  }
  return [openDialog, renderDeleteArtifactDialog]
}

export const useDeleteStudyArtifactDialog = (): [
  (studyId: number, artifact: Artifact) => void,
  () => ReactNode,
] => {
  const action = actionCreator()

  const [openDeleteArtifactDialog, setOpenDeleteArtifactDialog] =
    useState(false)
  const [target, setTarget] = useState<[number, Artifact | null]>([-1, null])

  const handleCloseDeleteArtifactDialog = () => {
    setOpenDeleteArtifactDialog(false)
    setTarget([-1, null])
  }

  const handleDeleteArtifact = () => {
    const [studyId, artifact] = target
    if (artifact === null) {
      return
    }
    action.deleteStudyArtifact(studyId, artifact.artifact_id)
    setOpenDeleteArtifactDialog(false)
    setTarget([-1, null])
  }

  const openDialog = (studyId: number, artifact: Artifact) => {
    setTarget([studyId, artifact])
    setOpenDeleteArtifactDialog(true)
  }

  const renderDeleteArtifactDialog = () => {
    return (
      <DeleteDialog
        openDeleteArtifactDialog={openDeleteArtifactDialog}
        handleCloseDeleteArtifactDialog={handleCloseDeleteArtifactDialog}
        filename={target[1]?.filename}
        handleDeleteArtifact={handleDeleteArtifact}
      />
    )
  }
  return [openDialog, renderDeleteArtifactDialog]
}

const DeleteDialog: FC<{
  openDeleteArtifactDialog: boolean
  handleCloseDeleteArtifactDialog: () => void
  filename: string | undefined
  handleDeleteArtifact: () => void
}> = ({
  openDeleteArtifactDialog,
  handleCloseDeleteArtifactDialog,
  filename,
  handleDeleteArtifact,
}) => {
  const theme = useTheme()
  return (
    <Dialog
      open={openDeleteArtifactDialog}
      onClose={() => {
        handleCloseDeleteArtifactDialog()
      }}
      aria-labelledby="delete-artifact-dialog-title"
    >
      <DialogTitle id="delete-artifact-dialog-title">
        Delete artifact
      </DialogTitle>
      <DialogContent>
        <DialogContentText
          sx={{
            marginBottom: theme.spacing(2),
          }}
        >
          Are you sure you want to delete an artifact ("
          {filename}")?
        </DialogContentText>
        <Alert severity="warning">
          If this artifact is linked to another study or trial, it will no
          longer be accessible from that study or trial as well.
        </Alert>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCloseDeleteArtifactDialog} color="primary">
          No
        </Button>
        <Button onClick={handleDeleteArtifact} color="primary">
          Yes
        </Button>
      </DialogActions>
    </Dialog>
  )
}
