import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EV Intelligence Platform',
  description: 'AI-powered Supply Chain & Asset Intelligence for Industrial EV Transition',
  viewport: 'width=device-width, initial-scale=1.0, maximum-scale=5.0',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'EV Intelligence',
  },
  formatDetection: {
    telephone: false,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="theme-color" content="#059669" />
        <meta name="mobile-web-app-capable" content="yes" />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  )
}
