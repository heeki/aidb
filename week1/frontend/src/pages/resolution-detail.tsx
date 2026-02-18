import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { CheckInForm } from "@/components/check-in-form"
import { CheckInTimeline } from "@/components/check-in-timeline"
import { ReminderSettings } from "@/components/reminder-settings"
import { ConfirmDialog } from "@/components/confirm-dialog"
import type { ResolutionDetail as ResolutionDetailType, CheckInResponse, ReminderResponse } from "@/api/types"
import { getResolution, deleteResolution, updateResolution } from "@/api/client"

function statusVariant(status: string) {
  switch (status) {
    case "completed":
      return "default" as const
    case "abandoned":
      return "destructive" as const
    default:
      return "secondary" as const
  }
}

export function ResolutionDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [resolution, setResolution] = useState<ResolutionDetailType | null>(null)
  const [loading, setLoading] = useState(true)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    getResolution(Number(id))
      .then(setResolution)
      .catch(() => navigate("/"))
      .finally(() => setLoading(false))
  }, [id, navigate])

  function handleCheckInCreated(checkIn: CheckInResponse) {
    if (!resolution) return
    setResolution({
      ...resolution,
      check_ins: [...resolution.check_ins, checkIn],
    })
  }

  function handleReminderUpdated(reminder: ReminderResponse) {
    if (!resolution) return
    setResolution({ ...resolution, reminder })
  }

  async function handleDelete() {
    if (!resolution) return
    setDeleting(true)
    try {
      await deleteResolution(resolution.id)
      navigate("/")
    } catch {
      setDeleting(false)
    }
  }

  async function handleStatusChange(status: string) {
    if (!resolution) return
    try {
      await updateResolution(resolution.id, { status })
      setResolution({ ...resolution, status })
    } catch {
      // ignore
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-48 w-full" />
      </div>
    )
  }

  if (!resolution) return null

  return (
    <>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">{resolution.title}</h1>
          <div className="flex items-center gap-2 mt-1">
            <Badge variant={statusVariant(resolution.status)}>
              {resolution.status}
            </Badge>
            {resolution.category && (
              <Badge variant="outline">{resolution.category}</Badge>
            )}
            {resolution.priority != null && (
              <Badge variant="outline">Priority: {resolution.priority}</Badge>
            )}
          </div>
        </div>
        <div className="flex gap-2">
          {resolution.status === "active" && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleStatusChange("completed")}
            >
              Mark Complete
            </Button>
          )}
          <Button
            variant="destructive"
            size="sm"
            onClick={() => setDeleteOpen(true)}
          >
            Delete
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>{resolution.description}</p>
          <Separator />
          <div className="flex gap-4 text-muted-foreground">
            {resolution.target_date && (
              <span>
                Target: {new Date(resolution.target_date).toLocaleDateString()}
              </span>
            )}
            <span>
              Created: {new Date(resolution.created_at).toLocaleDateString()}
            </span>
          </div>
        </CardContent>
      </Card>

      <ReminderSettings
        resolutionId={resolution.id}
        reminder={resolution.reminder}
        onUpdated={handleReminderUpdated}
      />

      <CheckInForm
        resolutionId={resolution.id}
        onCreated={handleCheckInCreated}
      />

      <CheckInTimeline checkIns={resolution.check_ins} />

      <ConfirmDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        title="Delete Resolution"
        description={`Are you sure you want to delete "${resolution.title}"? This action cannot be undone.`}
        onConfirm={handleDelete}
        loading={deleting}
      />
    </>
  )
}
