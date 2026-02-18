import { useEffect, useState } from "react"
import { SummaryCards } from "@/components/summary-cards"
import { QuickAddForm } from "@/components/quick-add-form"
import type { DashboardSummary } from "@/api/types"
import { getDashboardSummary } from "@/api/client"

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDashboardSummary()
      .then(setSummary)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <SummaryCards summary={summary} loading={loading} />
      <QuickAddForm />
    </>
  )
}
