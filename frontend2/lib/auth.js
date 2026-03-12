'use client'

export const demoAccounts = {
  'student@cit.edu': { role: 'student', path: '/dashboard/student' },
  'mentor@cit.edu':  { role: 'mentor',  path: '/dashboard/mentor'  },
  'club@cit.edu':    { role: 'club',    path: '/dashboard/club'    },
  'admin@cit.edu':   { role: 'admin',   path: '/dashboard/admin'   },
  'alumni@cit.edu':  { role: 'alumni',  path: '/dashboard/alumni'  },
}

export function login(email, password) {
  const account = demoAccounts[email]
  if (account && password === '12345678') {
    localStorage.setItem('userRole', account.role)
    localStorage.setItem('userEmail', email)
    return { success: true, path: account.path }
  }
  return { success: false }
}

export function logout() {
  localStorage.removeItem('userRole')
  localStorage.removeItem('userEmail')
}

export function getCurrentUser() {
  if (typeof window === 'undefined') return null
  return {
    email: localStorage.getItem('userEmail'),
    role: localStorage.getItem('userRole'),
  }
}
