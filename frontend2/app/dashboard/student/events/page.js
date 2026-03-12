'use client'

import TopNavbar from '../../../../components/layout/TopNavbar'
import Sidebar from '../../../../components/layout/Sidebar'
import OpportunityCard from '../../../../components/dashboard/OpportunityCard'
import EventCard from '../../../../components/dashboard/EventCard'

export default function EventsPage() {
  return (
    <div className="flex flex-col h-screen">
      <TopNavbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-100">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Events & Opportunities</h1>
              <p className="text-gray-500 text-sm mt-1">Discover hackathons, workshops, internships and more.</p>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Upcoming Events</h2>
            <div className="grid grid-cols-2 gap-4">
              <EventCard category="WORKSHOP"  title="Advanced Neural Networks" hostedBy="AI Club"      date="OCT 22" time="14:00 - 17:00" image={null} />
              <EventCard category="HACKATHON" title="Robotics Speed Challenge"  hostedBy="Robotics Hub" date="OCT 25" time="09:00 - 21:00" image={null} />
              <EventCard category="WORKSHOP"  title="Cloud Computing Bootcamp"  hostedBy="DevOps Club"  date="NOV 2"  time="10:00 - 16:00" image={null} />
              <EventCard category="HACKATHON" title="Smart City Challenge"      hostedBy="IEEE CIT"     date="NOV 10" time="08:00 - 20:00" image={null} />
            </div>
          </div>

          <div>
            <h2 className="text-lg font-bold text-gray-900 mb-4">Open Opportunities</h2>
            <div className="grid grid-cols-3 gap-4">
              <OpportunityCard type="HACKATHON"    title="National AI Hackathon"    organizer="Tech Hub Foundation" deadline="Oct 30, 2024" location="Main Campus / Remote"  buttonLabel="Register" />
              <OpportunityCard type="OPEN SOURCE"  title="Google Summer of Code"    organizer="Google Open Source"  deadline="Nov 15, 2024" location="Global / Remote"        buttonLabel="Apply Now" />
              <OpportunityCard type="INTERNSHIP"   title="ML Research Intern"       organizer="DeepMind Labs"        deadline="Oct 28, 2024" location="London, UK (Hybrid)"    buttonLabel="Register" />
              <OpportunityCard type="COMPETITION"  title="ACM ICPC Regionals"       organizer="ACM CIT Chapter"     deadline="Nov 5, 2024"  location="On Campus"             buttonLabel="Register" />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
