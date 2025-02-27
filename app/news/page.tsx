"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Volume2 } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import NewsCarousel from "@/components/news-carousel"

interface NewsArticle {
  title: string
  description: string
  url: string
  urlToImage: string
  publishedAt: string
  source: {
    name: string
  }
}

const categories = ["Technology", "Environment", "Business", "Science"]

export default function NewsPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [activeTab, setActiveTab] = useState("all")
  const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchNews()
  }, [activeTab, searchQuery]) // Updated dependency array

  const fetchNews = async () => {
    setIsLoading(true)
    try {
      const category = activeTab !== "all" ? `&category=${activeTab.toLowerCase()}` : ""
      const response = await fetch(`/api/news?q=${searchQuery}${category}`)
      const data = await response.json()
      setNewsArticles(data.articles)
    } catch (error) {
      console.error("Error fetching news:", error)
    }
    setIsLoading(false)
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchNews()
  }

  const speakHeadline = (headline: string) => {
    const utterance = new SpeechSynthesisUtterance(headline)
    window.speechSynthesis.speak(utterance)
  }

  return (
    <div className="container py-8">
      <div className="mb-8 space-y-4">
        <h1 className="text-3xl font-bold">News Aggregator</h1>
        <p className="text-muted-foreground">Stay updated with the latest news from various categories.</p>

        <form onSubmit={handleSearch} className="flex w-full max-w-sm items-center space-x-2">
          <Input
            type="text"
            placeholder="Search news..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full"
          />
          <Button type="submit" size="icon">
            <Search className="h-4 w-4" />
            <span className="sr-only">Search</span>
          </Button>
        </form>
      </div>

      <NewsCarousel articles={newsArticles.slice(0, 5)} onSpeak={speakHeadline} />

      <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab} className="w-full mt-8">
        <TabsList className="mb-6">
          <TabsTrigger value="all">All</TabsTrigger>
          {categories.map((category) => (
            <TabsTrigger key={category} value={category}>
              {category}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value={activeTab} className="mt-0">
          {isLoading ? (
            <div className="text-center">Loading...</div>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {newsArticles.map((article, index) => (
                <Card key={index} className="overflow-hidden">
                  <div className="aspect-video w-full overflow-hidden">
                    <Image
                      src={article.urlToImage || "/placeholder.svg"}
                      alt={article.title}
                      width={300}
                      height={200}
                      className="h-full w-full object-cover transition-all hover:scale-105"
                    />
                  </div>
                  <CardHeader>
                    <CardTitle className="line-clamp-2">{article.title}</CardTitle>
                    <CardDescription className="line-clamp-3">{article.description}</CardDescription>
                  </CardHeader>
                  <CardFooter className="flex justify-between">
                    <Button asChild>
                      <Link href={`/news/${encodeURIComponent(article.title)}`}>Read More</Link>
                    </Button>
                    <Button variant="outline" size="icon" onClick={() => speakHeadline(article.title)}>
                      <Volume2 className="h-4 w-4" />
                      <span className="sr-only">Read aloud</span>
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

