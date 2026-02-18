import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { createCheckIn } from "@/api/client"
import type { CheckInResponse } from "@/api/types"

interface CheckInFormProps {
  resolutionId: number
  onCreated: (checkIn: CheckInResponse) => void
}

export function CheckInForm({ resolutionId, onCreated }: CheckInFormProps) {
  const [note, setNote] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!note.trim()) return

    setSubmitting(true)
    setError("")
    try {
      const checkIn = await createCheckIn(resolutionId, { note: note.trim() })
      setNote("")
      onCreated(checkIn)
    } catch {
      setError("Failed to submit check-in. Please try again.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">New Check-in</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-3">
          <Textarea
            placeholder="How's your progress? What have you accomplished?"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={3}
            required
          />
          {error && <p className="text-sm text-destructive">{error}</p>}
          <Button type="submit" disabled={submitting}>
            {submitting ? "Analyzing..." : "Submit Check-in"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
