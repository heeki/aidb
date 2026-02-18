import { useState } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import type { DueReminder } from "@/api/types"

interface ReminderBannerProps {
  reminders: DueReminder[]
}

export function ReminderBanner({ reminders }: ReminderBannerProps) {
  const [dismissed, setDismissed] = useState(false)

  if (dismissed || reminders.length === 0) return null

  return (
    <div className="bg-destructive/10 border border-destructive/30 rounded-lg px-4 py-3 flex items-center justify-between">
      <div className="flex-1">
        <p className="text-sm font-medium text-destructive">
          {reminders.length} overdue reminder{reminders.length > 1 ? "s" : ""}
        </p>
        <div className="flex flex-wrap gap-2 mt-1">
          {reminders.map((r) => (
            <Link
              key={r.resolution_id}
              to={`/resolution/${r.resolution_id}`}
              className="text-xs underline text-destructive hover:opacity-80"
            >
              {r.resolution_title}
            </Link>
          ))}
        </div>
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setDismissed(true)}
        className="ml-2 text-destructive"
      >
        Dismiss
      </Button>
    </div>
  )
}
