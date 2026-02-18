import { useState, useEffect, useCallback } from "react"
import type { DueReminder } from "@/api/types"
import { getDueReminders } from "@/api/client"

const POLL_INTERVAL = 5 * 60 * 1000

export function useReminders() {
  const [reminders, setReminders] = useState<DueReminder[]>([])

  const refresh = useCallback(async () => {
    try {
      const data = await getDueReminders()
      setReminders(data)
    } catch {
      // silently ignore polling errors
    }
  }, [])

  useEffect(() => {
    refresh()
    const id = setInterval(refresh, POLL_INTERVAL)
    return () => clearInterval(id)
  }, [refresh])

  return { reminders, refresh }
}
