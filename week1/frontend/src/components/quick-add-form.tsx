import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { createResolution } from "@/api/client"

export function QuickAddForm() {
  const navigate = useNavigate()
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [targetDate, setTargetDate] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim() || !description.trim()) return

    setSubmitting(true)
    setError("")
    try {
      const res = await createResolution({
        title: title.trim(),
        description: description.trim(),
        target_date: targetDate || null,
      })
      setTitle("")
      setDescription("")
      setTargetDate("")
      navigate(`/resolution/${res.id}`)
    } catch {
      setError("Failed to create resolution. Please try again.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>New Resolution</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-3">
          <Input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <Textarea
            placeholder="What do you want to achieve?"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            required
          />
          <Input
            type="date"
            value={targetDate}
            onChange={(e) => setTargetDate(e.target.value)}
            placeholder="Target date (optional)"
          />
          {error && <p className="text-sm text-destructive">{error}</p>}
          <Button type="submit" disabled={submitting} className="w-full">
            {submitting ? "Analyzing..." : "Create Resolution"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
