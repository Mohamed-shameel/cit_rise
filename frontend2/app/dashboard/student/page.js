'use client'

import TopNavbar from '../../../components/layout/TopNavbar'
import Sidebar from '../../../components/layout/Sidebar'
import RightPanel from '../../../components/layout/RightPanel'
import OpportunityCard from '../../../components/dashboard/OpportunityCard'
import EventCard from '../../../components/dashboard/EventCard'
import PersonCard from '../../../components/dashboard/PersonCard'

export default function StudentDashboard() {
  return (
    <div className="flex flex-col h-screen">
      <TopNavbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-100">

          {/* Section 1: Recommended Opportunities */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Recommended Opportunities</h2>
              <a className="text-blue-600 text-sm font-medium hover:underline cursor-pointer">See all</a>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <OpportunityCard
                type="HACKATHON"
                title="National AI Hackathon"
                organizer="Tech Hub Foundation"
                deadline="Oct 30, 2024"
                location="Main Campus / Remote"
                buttonLabel="Register"
              />
              <OpportunityCard
                type="OPEN SOURCE"
                title="Google Summer of Code"
                organizer="Google Open Source"
                deadline="Nov 15, 2024"
                location="Global / Remote"
                buttonLabel="Apply Now"
              />
              <OpportunityCard
                type="INTERNSHIP"
                title="ML Research Intern"
                organizer="DeepMind Labs"
                deadline="Oct 28, 2024"
                location="London, UK (Hybrid)"
                buttonLabel="Register"
              />
            </div>
          </div>

          {/* Section 2: Upcoming Events */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Upcoming Events</h2>
              <a className="text-blue-600 text-sm font-medium hover:underline cursor-pointer">View Calendar</a>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <EventCard
                category="WORKSHOP"
                title="Advanced Neural Networks"
                hostedBy="AI Club"
                date="OCT 22"
                time="14:00 - 17:00"
                image={null}
              />
              <EventCard
                category="HACKATHON"
                title="Robotics Speed Challenge"
                hostedBy="Robotics Hub"
                date="OCT 25"
                time="09:00 - 21:00"
                image={null}
              />
            </div>
          </div>

          {/* Section 3: Connect With People */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Connect With People</h2>
              <a className="text-blue-600 text-sm font-medium hover:underline cursor-pointer">Find more</a>
            </div>
            <div className="flex flex-col gap-3">
              <PersonCard
                name="Sarah Chen"
                role="Mentor"
                description="Senior AI Researcher @ DeepTech • Alumni '20"
                avatarInitial="S"
                avatarColor="bg-rose-500"
              />
              <PersonCard
                name="Rahul Verma"
                role="Student"
                description="CSE AI • Year 3 • Interested in ML & Robotics"
                avatarInitial="R"
                avatarColor="bg-indigo-500"
              />
              <PersonCard
                name="Priya Nair"
                role="Alumni"
                description="SWE @ Google • CIT Batch of 2022"
                avatarInitial="P"
                avatarColor="bg-emerald-500"
              />
            </div>
          </div>

        </main>
        <RightPanel />
      </div>
    </div>
  )
}
