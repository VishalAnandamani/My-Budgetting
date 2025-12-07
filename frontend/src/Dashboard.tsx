import React, { useEffect, useState } from 'react';
import { getStats } from './api';
import type { Stats } from './api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Link } from 'react-router-dom';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    getStats().then(setStats).catch(console.error);
  }, []);

  if (!stats) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Family Finance Dashboard</h1>
        <Link to="/upload" className="bg-blue-500 text-white px-4 py-2 rounded">
          + Upload Data
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Debt Card */}
        <div className="bg-white shadow p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Debt Settlement</h3>
          {stats.debt_summary.length === 0 ? (
            <p className="text-gray-500">All settled up!</p>
          ) : (
            stats.debt_summary.map((debt, idx) => (
              <div key={idx} className="text-xl p-4 bg-red-50 rounded border border-red-200">
                <span className="font-bold text-red-600">{debt.debtor}</span> owes{' '}
                <span className="font-bold text-green-600">{debt.creditor}</span>
                <div className="text-3xl font-bold mt-2">${debt.amount.toFixed(2)}</div>
              </div>
            ))
          )}
        </div>

        {/* Category Chart */}
        <div className="bg-white shadow p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Spending by Category</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.spending_by_category}
                  dataKey="total"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {stats.spending_by_category.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
