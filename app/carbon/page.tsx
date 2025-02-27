"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Leaf, Info, AlertTriangle, CheckCircle } from "lucide-react"
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ChartTooltip,
} from "@/components/ui/chart"

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8"]

export default function CarbonPage() {
  const [formData, setFormData] = useState({
    electricity: "",
    gas: "",
    car: "",
    flights: "",
    diet: "mixed", // mixed, vegetarian, vegan
    recycling: "sometimes", // never, sometimes, always
  })

  const [result, setResult] = useState<null | {
    total: number
    breakdown: { name: string; value: number }[]
    tips: string[]
    level: "low" | "medium" | "high"
  }>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const calculateFootprint = () => {
    // Simple calculation for demonstration
    const electricityFootprint = Number.parseFloat(formData.electricity) * 0.5 || 0
    const gasFootprint = Number.parseFloat(formData.gas) * 0.2 || 0
    const carFootprint = Number.parseFloat(formData.car) * 0.3 || 0
    const flightsFootprint = Number.parseFloat(formData.flights) * 1.5 || 0

    // Diet factor
    let dietFactor = 1
    if (formData.diet === "vegetarian") dietFactor = 0.7
    if (formData.diet === "vegan") dietFactor = 0.5

    // Recycling factor
    let recyclingFactor = 1
    if (formData.recycling === "sometimes") recyclingFactor = 0.9
    if (formData.recycling === "always") recyclingFactor = 0.8

    const dietFootprint = 2 * dietFactor
    const recyclingFootprint = 1 * recyclingFactor

    const total =
      electricityFootprint + gasFootprint + carFootprint + flightsFootprint + dietFootprint + recyclingFootprint

    const breakdown = [
      { name: "Electricity", value: electricityFootprint },
      { name: "Gas", value: gasFootprint },
      { name: "Car", value: carFootprint },
      { name: "Flights", value: flightsFootprint },
      { name: "Diet", value: dietFootprint },
      { name: "Waste", value: recyclingFootprint },
    ]

    // Determine level and tips
    let level: "low" | "medium" | "high" = "medium"
    let tips: string[] = []

    if (total < 5) {
      level = "low"
      tips = [
        "Great job! Your carbon footprint is relatively low.",
        "Consider installing solar panels to further reduce your electricity emissions.",
        "Look into community garden projects to offset remaining emissions.",
      ]
    } else if (total < 10) {
      level = "medium"
      tips = [
        "Your carbon footprint is average. Here are some ways to improve:",
        "Reduce car usage by carpooling or using public transportation.",
        "Switch to energy-efficient appliances and LED lighting.",
        "Consider reducing meat consumption further.",
      ]
    } else {
      level = "high"
      tips = [
        "Your carbon footprint is higher than average. Here's how to reduce it:",
        "Significantly reduce air travel or offset your flights.",
        "Switch to renewable energy sources for your home.",
        "Consider a plant-based diet and reduce food waste.",
        "Improve home insulation to reduce heating/cooling needs.",
      ]
    }

    setResult({ total, breakdown, tips, level })
  }

  return (
    <div className="container py-8">
      <div className="mb-8 space-y-4">
        <h1 className="text-3xl font-bold">Carbon Footprint Calculator</h1>
        <p className="text-muted-foreground">
          Calculate your carbon footprint and discover ways to reduce your environmental impact.
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Enter Your Data</CardTitle>
            <CardDescription>
              Provide information about your lifestyle to calculate your carbon footprint.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="electricity" className="text-sm font-medium">
                Monthly Electricity Usage (kWh)
              </label>
              <Input
                id="electricity"
                name="electricity"
                type="number"
                placeholder="e.g., 500"
                value={formData.electricity}
                onChange={handleInputChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="gas" className="text-sm font-medium">
                Monthly Natural Gas Usage (therms)
              </label>
              <Input
                id="gas"
                name="gas"
                type="number"
                placeholder="e.g., 50"
                value={formData.gas}
                onChange={handleInputChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="car" className="text-sm font-medium">
                Weekly Car Mileage
              </label>
              <Input
                id="car"
                name="car"
                type="number"
                placeholder="e.g., 100"
                value={formData.car}
                onChange={handleInputChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="flights" className="text-sm font-medium">
                Flights per Year
              </label>
              <Input
                id="flights"
                name="flights"
                type="number"
                placeholder="e.g., 2"
                value={formData.flights}
                onChange={handleInputChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="diet" className="text-sm font-medium">
                Diet Type
              </label>
              <select
                id="diet"
                name="diet"
                value={formData.diet}
                onChange={handleInputChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="mixed">Mixed (includes meat)</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="recycling" className="text-sm font-medium">
                Recycling Habits
              </label>
              <select
                id="recycling"
                name="recycling"
                value={formData.recycling}
                onChange={handleInputChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="never">Never recycle</option>
                <option value="sometimes">Sometimes recycle</option>
                <option value="always">Always recycle</option>
              </select>
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={calculateFootprint} className="w-full">
              Calculate Footprint
            </Button>
          </CardFooter>
        </Card>

        {result && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Your Carbon Footprint</CardTitle>
                {result.level === "low" && <CheckCircle className="h-6 w-6 text-green-500" />}
                {result.level === "medium" && <Info className="h-6 w-6 text-amber-500" />}
                {result.level === "high" && <AlertTriangle className="h-6 w-6 text-red-500" />}
              </div>
              <CardDescription>
                {result.level === "low" && "Your carbon footprint is lower than average. Great job!"}
                {result.level === "medium" && "Your carbon footprint is around average. There's room for improvement."}
                {result.level === "high" && "Your carbon footprint is higher than average. Consider making changes."}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="text-center">
                <div className="text-4xl font-bold">{result.total.toFixed(2)}</div>
                <div className="text-sm text-muted-foreground">Tons of CO2 per year</div>
              </div>

              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={result.breakdown}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {result.breakdown.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip content={<ChartTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={result.breakdown}
                    margin={{
                      top: 20,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip content={<ChartTooltip />} />
                    <Legend />
                    <Bar dataKey="value" name="CO2 (tons)" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="space-y-2">
                <h3 className="font-medium">Recommendations</h3>
                <ul className="space-y-1">
                  {result.tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <Leaf className="mr-2 h-5 w-5 text-green-500 shrink-0" />
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

