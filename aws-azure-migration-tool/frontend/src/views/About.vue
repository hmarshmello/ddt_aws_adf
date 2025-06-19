<template>
  <div class="about dark-theme-page">
    <div class="container page-content-container"> <!-- Added .container here -->
      <h1 class="page-title mb-4">About the AWS to Azure Migration Mapping Tool</h1>
      
      <div class="card dark-card mb-4">
        <div class="card-header dark-card-header">
          <h5 class="mb-0">Overview</h5>
      </div>
      <div class="card-body">
        <p>
          The AWS to Azure Migration Mapping Tool helps you plan and document your migration from AWS Glue to Azure Data Factory and Azure Databricks.
          By analyzing your AWS Glue job definitions and scripts, it generates a comprehensive mapping document that outlines how to implement equivalent functionality in Azure.
        </p>
      </div>
    </div>
    
    <div class="card dark-card mb-4">
      <div class="card-header dark-card-header">
        <h5 class="mb-0">How It Works</h5>
      </div>
      <div class="card-body">
        <ol>
          <li>Upload your AWS Glue job configuration (JSON) and script (Python) files.</li>
          <li>The tool analyzes the files to understand the job's purpose, configuration, and logic.</li>
          <li>A comprehensive mapping report is generated, detailing how to implement the same functionality in Azure Data Factory and Azure Databricks.</li>
          <li>Review the report and download it for future reference.</li>
        </ol>
      </div>
    </div>
    
    <div class="card dark-card mb-4">
      <div class="card-header dark-card-header">
        <h5 class="mb-0">What's Included in the Mapping</h5>
      </div>
      <div class="card-body">
        <ul>
          <li><strong>Executive Summary:</strong> A high-level overview of the migration approach.</li>
          <li><strong>Assumptions and Decisions:</strong> Key technical decisions made for the migration.</li>
          <li><strong>Azure Data Factory Pipeline Definition:</strong> Detailed pipeline configuration.</li>
          <li><strong>Azure Linked Services:</strong> Required connections to data sources and compute resources.</li>
          <li><strong>Azure Datasets:</strong> Data source and sink definitions.</li>
          <li><strong>Azure Databricks Notebook:</strong> Converted script with necessary modifications.</li>
          <li><strong>Configuration Mapping:</strong> Detailed mapping of AWS Glue configurations to Azure equivalents.</li>
          <li><strong>Post-Migration Considerations:</strong> Testing, performance tuning, and monitoring recommendations.</li>
        </ul>
      </div>
    </div>
    
    <div class="card dark-card">
      <div class="card-header dark-card-header">
        <h5 class="mb-0">Technologies Used</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">
            <h6 class="tech-heading">Backend:</h6>
            <ul>
              <li>FastAPI (Python web framework)</li>
              <li>CrewAI (AI-powered analysis)</li>
              <li>Uvicorn (ASGI server)</li>
            </ul>
          </div>
          <div class="col-md-6">
            <h6 class="tech-heading">Frontend:</h6>
            <ul>
              <li>Vue.js (JavaScript framework)</li>
              <li>Bootstrap (CSS framework)</li>
              <li>Marked.js (Markdown rendering)</li>
              <li>Axios (HTTP client)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    </div> <!-- Closing .container -->
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.dark-theme-page {
  /* max-width: 1000px; /* Removed, .container will handle width */
  /* margin: 0 auto; /* Removed, .container will handle centering */
  color: #e0e0e0; /* Default light text */
  padding-top: 1rem; /* Consistent padding with MappingPage */
  padding-bottom: 2rem; /* Consistent padding with MappingPage */
}

.page-content-container {
  /* Styles for the new container if needed */
}

.page-title {
  color: #ffffff;
  font-weight: 700;
}

.dark-card {
  background-color: #2a2a2a; /* Dark card background */
  border: 1px solid #383838; /* Subtle border */
  color: #e0e0e0;
}

.dark-card-header {
  background-color: #343a40; /* Slightly lighter dark for header */
  color: #ffffff;
  border-bottom: 1px solid #484848;
}

.card-body p,
.card-body li {
  color: #c0c0c0; /* Lighter text for paragraphs and list items */
}

.card-body strong {
  color: #e0e0e0; /* Ensure strong text is also light */
}

.card-body ol,
.card-body ul {
  padding-left: 1.5rem; /* Adjust padding if needed */
}

.tech-heading {
  color: #f0f0f0; /* Brighter heading for tech list */
  font-weight: 600;
  margin-bottom: 0.5rem;
}
</style>
