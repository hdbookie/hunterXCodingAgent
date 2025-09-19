import React, { useState } from 'react';

const SessionScheduler: React.FC = () => {
  const [formData, setFormData] = useState({
    title: '',
    date: '',
    time: '',
    location: '',
    maxStudents: 8,
    description: ''
  });

  return (
    <div className="p-4">
      <div className="card-surf max-w-md mx-auto">
        <h2 className="text-xl font-bold mb-6">Schedule New Session</h2>

        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Session Title
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-surf-blue"
              placeholder="e.g., Beginner Surf Lesson"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date
              </label>
              <input
                type="date"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-surf-blue"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Time
              </label>
              <input
                type="time"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-surf-blue"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Location
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-surf-blue"
              placeholder="e.g., Malibu Beach"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Max Students
            </label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-surf-blue">
              <option value="4">4 students</option>
              <option value="6">6 students</option>
              <option value="8">8 students</option>
              <option value="10">10 students</option>
            </select>
          </div>

          <button type="submit" className="btn-surf w-full">
            Create Session
          </button>
        </form>
      </div>
    </div>
  );
};

export default SessionScheduler;