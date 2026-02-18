import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import type { CheckInResponse } from "@/api/types"

interface CheckInTimelineProps {
  checkIns: CheckInResponse[]
}

function sentimentVariant(sentiment: string | null) {
  switch (sentiment) {
    case "positive":
      return "default" as const
    case "negative":
      return "destructive" as const
    default:
      return "secondary" as const
  }
}

function sentimentColor(sentiment: string | null) {
  switch (sentiment) {
    case "positive":
      return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
    case "negative":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
    case "neutral":
      return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
    default:
      return ""
  }
}

export function CheckInTimeline({ checkIns }: CheckInTimelineProps) {
  if (checkIns.length === 0) {
    return (
      <p className="text-sm text-muted-foreground py-4">
        No check-ins yet. Submit your first one above!
      </p>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Check-in History</h3>
      {checkIns
        .slice()
        .sort((a, b) => b.created_at.localeCompare(a.created_at))
        .map((ci, i) => (
          <div key={ci.id}>
            {i > 0 && <Separator className="mb-4" />}
            <Card>
              <CardContent className="pt-4 space-y-2">
                <div className="flex items-center justify-between">
                  <time className="text-xs text-muted-foreground">
                    {new Date(ci.created_at).toLocaleString()}
                  </time>
                  {ci.sentiment && (
                    <Badge
                      variant={sentimentVariant(ci.sentiment)}
                      className={sentimentColor(ci.sentiment)}
                    >
                      {ci.sentiment}
                      {ci.sentiment_score != null &&
                        ` (${ci.sentiment_score.toFixed(2)})`}
                    </Badge>
                  )}
                </div>
                <p className="text-sm">{ci.note}</p>
                {ci.ai_feedback && (
                  <div className="bg-muted rounded-md p-3 text-sm">
                    <p className="font-medium text-xs text-muted-foreground mb-1">
                      AI Feedback
                    </p>
                    <p>{ci.ai_feedback}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        ))}
    </div>
  )
}
