"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, ArrowRight } from "lucide-react"
import Link from "next/link"

interface QuestionBankUnit {
  unit_number: number
  unit_name: string
  topics: string[]
}

export default function Topics() {
  const router = useRouter()
  const [questionBank, setQuestionBank] = useState<QuestionBankUnit[]>([])
  const [selectedUnit, setSelectedUnit] = useState<number | null>(null)
  const [selectedTopics, setSelectedTopics] = useState<string[]>([])

  // ✅ Fetch and transform question bank data from FastAPI
  useEffect(() => {
    fetch("http://localhost:8000/question-bank")
      .then((res) => res.json())
      .then((data) => {
        const transformed: QuestionBankUnit[] = data.Units.map((unit: any) => ({
          unit_number: parseInt(unit["Unit Number"]),
          unit_name: unit["Unit Name"],
          topics: Object.keys(unit.Topics)
        }))
        setQuestionBank(transformed)
      })
      .catch((err) => console.error("Failed to fetch question bank", err))
  }, [])

  const handleUnitChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const unitNum = parseInt(e.target.value)
    setSelectedUnit(unitNum)
    const unit = questionBank.find((u) => u.unit_number === unitNum)
    setSelectedTopics(unit ? unit.topics : [])
  }

  const handleTopicChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = Array.from(e.target.selectedOptions).map((opt) => opt.value)
    setSelectedTopics(selectedOptions)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedTopics.length === 0) {
      alert("Please select at least one topic")
      return
    }

    // ✅ Save to local storage or send to backend/context if needed
    localStorage.setItem("selectedTopics", JSON.stringify(selectedTopics))

    router.push("/exam")
  }

  const topicsForSelectedUnit = questionBank.find((u) => u.unit_number === selectedUnit)?.topics || []

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-md w-full">
        <Card className="border-2 shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl">Select Unit & Topics</CardTitle>
            <CardDescription>Select the unit and the corresponding topics</CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div>
                <label htmlFor="unit" className="block mb-1 font-medium">
                  Select Unit
                </label>
                <select
                  id="unit"
                  value={selectedUnit ?? ""}
                  onChange={handleUnitChange}
                  className="w-full border px-3 py-2 rounded"
                  required
                >
                  <option value="" disabled>Select a unit</option>
                  {questionBank.map((unit) => (
                    <option key={unit.unit_number} value={unit.unit_number}>
                      {unit.unit_name}
                    </option>
                  ))}
                </select>
              </div>

              {selectedUnit !== null && (
                <div>
                  <label htmlFor="topics" className="block mb-1 font-medium">
                    Select Topics
                  </label>
                  <select
                    id="topics"
                    multiple
                    value={selectedTopics}
                    onChange={handleTopicChange}
                    className="w-full border px-3 py-2 rounded h-32"
                  >
                    {topicsForSelectedUnit.map((topic, idx) => (
                      <option key={idx} value={topic}>
                        {topic}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline" asChild>
                <Link href="/login">
                  <ArrowLeft className="mr-2 h-4 w-4" /> Back
                </Link>
              </Button>
              <Button type="submit">
                Start Exam <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </CardFooter>
          </form>
        </Card>
      </div>
    </main>
  )
}
