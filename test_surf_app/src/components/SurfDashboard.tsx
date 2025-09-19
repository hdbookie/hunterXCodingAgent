import React from 'react';

const SurfDashboard: React.FC = () => {
  return (
    <div className="p-4 space-y-6">
      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card-surf text-center">
          <div className="text-2xl font-bold text-surf-blue">12</div>
          <div className="text-sm text-gray-600">Active Students</div>
        </div>
        <div className="card-surf text-center">
          <div className="text-2xl font-bold text-surf-teal">5</div>
          <div className="text-sm text-gray-600">Sessions This Week</div>
        </div>
        <div className="card-surf text-center">
          <div className="text-2xl font-bold text-surf-sand">8.5</div>
          <div className="text-sm text-gray-600">Avg Rating</div>
        </div>
        <div className="card-surf text-center">
          <div className="text-2xl font-bold text-green-600">92%</div>
          <div className="text-sm text-gray-600">Attendance</div>
        </div>
      </div>

      {/* Upcoming Sessions */}
      <div className="card-surf">
        <h3 className="text-lg font-semibold mb-4">Upcoming Sessions</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <div className="font-medium">Beginner Group A</div>
              <div className="text-sm text-gray-600">Today, 2:00 PM - Malibu</div>
            </div>
            <span className="text-surf-blue font-medium">6/8 students</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button className="btn-surf w-full">Schedule New Session</button>
        <button className="btn-surf w-full bg-surf-teal hover:bg-teal-600">View All Students</button>
      </div>
    </div>
  );
};

export default SurfDashboard;