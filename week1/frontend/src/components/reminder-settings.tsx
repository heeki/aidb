import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { updateReminder } from "@/api/client"
import type { ReminderResponse } from "@/api/types"

interface ReminderSettingsProps {
  resolutionId: number
  reminder: ReminderResponse | null
  onUpdated: (reminder: ReminderResponse) => void
}

const FREQUENCIES = ["daily", "weekly", "biweekly", "monthly"]

export function ReminderSettings({
  resolutionId,
  reminder,
  onUpdated,
}: ReminderSettingsProps) {
  const [frequency, setFrequency] = useState(reminder?.frequency ?? "weekly")
  const [saving, setSaving] = useState(false)

  async function handleSave() {
    setSaving(true)
    try {
      const updated = await updateReminder(resolutionId, {
        frequency,
        is_active: true,
      })
      onUpdated(updated)
    } catch {
      // ignore
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Reminder Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center gap-3">
          <Select value={frequency} onValueChange={setFrequency}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {FREQUENCIES.map((f) => (
                <SelectItem key={f} value={f}>
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button onClick={handleSave} disabled={saving} size="sm">
            {saving ? "Saving..." : "Save"}
          </Button>
        </div>
        {reminder && (
          <p className="text-xs text-muted-foreground">
            Next due: {new Date(reminder.next_due).toLocaleDateString()}
          </p>
        )}
      </CardContent>
    </Card>
  )
}
