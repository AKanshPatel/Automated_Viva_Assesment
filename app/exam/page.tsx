// app/exam/page.tsx
"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Play, Pause, ArrowRight, AlertCircle, RefreshCw, BookOpen, HelpCircle } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

// Mock questions for demonstration
const mockQuestions = [
  "Explain the concept of virtual DOM in React and how it improves performance.",
  "What are the key differences between SQL and NoSQL databases?",
  "Describe the working of HTTP protocol and its main request methods.",
  "Explain the concept of time complexity in algorithms and give examples.",
  "What is the difference between supervised and unsupervised learning in machine learning?",
]

export default function Exam() {
  const router = useRouter()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState(mockQuestions[0])
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [timeLeft, setTimeLeft] = useState(60) // 60 seconds per question
  const [answer, setAnswer] = useState("")
  const [showAlert, setShowAlert] = useState(false)
  const [loading, setLoading] = useState(false)
  const [processingAction, setProcessingAction] = useState<string | null>(null)
  const [helperContent, setHelperContent] = useState<string | null>(null)
  
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const streamRef = useRef<MediaStream | null>(null)
  const recordingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Initialize with the first question
  useEffect(() => {
    setCurrentQuestion(mockQuestions[currentQuestionIndex])
  }, [currentQuestionIndex])

  // Auto-start recording after question is played
  useEffect(() => {
    if (audioRef.current) {
      // When audio ends, start recording after a delay
      const handleAudioEnd = () => {
        setIsPlaying(false)
        // Start recording after 3 seconds
        if (recordingTimeoutRef.current) {
          clearTimeout(recordingTimeoutRef.current)
        }
        recordingTimeoutRef.current = setTimeout(() => {
          startRecording()
        }, 3000)
      }
      
      audioRef.current.addEventListener('ended', handleAudioEnd)
      
      return () => {
        if (audioRef.current) {
          audioRef.current.removeEventListener('ended', handleAudioEnd)
        }
      }
    }
  }, [audioRef.current])

  // Timer effect
  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft((prev) => prev - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [timeLeft])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopRecording()
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
      if (recordingTimeoutRef.current) {
        clearTimeout(recordingTimeoutRef.current)
      }
    }
  }, [])

  // Audio playback
  const playQuestion = () => {
    if (audioRef.current) {
      audioRef.current.play()
      setIsPlaying(true)
    }
  }

  const pauseQuestion = () => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }

  // Recording functionality
  const startRecording = async () => {
    try {
      // Stop any existing recording
      stopRecording()
      
      // Clear any helper content
      setHelperContent(null)
      
      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        // Only process the recording if we have data and we're not in the middle of another action
        if (audioChunksRef.current.length > 0 && !processingAction) {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/mp3' })
          
          // For preview (optional)
          if (audioRef.current) {
            const audioUrl = URL.createObjectURL(audioBlob)
            audioRef.current.src = audioUrl
          }
          
          // Mock transcription - in a real app, this would come from the backend
          setAnswer("This is a mock answer that would come from the speech-to-text API.")
        }
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error("Error starting recording:", error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      // Stop all tracks
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }
    }
  }

  // Helper button handlers
  const handleRephrase = async () => {
    try {
      stopRecording() // Stop current recording
      setProcessingAction("rephrase")
      setHelperContent("Getting rephrased question...")
      
      // Mock API call - simulate loading
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock response
      const rephrased = `Could you please explain how the ${
        currentQuestion.includes("virtual DOM") ? "virtual DOM concept works in React and its performance benefits" :
        currentQuestion.includes("SQL") ? "SQL and NoSQL database paradigms differ from each other" :
        currentQuestion.includes("HTTP") ? "HTTP protocol functions and what its primary request methods are" :
        currentQuestion.includes("time complexity") ? "concept of algorithmic time complexity works and provide some examples" :
        "supervised and unsupervised learning approaches differ in machine learning"
      }?`
      
      setCurrentQuestion(rephrased)
      setHelperContent(null)
      setProcessingAction(null)
      
      // Start recording after a delay
      if (recordingTimeoutRef.current) {
        clearTimeout(recordingTimeoutRef.current)
      }
      recordingTimeoutRef.current = setTimeout(() => {
        startRecording()
      }, 3000)
    } catch (error) {
      console.error("Error rephrasing question:", error)
      setHelperContent("Failed to rephrase question. Please try again.")
      setProcessingAction(null)
    }
  }

  const handleTopicContext = async () => {
    try {
      stopRecording() // Stop current recording
      setProcessingAction("context")
      setHelperContent("Getting topic context...")
      
      // Mock API call - simulate loading
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock response based on current question
      const contextMap: {[key: string]: string} = {
        "virtual DOM": "The Virtual DOM is a programming concept where a virtual representation of a UI is kept in memory and synced with the 'real' DOM. It's a pattern implemented by libraries like React for performance optimization.",
        "SQL": "Database systems are categorized primarily as SQL (relational) or NoSQL (non-relational). They differ in data structure, schema flexibility, scaling, and query capabilities.",
        "HTTP": "HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the web. It follows a client-server model with stateless request-response cycles.",
        "time complexity": "Time complexity is a concept in computer science that describes the amount of time an algorithm takes to run as a function of the length of the input. It's typically expressed using Big O notation.",
        "supervised": "Machine learning approaches are broadly categorized as supervised (using labeled data) or unsupervised (finding patterns in unlabeled data). They serve different purposes in data analysis and prediction."
      }
      
      // Find which context to show based on the question
      let contextKey = Object.keys(contextMap).find(key => currentQuestion.toLowerCase().includes(key.toLowerCase())) || "virtual DOM"
      
      setHelperContent(contextMap[contextKey])
      setProcessingAction(null)
      
      // Start recording after a delay
      if (recordingTimeoutRef.current) {
        clearTimeout(recordingTimeoutRef.current)
      }
      recordingTimeoutRef.current = setTimeout(() => {
        startRecording()
      }, 5000) // Give student time to read the context
    } catch (error) {
      console.error("Error getting topic context:", error)
      setHelperContent("Failed to get topic context. Please try again.")
      setProcessingAction(null)
    }
  }

  const handleHint = async () => {
    try {
      stopRecording() // Stop current recording
      setProcessingAction("hint")
      setHelperContent("Getting hint...")
      
      // Mock API call - simulate loading
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock response based on current question
      const hintMap: {[key: string]: string} = {
        "virtual DOM": "Think about how comparing two JavaScript objects is more efficient than directly manipulating the browser's DOM.",
        "SQL": "Consider how data relationships and ACID properties differ between these database types.",
        "HTTP": "Remember the common methods like GET, POST, PUT, DELETE and their intended uses.",
        "time complexity": "Consider how Big O notation represents the worst-case scenario for algorithm performance.",
        "supervised": "Think about the presence or absence of labeled training data as the key differentiator."
      }
      
      // Find which hint to show based on the question
      let hintKey = Object.keys(hintMap).find(key => currentQuestion.toLowerCase().includes(key.toLowerCase())) || "virtual DOM"
      
      setHelperContent(hintMap[hintKey])
      setProcessingAction(null)
      
      // Start recording after a delay
      if (recordingTimeoutRef.current) {
        clearTimeout(recordingTimeoutRef.current)
      }
      recordingTimeoutRef.current = setTimeout(() => {
        startRecording()
      }, 5000) // Give student time to read the hint
    } catch (error) {
      console.error("Error getting hint:", error)
      setHelperContent("Failed to get hint. Please try again.")
      setProcessingAction(null)
    }
  }

  const handleNextQuestion = async () => {
    // Stop any active recording
    stopRecording()
    
    if (audioChunksRef.current.length === 0 && !answer) {
      setShowAlert(true)
      return
    }

    try {
      setLoading(true)
      
      // Mock API call - simulate loading
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      if (currentQuestionIndex >= mockQuestions.length - 1) {
        // Last question - redirect to results
        router.push("/results")
        return
      }
      
      // Move to next question
      setCurrentQuestionIndex(prev => prev + 1)
      setAnswer("")
      setTimeLeft(60)
      setShowAlert(false)
      setHelperContent(null)
      audioChunksRef.current = []
      setLoading(false)
      
      // Auto-play would happen here in a real implementation
    } catch (error) {
      console.error("Error submitting answer:", error)
      setLoading(false)
    }
  }

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
  }

  // Calculate progress
  const progress = ((currentQuestionIndex) / mockQuestions.length) * 100

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading...</p>
        </div>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-3xl w-full">
        <Card className="border-2 shadow-lg">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="text-2xl">Viva Exam</CardTitle>
              <Badge variant="outline" className="text-lg font-mono">
                {formatTime(timeLeft)}
              </Badge>
            </div>
            <CardDescription>
              Question {currentQuestionIndex + 1} of {mockQuestions.length}
            </CardDescription>
            <Progress value={progress} className="h-2" />
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="bg-muted p-4 rounded-lg">
              <h3 className="font-medium mb-2">Question:</h3>
              <p>{currentQuestion}</p>

              <div className="flex items-center mt-4 space-x-2">
                <Button size="sm" variant="outline" onClick={isPlaying ? pauseQuestion : playQuestion}>
                  {isPlaying ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                  {isPlaying ? "Pause" : "Play"} Question
                </Button>
                {/* Using a placeholder audio for demo purposes */}
                <audio 
                  ref={audioRef} 
                  src="/placeholder.mp3" 
                  onEnded={() => setIsPlaying(false)}
                  onPause={() => setIsPlaying(false)}
                />
              </div>
            </div>

            {/* Helper buttons */}
            <div className="flex flex-wrap gap-2">
              <Button 
                size="sm" 
                variant="outline" 
                onClick={handleRephrase}
                disabled={loading || processingAction !== null}
              >
                <RefreshCw className="h-4 w-4 mr-2" /> 
                Rephrase Question
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                onClick={handleTopicContext}
                disabled={loading || processingAction !== null}
              >
                <BookOpen className="h-4 w-4 mr-2" /> 
                Topic Context
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                onClick={handleHint}
                disabled={loading || processingAction !== null}
              >
                <HelpCircle className="h-4 w-4 mr-2" /> 
                Hint
              </Button>
            </div>

            {/* Helper content display */}
            {helperContent && (
              <div className="bg-secondary/30 p-4 rounded-lg">
                <h3 className="font-medium mb-2">
                  {processingAction === "rephrase" ? "Rephrased Question" : 
                   processingAction === "context" ? "Topic Context" : 
                   processingAction === "hint" ? "Hint" : "Additional Information"}:
                </h3>
                <p>{helperContent}</p>
              </div>
            )}

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="font-medium">Your Answer:</h3>
                {isRecording && (
                  <Badge variant="outline" className="animate-pulse">
                    Recording...
                  </Badge>
                )}
              </div>

              {isRecording ? (
                <div className="h-24 bg-muted/50 rounded-lg flex items-center justify-center">
                  <div className="flex items-center space-x-2">
                    <span className="animate-pulse text-primary">●</span>
                    <span>Recording your answer...</span>
                  </div>
                </div>
              ) : answer ? (
                <div className="bg-muted/50 p-4 rounded-lg min-h-24">{answer}</div>
              ) : (
                <div className="h-24 bg-muted/50 rounded-lg flex items-center justify-center text-muted-foreground">
                  {processingAction ? "Processing..." : "Waiting to start recording..."}
                </div>
              )}
            </div>

            {showAlert && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>No answer recorded. Please ensure your microphone is working and try again.</AlertDescription>
              </Alert>
            )}
          </CardContent>
          <CardFooter className="flex justify-end">
            <Button onClick={handleNextQuestion} disabled={loading || processingAction !== null}>
              {currentQuestionIndex < mockQuestions.length - 1 ? (
                <>
                  Next Question <ArrowRight className="ml-2 h-4 w-4" />
                </>
              ) : (
                <>
                  Finish Exam <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  )
}