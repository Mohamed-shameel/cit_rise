import './globals.css'

export const metadata = { title: 'CIT RISE' }

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <body suppressHydrationWarning={true}>{children}</body>
    </html>
  )
}
