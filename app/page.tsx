import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Newspaper, Leaf, Code } from "lucide-react"

export default function Home() {
  return (
    <div className="flex flex-col min-h-[calc(100vh-8rem)]">
      <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-gradient-to-b from-background to-muted">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-4 text-center">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                Welcome to NextGenNode
              </h1>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                Your modern platform for news, carbon footprint tracking, and code debugging.
              </p>
            </div>
            <div className="space-x-4">
              <Link href="/news">
                <Button>Get Started</Button>
              </Link>
              <Link href="#features">
                <Button variant="outline">Learn More</Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="w-full py-12 md:py-24 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Explore Our Features</h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Discover the powerful tools and resources available on NextGenNode.
              </p>
            </div>
          </div>
          <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-3">
            <div className="flex flex-col items-center space-y-4 rounded-lg border p-6 shadow-sm">
              <div className="rounded-full bg-primary/10 p-4">
                <Newspaper className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold">News Aggregator</h3>
              <p className="text-center text-muted-foreground">
                Stay updated with the latest news from various categories, all in one place.
              </p>
              <Link href="/news">
                <Button variant="outline">Browse News</Button>
              </Link>
            </div>
            <div className="flex flex-col items-center space-y-4 rounded-lg border p-6 shadow-sm">
              <div className="rounded-full bg-primary/10 p-4">
                <Leaf className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold">Carbon Footprint</h3>
              <p className="text-center text-muted-foreground">
                Calculate your carbon footprint and get personalized tips to reduce your impact.
              </p>
              <Link href="/carbon">
                <Button variant="outline">Calculate Now</Button>
              </Link>
            </div>
            <div className="flex flex-col items-center space-y-4 rounded-lg border p-6 shadow-sm">
              <div className="rounded-full bg-primary/10 p-4">
                <Code className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold">YourCode</h3>
              <p className="text-center text-muted-foreground">
                Debug your code with our retro CRT-style time machine interface.
              </p>
              <Link href="/code">
                <Button variant="outline">Debug Code</Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

