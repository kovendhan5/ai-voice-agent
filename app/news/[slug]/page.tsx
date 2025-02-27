import { notFound } from "next/navigation"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import Link from "next/link"

async function getArticle(slug: string) {
  const apiKey = process.env.NEWS_API_KEY
  const response = await fetch(`https://newsapi.org/v2/everything?q=${slug}&apiKey=${apiKey}`)
  const data = await response.json()
  return data.articles[0]
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const article = await getArticle(params.slug)

  if (!article) {
    notFound()
  }

  return (
    <div className="container py-8">
      <Button asChild className="mb-4">
        <Link href="/news">← Back to News</Link>
      </Button>
      <article className="prose lg:prose-xl mx-auto">
        <h1>{article.title}</h1>
        {article.urlToImage && (
          <Image
            src={article.urlToImage || "/placeholder.svg"}
            alt={article.title}
            width={800}
            height={400}
            className="rounded-lg object-cover"
          />
        )}
        <p className="text-muted-foreground">
          Published on {new Date(article.publishedAt).toLocaleDateString()} by {article.source.name}
        </p>
        <p>{article.description}</p>
        <p>{article.content}</p>
        <Button asChild>
          <a href={article.url} target="_blank" rel="noopener noreferrer">
            Read Full Article
          </a>
        </Button>
      </article>
    </div>
  )
}

