import React, { useState } from 'react';
import axios from 'axios';
import JobCard from './components/JobCard';

function App() {
  const [jobs, setJobs] = useState([]);
  const [form, setForm] = useState({
    desired_role: '',
    locations: '',
    skills: '',
    experience_level: '',
    min_salary: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/recommend', {
        user_id: "user1",  // Can be dynamic later
        ...form,
        skills: form.skills.split(','),  // Convert comma-separated string to array
        locations: [form.locations]      // Ensure locations is an array
      });
      setJobs(response.data.jobs);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div className="App">
      <h1>Job Recommendation System</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Desired Role (e.g., Software Engineer)" 
          value={form.desired_role}
          onChange={(e) => setForm({...form, desired_role: e.target.value})} 
        />
        <input 
          type="text" 
          placeholder="Locations (e.g., Remote)" 
          value={form.locations}
          onChange={(e) => setForm({...form, locations: e.target.value})} 
        />
        <input 
          type="text" 
          placeholder="Skills (comma-separated, e.g., Python,SQL)" 
          value={form.skills}
          onChange={(e) => setForm({...form, skills: e.target.value})} 
        />
        <input 
          type="text" 
          placeholder="Experience Level (e.g., Mid)" 
          value={form.experience_level}
          onChange={(e) => setForm({...form, experience_level: e.target.value})} 
        />
        <input 
          type="number" 
          placeholder="Minimum Salary" 
          value={form.min_salary}
          onChange={(e) => setForm({...form, min_salary: e.target.value})} 
        />
        <button type="submit">Search Jobs</button>
      </form>
      
      {/* Display recommended jobs */}
      <div className="job-list">
        {jobs.map((job) => (
          <JobCard key={job.job_id || job.id} job={job} />  // Use `job.id` as fallback
        ))}
      </div>
    </div>
  );
}

export default App;