"use client"

import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight, Volume2 } from "lucide-react"
import { Button } from "@/components/ui/button"

interface NewsArticle {
  title: string
  description: string
  url: string
}

interface NewsCarouselProps {
  articles: NewsArticle[]
  onSpeak: (headline: string) => void
}

export default function NewsCarousel({ articles, onSpeak }: NewsCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % articles.length)
    }, 5000)

    return () => clearInterval(interval)
  }, [articles.length])

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + articles.length) % articles.length)
  }

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % articles.length)
  }

  if (articles.length === 0) {
    return null
  }

  return (
    <div className="relative overflow-hidden rounded-lg bg-muted p-4">
      <h2 className="mb-2 text-xl font-bold">Today's Headlines</h2>
      <div className="flex items-center justify-between">
        <Button variant="outline" size="icon" onClick={handlePrev}>
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <div className="mx-4 flex-1 text-center">
          <p className="font-medium">{articles[currentIndex].title}</p>
        </div>
        <Button variant="outline" size="icon" onClick={handleNext}>
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
      <div className="mt-2 flex justify-center">
        <Button variant="outline" size="sm" onClick={() => onSpeak(articles[currentIndex].title)}>
          <Volume2 className="mr-2 h-4 w-4" />
          Read Aloud
        </Button>
      </div>
    </div>
  )
}

