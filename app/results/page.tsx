"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Home, Download, Award, AlertCircle } from "lucide-react"
import Link from "next/link"
import { useState, useEffect } from "react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

// Define interfaces to match the backend models
interface AnswerResult {
    question_no: number;
    question_text: string;
    answer_text?: string;
    correct_answer?: string; // Added correct_answer
    score: number;
    max_score: number;
}

interface ExamResult {
    student_name: string;
    roll_number: string;
    student_id: string;
    session_id: string;
    answers: AnswerResult[];
    total_score: number;
    max_score: number;
}

export default function Results() {
    const [resultsData, setResultsData] = useState<ExamResult | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [sessionId, setSessionId] = useState<string | null>(null);

    useEffect(() => {
        // First, get the session ID from localStorage
        const storedSessionId = localStorage.getItem("sessionId") || localStorage.getItem("session_id");
        setSessionId(storedSessionId);

        if (!storedSessionId) {
            setError("Session ID not found. Please complete an exam first.");
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                console.log(`Fetching results with session ID: ${storedSessionId}`);

                // Use the correct API URL
                const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/results`;
                console.log(`API URL: ${apiUrl}`);

                const response = await fetch(`${apiUrl}?session_id=${storedSessionId}`, {
                    method: "GET",
                    headers: {
                        Accept: "application/json",
                    },
                });

                console.log(`Response status: ${response.status}`);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error(`Error response: ${errorText}`);
                    throw new Error(`Error fetching results: ${response.status} - ${errorText}`);
                }

                const data = await response.json();
                console.log("Results data received:", data);

                setResultsData(data);
                setLoading(false);
            } catch (e: any) {
                console.error("Error fetching results:", e);
                setError(e.message || "An error occurred while fetching your results");
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const getGrade = (percentage: number) => {
        if (percentage >= 80) return { letter: "A", color: "text-green-500" };
        if (percentage >= 70) return { letter: "B", color: "text-blue-500" };
        if (percentage >= 60) return { letter: "C", color: "text-yellow-500" };
        if (percentage >= 50) return { letter: "D", color: "text-orange-500" };
        return { letter: "F", color: "text-red-500" };
    };

    // For debugging - show session ID in error state
    if (loading) {
        return (
            <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p>Loading your results...</p>
                    {sessionId && <p className="text-sm text-muted-foreground mt-2">Session ID: {sessionId}</p>}
                </div>
            </main>
        );
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
                            {sessionId && <p className="text-sm mt-2">Session ID: {sessionId}</p>}
                            <div className="mt-4">
                                <Button variant="outline" asChild>
                                    <Link href="/">Go back to home</Link>
                                </Button>
                            </div>
                        </AlertDescription>
                    </Alert>
                </div>
            </main>
        );
    }

    if (!resultsData) {
        return (
            <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-secondary/20">
                <div className="max-w-md w-full">
                    <Alert>
                        <AlertTitle>No Results Available</AlertTitle>
                        <AlertDescription>
                            No exam results are currently available. Please complete an exam first.
                            {sessionId && <p className="text-sm mt-2">Session ID: {sessionId}</p>}
                            <div className="mt-4">
                                <Button variant="outline" asChild>
                                    <Link href="/">Go back to home</Link>
                                </Button>
                            </div>
                        </AlertDescription>
                    </Alert>
                </div>
            </main>
        );
    }

    const { student_name, roll_number, total_score, max_score, answers } = resultsData;
    const scorePercentage = max_score > 0 ? (total_score / max_score) * 100 : 0;
    const grade = getGrade(scorePercentage);

    // Function to handle downloading results as JSON
    const handleDownloadResults = () => {
        // Create a JSON string of the results
        const resultsJson = JSON.stringify(resultsData, null, 2);

        // Create a blob with the data
        const blob = new Blob([resultsJson], { type: "application/json" });

        // Create a URL for the blob
        const url = URL.createObjectURL(blob);

        // Create a temporary anchor element and trigger download
        const a = document.createElement("a");
        a.href = url;
        a.download = `exam_results_${roll_number}.json`;
        document.body.appendChild(a);
        a.click();

        // Clean up
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

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
                            {student_name} ({roll_number})
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="text-center">
                            <div className="flex justify-center items-baseline space-x-2">
                                <span className="text-4xl font-bold">{total_score}</span>
                                <span className="text-muted-foreground">/ {max_score}</span>
                                <span className={`text-2xl font-bold ml-4 ${grade.color}`}>Grade: {grade.letter}</span>
                            </div>
                            <Progress value={scorePercentage} className="h-2 mt-2" />
                        </div>

                        <Separator />

                        <div className="space-y-4">
                            <h3 className="font-medium">Question Breakdown:</h3>
                            {answers && answers.length > 0 ? (
                                answers.map((answer, index) => (
                                    <div key={index} className="space-y-2 border rounded-md p-4">
                                        <div className="flex justify-between items-baseline">
                                            <p className="text-sm font-medium">Question {answer.question_no}</p>
                                            <p className="text-sm">
                                                {answer.score} / {answer.max_score}
                                            </p>
                                        </div>
                                        <p className="text-sm text-muted-foreground mb-2">{answer.question_text}</p>
                                        <Progress value={(answer.score / answer.max_score) * 100} className="h-1 mb-2" />
                                        {answer.answer_text && (
                                            <p className="text-xs text-blue-500">Your Answer: {answer.answer_text}</p>
                                        )}
                                        {answer.correct_answer && ( // Display correct answer
                                            <p className="text-xs text-green-500">Correct Answer: {answer.correct_answer}</p>
                                        )}
                                    </div>
                                ))
                            ) : (
                                <p className="text-muted-foreground">No question data available.</p>
                            )}
                        </div>
                    </CardContent>
                    <CardFooter className="flex justify-between">
                        <Button variant="outline" asChild>
                            <Link href="/">
                                <Home className="mr-2 h-4 w-4" /> Home
                            </Link>
                        </Button>
                        <Button onClick={handleDownloadResults}>
                            <Download className="mr-2 h-4 w-4" /> Download Results
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </main>
    );
}
