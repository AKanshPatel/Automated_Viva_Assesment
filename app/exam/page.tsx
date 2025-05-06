"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Play, Pause, ArrowRight, AlertCircle, RefreshCw, BookOpen, HelpCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function Exam() {
  const router = useRouter()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState(""); // This will hold the audio URL
  const [questionText, setQuestionText] = useState("");     // This will hold the question text
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [timeLeft, setTimeLeft] = useState(60) // 60 seconds per question
  const [answer, setAnswer] = useState("")
  const [showAlert, setShowAlert] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [processingAction, setProcessingAction] = useState<string | null>(null)
  const [helperContent, setHelperContent] = useState<string | null>(null)
  const [totalQuestions, setTotalQuestions] = useState(0)
  const [session_id, setsession_id] = useState<string | null>(null)

  const audioRef = useRef<HTMLAudioElement | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const streamRef = useRef<MediaStream | null>(null)
  const recordingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Get session ID from localStorage
  useEffect(() => {
    const storedsession_id = localStorage.getItem("session_id")
    if (storedsession_id) {
      setsession_id(storedsession_id)
    } else {
      console.error("No session ID found in localStorage")
      setError("Session not found. Please go back and select topics again.")
    }
  }, [])

  // Fetch question from backend when currentQuestionIndex changes or on initial load
  useEffect(() => {
    if (audioRef.current && currentQuestion) {
      // Assuming 'currentQuestion' now holds the audio URL correctly
      audioRef.current.src = currentQuestion // Use currentQuestion which should be data.audioUrl
    }
  }, [audioRef.current, currentQuestion]) // Depend on audioRef.current and currentQuestion

 // Fetch question from backend
useEffect(() => {
  if (!session_id) return;

  const fetchQuestion = async () => {
    try {
      setLoading(true);
      setError(null);

      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/questions`;
      const response = await fetch(`${apiUrl}?session_id=${session_id}&question_index=${currentQuestionIndex + 1}`);

      if (!response.ok) {
        throw new Error(`Error fetching question: ${response.status}`);
      }

      const data = await response.json();

      setCurrentQuestion(data.audioUrl);       // Holds the audio URL
      setQuestionText(data.questionText);   // Holds the question text

      if (data.totalQuestions) {
        setTotalQuestions(data.totalQuestions);
      }

      setLoading(false);
    } catch (err) {
      console.error("Error fetching question:", err);
      setError(err instanceof Error ? err.message : "An unknown error occurred");
      setLoading(false);
    }
  };

  fetchQuestion();
}, [currentQuestionIndex, session_id]);

// Set audio source and attempt to play when audioRef.current and currentQuestion are available
useEffect(() => {
  if (audioRef.current && currentQuestion) {
    audioRef.current.src = currentQuestion;
    console.log("Audio source URL set (useEffect):", currentQuestion);
    audioRef.current.play()
      .then(() => {
        setIsPlaying(true);
      })
      .catch(error => {
        console.error("Autoplay prevented or error during play:", error);
        // Optionally, inform the user to click play.
      });
  }
}, [audioRef.current, currentQuestion]);

// Set audio source and attempt to play when audioRef.current and currentQuestion are available
useEffect(() => {
  if (audioRef.current && currentQuestion) {
    audioRef.current.src = currentQuestion;
    console.log("Audio source URL set (useEffect):", currentQuestion);
    audioRef.current.play()
      .then(() => {
        setIsPlaying(true);
      })
      .catch(error => {
        console.error("Autoplay prevented or error during play:", error);
        // Optionally, inform the user to click play.
      });
  }
}, [audioRef.current, currentQuestion]);

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

      audioRef.current.addEventListener("ended", handleAudioEnd)

      return () => {
        if (audioRef.current) {
          audioRef.current.removeEventListener("ended", handleAudioEnd)
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
        streamRef.current.getTracks().forEach((track) => track.stop())
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
    console.log("startRecording called...");
    try {
      stopRecording(); // Ensure any previous recording is stopped
      setHelperContent(null);
      console.log("Existing recording stopped.");
  
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      console.log("User media stream obtained:", stream);
      stream.getAudioTracks().forEach(track => console.log("Audio track enabled:", track.enabled));
  
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
  
      mediaRecorder.ondataavailable = (event) => {
        console.log("ondataavailable event fired. Data size:", event.data.size);
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
          console.log("Audio chunk added. Total chunks:", audioChunksRef.current.length);
        }
      };

      mediaRecorder.onstop = async () => {
        console.log("Recording stopped. Processing audio chunks:", audioChunksRef.current.length);
        if (audioChunksRef.current.length > 0 && !processingAction) {
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp3" });
          console.log("Final audio Blob created. Size:", audioBlob.size, "Type:", audioBlob.type);         
          try {
            // Send the audio to the backend for transcription
            const formData = new FormData()
            formData.append("audio", audioBlob, `question_${currentQuestionIndex + 1}.mp3`)
            formData.append("session_id", session_id || "")
            // TODO : Send question text 
            formData.append("question_text", currentQuestion)

            const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/transcribe`
            const response = await fetch(apiUrl, {
              method: "POST",
              body: formData,
            })

            if (!response.ok) {
              throw new Error(`Error transcribing audio: ${response.status}`)
            }

            const data = await response.json()
            setAnswer(data.transcription)
          } catch (error) {
            console.error("Error transcribing audio:", error)
            setAnswer("Error transcribing your answer. The audio has been recorded and will be processed.")
          }
        }
      }

      mediaRecorder.start();
      setIsRecording(true);
      console.log("Recording started successfully. MediaRecorder state:", mediaRecorderRef.current?.state);
  
    } catch (error: any) {
      console.error("Error starting recording:", error);
      setError("Could not access microphone. Please check your browser permissions.");
      console.error("Error details:", error?.name, error?.message, error?.constraint);
    }
  };
  
  const stopRecording = () => {
    console.log("stopRecording called...");
    if (mediaRecorderRef.current && isRecording) {
      console.log("Stopping recording. MediaRecorder state before stop:", mediaRecorderRef.current?.state);
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log("MediaRecorder stopped.");
  
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        console.log("Audio tracks stopped and streamRef reset.");
      }
    } else {
      console.log("No active recording to stop.");
    }
  };
  // Helper button handlers
  const handleRephrase = async () => {
    if (!session_id) return

    try {
      stopRecording() // Stop current recording
      setProcessingAction("rephrase")
      setHelperContent("Getting rephrased question...")

      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/rephrase`
      const response = await fetch(`${apiUrl}?session_id=${session_id}&question_index=${currentQuestionIndex + 1}`)

      if (!response.ok) {
        throw new Error(`Error rephrasing question: ${response.status}`)
      }

      const data = await response.json()
      setCurrentQuestion(data.rephrased)
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
    if (!session_id) return

    try {
      stopRecording() // Stop current recording
      setProcessingAction("context")
      setHelperContent("Getting topic context...")

      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/context`
      const response = await fetch(`${apiUrl}?session_id=${session_id}&question_index=${currentQuestionIndex + 1}`)

      if (!response.ok) {
        throw new Error(`Error getting topic context: ${response.status}`)
      }

      const data = await response.json()
      setHelperContent(data.context)
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
    if (!session_id) return

    try {
      stopRecording() // Stop current recording
      setProcessingAction("hint")
      setHelperContent("Getting hint...")

      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/hint`
      const response = await fetch(`${apiUrl}?session_id=${session_id}&question_index=${currentQuestionIndex + 1}`)

      if (!response.ok) {
        throw new Error(`Error getting hint: ${response.status}`)
      }

      const data = await response.json()
      setHelperContent(data.hint)
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
    if (!session_id) return

    // Stop any active recording
    stopRecording()

    if (audioChunksRef.current.length === 0 && !answer) {
      setShowAlert(true)
      return
    }

    try {
      setLoading(true)

      // Create FormData with the audio recording
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp3" })
      const formData = new FormData()
      formData.append("audio", audioBlob, `question_${currentQuestionIndex + 1}.mp3`)
      formData.append("session_id", session_id)
      // TODO Handle the Zero index
      formData.append("question_index", currentQuestionIndex.toString())
      formData.append("question_text", currentQuestion)
      // formData.append("answer_text", answer)

      // Submit the answer to the backend
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/submit-answer`
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Error submitting answer: ${response.status}`)
      }

      const data = await response.json()

      // Check if this was the last question
      if (data.isLastQuestion || (totalQuestions > 0 && currentQuestionIndex >= totalQuestions)) {
        // Last question - redirect to results
        router.push("/results")
        return
      }

      // Move to next question
      setCurrentQuestionIndex((prev) => prev + 1)
      setAnswer("")
      setTimeLeft(60)
      setShowAlert(false)
      setHelperContent(null)
      audioChunksRef.current = []
    } catch (error) {
      console.error("Error submitting answer:", error)
      setError("Failed to submit your answer. Please try again.")
    } finally {
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
  const progress = totalQuestions > 0 ? (currentQuestionIndex / totalQuestions) * 100 : 0

  if (loading && currentQuestionIndex === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading your exam...</p>
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
        <div className="max-w-md w-full">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              {error}
              <div className="mt-4">
                <Button variant="outline" asChild>
                  <a href="/topics">Go back to topic selection</a>
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
              Question {currentQuestionIndex + 1} {totalQuestions > 0 ? `of ${totalQuestions}` : ""}
            </CardDescription>
            <Progress value={progress} className="h-2" />
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="bg-muted p-4 rounded-lg">
              <h3 className="font-medium mb-2">Question:</h3>
              <p>{questionText}</p>

              <div className="flex items-center mt-4 space-x-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={isPlaying ? pauseQuestion : playQuestion}
                  disabled={loading}
                >
                  {isPlaying ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                  {isPlaying ? "Pause" : "Play"} Question
                </Button>
                <audio
                  ref={audioRef}
                  onEnded={() => setIsPlaying(false)}
                  onPause={() => setIsPlaying(false)}
                  autoPlay
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
              <Button size="sm" variant="outline" onClick={handleHint} disabled={loading || processingAction !== null}>
                <HelpCircle className="h-4 w-4 mr-2" />
                Hint
              </Button>
            </div>

            {/* Helper content display */}
            {helperContent && (
              <div className="bg-secondary/30 p-4 rounded-lg">
                <h3 className="font-medium mb-2">
                  {processingAction === "rephrase"
                    ? "Rephrased Question"
                    : processingAction === "context"
                      ? "Topic Context"
                      : processingAction === "hint"
                        ? "Hint"
                        : "Additional Information"}
                  :
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
                <AlertDescription>
                  No answer recorded. Please ensure your microphone is working and try again.
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
          <CardFooter className="flex justify-end">
            <Button onClick={handleNextQuestion} disabled={loading || processingAction !== null}>
              {loading && (
                <div className="animate-spin h-4 w-4 mr-2 border-2 border-current border-t-transparent rounded-full" />
              )}
              {totalQuestions > 0 && currentQuestionIndex >= totalQuestions - 1 ? (
                <>
                  Finish Exam <ArrowRight className="ml-2 h-4 w-4" />
                </>
              ) : (
                <>
                  Next Question <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  )
}
