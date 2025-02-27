"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Play, Rewind, FastForward, Pause, Terminal, Bug, Lightbulb } from "lucide-react"

export default function CodePage() {
  const [codeInput, setCodeInput] = useState(`function calculateSum(a, b) {
  return a + b;
}

// This function has a bug
function multiplyNumbers(a, b) {
  return a + b; // Should be a * b
}

const result = multiplyNumbers(5, 3);
console.log("Result:", result); // Outputs 8 instead of 15
`)

  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)
  const [currentStep, setCurrentStep] = useState(0)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [displayCode, setDisplayCode] = useState("")
  const [isFlickering, setIsFlickering] = useState(false)

  const codeLines = codeInput.split("\n")
  const totalSteps = codeLines.length

  const terminalRef = useRef<HTMLDivElement>(null)

  // Mock AI suggestions based on code content
  const generateSuggestions = () => {
    if (codeInput.includes("a + b") && codeInput.includes("multiplyNumbers")) {
      return [
        "Line 6: In function 'multiplyNumbers', you're using addition (+) instead of multiplication (*)",
        "Consider using proper variable names to avoid confusion",
        "Add input validation to handle edge cases",
      ]
    }

    return [
      "No specific issues found in your code",
      "Consider adding comments to explain complex logic",
      "Make sure to handle potential errors",
    ]
  }

  // Simulate code playback
  useEffect(() => {
    if (!isPlaying || currentStep >= totalSteps) return

    const timer = setTimeout(() => {
      setCurrentStep((prev) => {
        const next = prev + 1
        if (next >= totalSteps) {
          setIsPlaying(false)
          setSuggestions(generateSuggestions())
          return totalSteps
        }
        return next
      })
    }, 500 / playbackSpeed)

    return () => clearTimeout(timer)
  }, [isPlaying, currentStep, totalSteps, playbackSpeed])

  // Update display code based on current step
  useEffect(() => {
    setDisplayCode(codeLines.slice(0, currentStep).join("\n"))
  }, [currentStep, codeLines])

  // Scroll terminal to bottom when content changes
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [terminalRef])

  // CRT flicker effect
  useEffect(() => {
    const flickerInterval = setInterval(() => {
      setIsFlickering((prev) => !prev)
    }, 2000)

    return () => clearInterval(flickerInterval)
  }, [])

  const handleDebugNow = () => {
    setCurrentStep(0)
    setIsPlaying(true)
    setSuggestions([])
  }

  const handleRewind = () => {
    setCurrentStep(0)
    setIsPlaying(false)
  }

  const handlePlayPause = () => {
    if (currentStep >= totalSteps) {
      setCurrentStep(0)
    }
    setIsPlaying(!isPlaying)
  }

  const handleFastForward = () => {
    setCurrentStep(totalSteps)
    setIsPlaying(false)
    setSuggestions(generateSuggestions())
  }

  return (
    <div className="container py-8">
      <div className="mb-8 space-y-4">
        <h1 className="text-3xl font-bold">YourCode - Bug Tracking Time Machine</h1>
        <p className="text-muted-foreground">
          Travel back in time to debug your code with our retro CRT-style interface.
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Input Your Code</h2>
          <Textarea
            value={codeInput}
            onChange={(e) => setCodeInput(e.target.value)}
            className="font-mono h-[400px]"
            placeholder="Paste your code here..."
          />
          <Button onClick={handleDebugNow} className="w-full">
            <Bug className="mr-2 h-4 w-4" />
            Debug Now
          </Button>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-bold">Time Machine Playback</h2>

          <div className={`crt-container p-4 h-[400px] ${isFlickering ? "crt-flicker" : ""}`}>
            <div className="crt-scan"></div>
            <div ref={terminalRef} className="crt-text font-mono text-sm h-full overflow-auto whitespace-pre">
              <div className="flex items-center mb-2">
                <Terminal className="mr-2 h-4 w-4 crt-text" />
                <span className="crt-glow">YourCode Terminal v1.0</span>
              </div>
              <div className="mb-4">
                <span className="crt-text">{">"} Loading code...</span>
              </div>
              {displayCode}
              <span className="crt-blink">_</span>
            </div>
          </div>

          <div className="flex justify-between items-center">
            <div className="flex space-x-2">
              <Button variant="outline" size="icon" onClick={handleRewind}>
                <Rewind className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" onClick={handlePlayPause}>
                {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </Button>
              <Button variant="outline" size="icon" onClick={handleFastForward}>
                <FastForward className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex items-center space-x-2">
              <span className="text-sm">Speed:</span>
              <select
                value={playbackSpeed}
                onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
                className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm"
              >
                <option value={0.5}>0.5x</option>
                <option value={1}>1x</option>
                <option value={2}>2x</option>
                <option value={4}>4x</option>
              </select>
            </div>
          </div>

          {suggestions.length > 0 && (
            <div className="mt-4 p-4 border rounded-md bg-muted/50">
              <h3 className="font-medium flex items-center mb-2">
                <Lightbulb className="mr-2 h-4 w-4 text-yellow-500" />
                AI Suggestions
              </h3>
              <ul className="space-y-2">
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    className="text-sm time-machine-playback"
                    style={{ animationDelay: `${index * 0.5}s` }}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

