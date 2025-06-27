// src/app/layout.js

import './globals.css'; // Import your global Tailwind or CSS styles

// Import Google Fonts using Next.js font optimization
import { Inter, Roboto_Mono } from 'next/font/google';

// Configure the Inter font (sans-serif)
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter', // Exposed as a CSS variable
});

// Configure the Roboto Mono font (monospace)
const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
});

// Export page metadata (optional but good for SEO)
export const metadata = {
  title: 'Document Intelligence Platform',
  description: 'Ask AI questions about your uploaded documents',
};

// Main root layout wrapper
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`
          ${inter.variable} 
          ${robotoMono.variable} 
          antialiased 
          bg-white 
          text-gray-900 
          min-h-screen
        `}
      >
        {children}
      </body>
    </html>
  );
}
