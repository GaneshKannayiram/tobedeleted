import React from 'react';

const JobCard = ({ job, similarity }) => (
  <div className="job-card">
    <h3>{job.title} ({Math.round(similarity * 100)}% match)</h3>
    <p>{job.company} • {job.location}</p>
    <p>Skills: {job.skills.join(', ')}</p>
    <a href={job.source_url} target="_blank" rel="noopener">View Job</a>
  </div>
);

export default JobCard;