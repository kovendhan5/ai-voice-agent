"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Newspaper, Leaf, Code, User, LogOut } from "lucide-react"

export default function Navbar() {
  const pathname = usePathname()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState("")

  const handleLogin = () => {
    setIsLoggedIn(true)
    setUsername("kovendhan")
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUsername("")
  }

  const navItems = [
    { name: "News", href: "/news", icon: <Newspaper className="h-4 w-4" /> },
    { name: "Carbon Footprint", href: "/carbon", icon: <Leaf className="h-4 w-4" /> },
    { name: "YourCode", href: "/code", icon: <Code className="h-4 w-4" /> },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Code className="h-6 w-6" />
            <span className="hidden font-bold sm:inline-block">NextGenNode</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center space-x-2 ${
                  pathname === item.href ? "text-foreground" : "text-foreground/60"
                } transition-colors hover:text-foreground`}
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center space-x-2">
            {isLoggedIn ? (
              <>
                <Button variant="ghost" className="w-9 px-0">
                  <User className="h-4 w-4" />
                  <span className="sr-only">User</span>
                </Button>
                <span className="text-sm font-medium">Welcome, {username}!</span>
                <Button variant="ghost" size="sm" className="w-9 px-0" onClick={handleLogout}>
                  <LogOut className="h-4 w-4" />
                  <span className="sr-only">Log out</span>
                </Button>
              </>
            ) : (
              <Button variant="ghost" size="sm" className="w-9 px-0" onClick={handleLogin}>
                <User className="h-4 w-4" />
                <span className="sr-only">Log in</span>
              </Button>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}

