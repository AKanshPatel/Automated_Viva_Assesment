"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Home, Download, Award } from "lucide-react"
import Link from "next/link"

// Mock results data - in a real app, this would come from the API
const mockResults = {
  studentName: "John Doe",
  studentId: "S12345",
  totalScore: 85,
  maxScore: 100,
  feedback: "Good understanding of core concepts. Could improve on technical terminology and depth of explanations.",
  questionScores: [
    {
      question: "Explain the concept of virtual DOM in React and how it improves performance.",
      score: 18,
      maxScore: 20,
    },
    { question: "What are the key differences between SQL and NoSQL databases?", score: 17, maxScore: 20 },
    { question: "Describe the working of HTTP protocol and its main request methods.", score: 16, maxScore: 20 },
    { question: "Explain the concept of time complexity in algorithms and give examples.", score: 15, maxScore: 20 },
    {
      question: "What is the difference between supervised and unsupervised learning in machine learning?",
      score: 19,
      maxScore: 20,
    },
  ],
}

export default function Results() {
  const { studentName, studentId, totalScore, maxScore, feedback, questionScores } = mockResults
  const scorePercentage = (totalScore / maxScore) * 100

  // Determine grade based on score percentage
  const getGrade = (percentage: number) => {
    if (percentage >= 90) return { letter: "A", color: "text-green-500" }
    if (percentage >= 80) return { letter: "B", color: "text-blue-500" }
    if (percentage >= 70) return { letter: "C", color: "text-yellow-500" }
    if (percentage >= 60) return { letter: "D", color: "text-orange-500" }
    return { letter: "F", color: "text-red-500" }
  }

  const grade = getGrade(scorePercentage)

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-3xl w-full">
        <Card className="border-2 shadow-lg">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <Award className="h-8 w-8 text-primary" />
            </div>
            <CardTitle className="text-2xl">Exam Results</CardTitle>
            <CardDescription>
              {studentName} ({studentId})
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-center">
              <div className="flex justify-center items-baseline space-x-2">
                <span className="text-4xl font-bold">{totalScore}</span>
                <span className="text-muted-foreground">/ {maxScore}</span>
                <span className={`text-2xl font-bold ml-4 ${grade.color}`}>Grade: {grade.letter}</span>
              </div>
              <Progress value={scorePercentage} className="h-2 mt-2" />
            </div>

            <div className="space-y-2">
              <h3 className="font-medium">Overall Feedback:</h3>
              <p className="bg-muted p-4 rounded-lg">{feedback}</p>
            </div>

            <Separator />

            <div className="space-y-4">
              <h3 className="font-medium">Question Breakdown:</h3>
              {questionScores.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-baseline">
                    <p className="text-sm font-medium">Question {index + 1}</p>
                    <p className="text-sm">
                      {item.score} / {item.maxScore}
                    </p>
                  </div>
                  <p className="text-sm text-muted-foreground">{item.question}</p>
                  <Progress value={(item.score / item.maxScore) * 100} className="h-1" />
                </div>
              ))}
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline" asChild>
              <Link href="/">
                <Home className="mr-2 h-4 w-4" /> Home
              </Link>
            </Button>
            <Button>
              <Download className="mr-2 h-4 w-4" /> Download Results
            </Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  )
}

