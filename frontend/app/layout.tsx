import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EV Intelligence Platform',
  description: 'AI-powered Supply Chain & Asset Intelligence for Industrial EV Transition',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
