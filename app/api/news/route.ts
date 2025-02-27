import { NextResponse } from "next/server"

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const query = searchParams.get("q") || ""
  const category = searchParams.get("category") || ""

  const apiKey = process.env.NEWS_API_KEY
  const baseUrl = "https://newsapi.org/v2/top-headlines"
  const country = "us"

  let url = `${baseUrl}?country=${country}&apiKey=${apiKey}`

  if (query) {
    url += `&q=${query}`
  }

  if (category) {
    url += `&category=${category}`
  }

  try {
    const response = await fetch(url)
    const data = await response.json()

    return NextResponse.json(data)
  } catch (error) {
    console.error("Error fetching news:", error)
    return NextResponse.json({ error: "Failed to fetch news" }, { status: 500 })
  }
}

