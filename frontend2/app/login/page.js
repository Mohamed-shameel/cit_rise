'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { login, demoAccounts } from '../../lib/auth'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  const handleSignIn = () => {
    setError('')
    const result = login(email, password)
    if (result.success) {
      router.push(result.path)
    } else {
      setError('Invalid credentials. Use demo accounts only.')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSignIn()
  }

  return (
    <div className="min-h-screen flex" style={{ background: 'linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #1e40af 100%)' }}>
      {/* Left branding panel */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-16 text-white">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center">
            <span className="text-2xl">🎓</span>
          </div>
          <span className="text-3xl font-bold tracking-wide">CIT RISE</span>
        </div>
        <h1 className="text-4xl font-bold leading-tight mb-4">
          Empowering Students<br />to Reach New Heights
        </h1>
        <p className="text-blue-200 text-lg leading-relaxed mb-10">
          Connect with mentors, discover opportunities, track your career roadmap,
          and collaborate with peers across CIT.
        </p>
        <div className="flex flex-col gap-4">
          {[
            { icon: '🚀', title: 'Smart Opportunities', desc: 'AI-powered recommendations tailored to your skills' },
            { icon: '🤝', title: 'Expert Mentorship', desc: 'Connect with industry professionals and alumni' },
            { icon: '📈', title: 'Career Roadmap', desc: 'Visualize and track your professional growth' },
          ].map((item) => (
            <div key={item.title} className="flex items-start gap-3">
              <div className="w-9 h-9 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 text-lg">
                {item.icon}
              </div>
              <div>
                <p className="font-semibold text-sm">{item.title}</p>
                <p className="text-blue-200 text-xs mt-0.5">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Right login panel */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-2 mb-6 justify-center">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
              <span className="text-xl">🎓</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">CIT RISE</span>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mb-1">Welcome back</h2>
          <p className="text-gray-500 text-sm mb-6">Sign in to your account to continue</p>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-lg px-4 py-3 mb-4">
              {error}
            </div>
          )}

          <div className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="student@cit.edu"
                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="••••••••"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-sm"
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
            </div>

            <button
              onClick={handleSignIn}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg text-sm transition-colors mt-1"
            >
              Sign In
            </button>
          </div>

          {/* Demo accounts */}
          <div className="mt-6 pt-5 border-t border-gray-100">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Demo Accounts (password: 12345678)</p>
            <div className="flex flex-col gap-1.5">
              {Object.entries(demoAccounts).map(([em, { role }]) => (
                <button
                  key={em}
                  onClick={() => { setEmail(em); setPassword('12345678') }}
                  className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-blue-50 text-left transition-colors group"
                >
                  <span className="text-xs text-gray-600 group-hover:text-blue-700">{em}</span>
                  <span className="text-[10px] font-bold uppercase bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">
                    {role}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
