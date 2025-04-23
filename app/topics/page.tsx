// app/topics/page.tsx
"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { ArrowLeft, ArrowRight, ChevronDown, ChevronRight } from 'lucide-react'
import Link from "next/link"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from 'lucide-react'

// Define the data structure types
interface QuestionBank {
  Units: Unit[]
}

interface Unit {
  "Unit Number": string
  "Unit Name": string
  Topics: {
    [topicName: string]: string[]
  }
}

export default function Topics() {
  const router = useRouter()
  
  // State for question bank data
  const [questionBankData, setQuestionBankData] = useState<QuestionBank | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)
  
  // State for expanded units
  const [expandedUnits, setExpandedUnits] = useState<Record<string, boolean>>({})
  
  // State for selected topics grouped by unit
  const [selectedTopicsByUnit, setSelectedTopicsByUnit] = useState<Record<string, string[]>>({})
  
  // State for selected units
  const [selectedUnits, setSelectedUnits] = useState<string[]>([])
  
  // Derived state: flat list of all selected topics
  const [allSelectedTopics, setAllSelectedTopics] = useState<string[]>([])
  
  // Student Session_id from localStorage 
  const [sessionId, setSessionId] = useState<string | null>(null)

  // Fetch session_id from localStorage
  useEffect(() => {
    const session_id = localStorage.getItem("session_id")
    if (!session_id) {
      setError("Session ID not found. Please log in again.")
      return
    }
    setSessionId(session_id)
  }, [])

  
  // Fetch question bank data from backend
  useEffect(() => {
    const fetchQuestionBank = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/question-bank`)
        
        if (!response.ok) {
          throw new Error(`Error fetching question bank: ${response.status}`)
        }
        
        const data = await response.json()
        setQuestionBankData(data)
        
        // Initialize expanded state for all units
        const initialExpandedState: Record<string, boolean> = {}
        data.Units.forEach((unit: Unit) => {
          initialExpandedState[unit["Unit Name"]] = false
        })
        setExpandedUnits(initialExpandedState)
        
        setLoading(false)
      } catch (err) {
        console.error("Error fetching question bank:", err)
        setError(err instanceof Error ? err.message : "An unknown error occurred")
        setLoading(false)
      }
    }
    
    fetchQuestionBank()
  }, [])
  
  // Update allSelectedTopics whenever selectedTopicsByUnit changes
  useEffect(() => {
    const allTopics: string[] = []
    Object.values(selectedTopicsByUnit).forEach(topics => {
      topics.forEach(topic => {
        if (!allTopics.includes(topic)) {
          allTopics.push(topic)
        }
      })
    })
    setAllSelectedTopics(allTopics)
  }, [selectedTopicsByUnit])
  
  // Toggle unit expansion
  const toggleUnitExpansion = (unitName: string) => {
    setExpandedUnits(prev => ({
      ...prev,
      [unitName]: !prev[unitName]
    }))
  }
  
  // Toggle unit selection
  const toggleUnitSelection = (unitName: string) => {
    if (!questionBankData) return
    
    const unit = questionBankData.Units.find(u => u["Unit Name"] === unitName)
    if (!unit) return
    
    const isSelected = selectedUnits.includes(unitName)
    
    if (isSelected) {
      // Deselect unit and all its topics
      setSelectedUnits(prev => prev.filter(u => u !== unitName))
      setSelectedTopicsByUnit(prev => {
        const newState = { ...prev }
        delete newState[unitName]
        return newState
      })
    } else {
      // Select unit and all its topics
      setSelectedUnits(prev => [...prev, unitName])
      
      // Get all topics for this unit
      const topicNames = Object.keys(unit.Topics)
      
      setSelectedTopicsByUnit(prev => ({
        ...prev,
        [unitName]: topicNames
      }))
      
      // Ensure the unit is expanded when selected
      setExpandedUnits(prev => ({
        ...prev,
        [unitName]: true
      }))
    }
  }
  
  // Toggle topic selection
  const toggleTopicSelection = (unitName: string, topicName: string) => {
    const unitTopics = selectedTopicsByUnit[unitName] || []
    const isTopicSelected = unitTopics.includes(topicName)
    
    if (isTopicSelected) {
      // Deselect topic
      const updatedTopics = unitTopics.filter(t => t !== topicName)
      
      if (updatedTopics.length === 0) {
        // If no topics remain selected, deselect the unit too
        setSelectedUnits(prev => prev.filter(u => u !== unitName))
        
        setSelectedTopicsByUnit(prev => {
          const newState = { ...prev }
          delete newState[unitName]
          return newState
        })
      } else {
        // Otherwise just update the topics for this unit
        setSelectedTopicsByUnit(prev => ({
          ...prev,
          [unitName]: updatedTopics
        }))
      }
    } else {
      // Select topic
      const updatedTopics = [...unitTopics, topicName]
      
      // If this is the first topic selected for this unit, also select the unit
      if (unitTopics.length === 0) {
        setSelectedUnits(prev => [...prev, unitName])
      }
      
      setSelectedTopicsByUnit(prev => ({
        ...prev,
        [unitName]: updatedTopics
      }))
    }
  }
  
  // Check if all topics in a unit are selected
  const areAllTopicsSelected = (unitName: string) => {
    if (!questionBankData) return false
    
    const unit = questionBankData.Units.find(u => u["Unit Name"] === unitName)
    if (!unit) return false
    
    const allTopics = Object.keys(unit.Topics)
    const selectedTopics = selectedTopicsByUnit[unitName] || []
    
    return allTopics.length === selectedTopics.length && 
           allTopics.every(topic => selectedTopics.includes(topic))
  }
  
  // Save selected topics to backend
  const saveSelectedTopics = async () => {
    if (!sessionId) {
      setError("Student information not found. Please go back to login.")
      return false
    }
    
    try {
      setSubmitting(true)
      
      // Create the data to send to the backend in the requested format
      // {Unit_name: [topics_selected,...], ...}
      const topicsData = {
        sessionId: sessionId,
        selected_topics: selectedTopicsByUnit  // This is already in the format {Unit_name: [topics_selected,...], ...}
      }
      
      // Send the data to the backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/save-topics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(topicsData),
      })
      
      if (!response.ok) {
        throw new Error(`Error saving topics: ${response.status}`)
      }
      
      const result = await response.json()
      
      // Store session ID for the exam page
      if (result.session_id) {
        localStorage.setItem("sessionId", result.session_id)
      }
      
      // Also store in localStorage as a backup
      localStorage.setItem("selectedTopics", JSON.stringify(allSelectedTopics))
      localStorage.setItem("selectedTopicsByUnit", JSON.stringify(selectedTopicsByUnit))
      
      setSubmitting(false)
      return true
    } catch (err) {
      console.error("Error saving topics:", err)
      setError(err instanceof Error ? err.message : "An unknown error occurred")
      setSubmitting(false)
      return false
    }
  }
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (allSelectedTopics.length === 0) {
      alert("Please select at least one topic")
      return
    }
    
    const success = await saveSelectedTopics()
    
    if (success) {
      // Navigate to the exam page
      router.push("/exam")
    }
  }

  // Loading state
  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="max-w-2xl w-full text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading topics...</p>
        </div>
      </main>
    )
  }

  // Error state
  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="max-w-2xl w-full">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              {error}
              <div className="mt-2">
                <Button variant="outline" asChild>
                  <Link href="/login">
                    <ArrowLeft className="mr-2 h-4 w-4" /> Back to Login
                  </Link>
                </Button>
              </div>
            </AlertDescription>
          </Alert>
        </div>
      </main>
    )
  }

  // No data state
  if (!questionBankData || !questionBankData.Units || questionBankData.Units.length === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="max-w-2xl w-full">
          <Alert>
            <AlertTitle>No Topics Available</AlertTitle>
            <AlertDescription>
              No topics are currently available. Please try again later or contact support.
              <div className="mt-2">
                <Button variant="outline" asChild>
                  <Link href="/login">
                    <ArrowLeft className="mr-2 h-4 w-4" /> Back to Login
                  </Link>
                </Button>
              </div>
            </AlertDescription>
          </Alert>
        </div>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-2xl w-full">
        <Card className="border-2 shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl">Select Topics</CardTitle>
            <CardDescription>Choose the units and topics you want to be examined on</CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent>
              <div className="space-y-4">
                {questionBankData.Units.map((unit) => (
                  <div key={unit["Unit Number"]} className="border rounded-lg overflow-hidden">
                    <div className="flex items-center p-3 bg-muted/50">
                      <Checkbox 
                        id={`unit-${unit["Unit Number"]}`}
                        checked={selectedUnits.includes(unit["Unit Name"])}
                        onCheckedChange={() => toggleUnitSelection(unit["Unit Name"])}
                        className="mr-2"
                      />
                      <div 
                        className="flex-1 flex items-center cursor-pointer"
                        onClick={() => toggleUnitExpansion(unit["Unit Name"])}
                      >
                        <Label 
                          htmlFor={`unit-${unit["Unit Number"]}`} 
                          className="flex-1 font-medium cursor-pointer"
                        >
                          {unit["Unit Name"]}
                        </Label>
                        <Badge variant="outline" className="ml-2">
                          {Object.keys(unit.Topics).length} topics
                        </Badge>
                        {expandedUnits[unit["Unit Name"]] ? 
                          <ChevronDown className="h-4 w-4 ml-2" /> : 
                          <ChevronRight className="h-4 w-4 ml-2" />
                        }
                      </div>
                    </div>
                    
                    {expandedUnits[unit["Unit Name"]] && (
                      <div className="p-3 pl-10 border-t bg-background space-y-2">
                        {Object.keys(unit.Topics).map((topicName) => (
                          <div key={topicName} className="flex items-center space-x-2">
                            <Checkbox 
                              id={`topic-${unit["Unit Number"]}-${topicName}`}
                              checked={(selectedTopicsByUnit[unit["Unit Name"]] || []).includes(topicName)}
                              onCheckedChange={() => toggleTopicSelection(unit["Unit Name"], topicName)}
                            />
                            <Label 
                              htmlFor={`topic-${unit["Unit Number"]}-${topicName}`}
                              className="cursor-pointer"
                            >
                              {topicName}
                            </Label>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              {allSelectedTopics.length > 0 && (
                <div className="mt-6 p-3 bg-primary/10 rounded-lg">
                  <p className="font-medium mb-2">Selected Topics: {allSelectedTopics.length}</p>
                  <div className="flex flex-wrap gap-2">
                    {allSelectedTopics.map(topic => (
                      <Badge key={topic} variant="secondary">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline" asChild>
                <Link href="/login">
                  <ArrowLeft className="mr-2 h-4 w-4" /> Back
                </Link>
              </Button>
              <Button 
                type="submit" 
                disabled={allSelectedTopics.length === 3 || submitting}
              >
                {submitting ? (
                  <>
                    <div className="animate-spin h-4 w-4 mr-2 border-2 border-current border-t-transparent rounded-full" />
                    Saving...
                  </>
                ) : (
                  <>
                    Start Exam <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </div>
    </main>
  )
}