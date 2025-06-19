<template>
  <div class="mapping-page dark-theme-page">
    <div class="container page-content-container"> 
      <h1 class="page-title mb-5 text-center">AWS Glue to Azure Data Factory Migration Tool</h1>
      
      <!-- Main interaction area: always visible now -->
      <div class="interaction-area mb-5">
        <div class="row">
          <!-- Column 1: File Inputs -->
          <div class="col-lg-5 mb-4 mb-lg-0">
            <h4 class="column-title mb-3">1. Upload Your AWS Glue Assets</h4>
            <div class="file-input-card p-4 rounded">
              <div class="mb-4">
                <label for="glue-config" class="form-label">AWS Glue Configuration (JSON)</label>
                <input 
                  type="file" 
                  id="glue-config" 
                  class="form-control form-control-dark"
                  accept=".json"
                  @change="handleGlueConfigChange"
                  :disabled="isLoading"
                />
                <div v-if="glueConfigName" class="mt-2 text-light file-selected-text">
                  <small>Selected: {{ glueConfigName }}</small>
                </div>
              </div>
              
              <div>
                <label for="glue-script" class="form-label">AWS Glue Script (Python)</label>
                <input 
                  type="file" 
                  id="glue-script" 
                  class="form-control form-control-dark"
                  accept=".py"
                  @change="handleGlueScriptChange"
                  :disabled="isLoading"
                />
                <div v-if="glueScriptName" class="mt-2 text-light file-selected-text">
                  <small>Selected: {{ glueScriptName }}</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Column 2: Action Buttons -->
          <div class="col-lg-7">
            <h4 class="column-title mb-3">2. Choose an Action</h4>
            <div class="action-buttons-grid">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action w-100" @click="fetchMappingReference" :disabled="!hasFiles || isLoading">Generate Mapping Reference</button>
                </div>
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action w-100" @click="fetchAdfNotebook" :disabled="!hasFiles || isLoading">Generate ADF Notebook</button>
                </div>
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action w-100" :disabled="!hasFiles || isLoading">Generate ARM Template</button>
                </div>
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action w-100" :disabled="!hasFiles || isLoading">Generate Manifest Pipeline</button>
                </div>
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action w-100" :disabled="!hasFiles || isLoading">List Required Azure Parameters</button>
                </div>
                <div class="col-md-6 mb-3">
                  <button class="btn btn-action-main w-100" @click="generateMapping" :disabled="!hasFiles || isLoading">
                    <span v-if="isLoading && currentAction === 'doAll'" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ (isLoading && currentAction === 'doAll') ? 'Processing...' : 'Do all and Generate ARM and Manifest' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Loading section (remains the same) -->
      <div v-if="isLoading" class="loading-section text-center my-5">
      <div class="spinner-border text-accent" role="status"> <!-- Changed to text-accent -->
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">{{ dynamicLoadingMessage }}</p>
      <p class="text-muted-dark">This may take a few moments.</p> <!-- Custom muted class for dark theme -->
    </div>
    
    <div v-if="report" class="report-section mt-5"> <!-- Added mt-5 for spacing when input area is always visible -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="report-section-title mb-0">{{ activeReportTitle }}</h4>
        <div>
          <button @click="resetForm" class="btn btn-cta-secondary me-2">Upload New Files & Clear Report</button>
          <button @click="downloadReport" class="btn btn-cta-primary">Download Report</button>
        </div>
      </div>
      
      <div class="card dark-card">
        <!-- Card header removed as title is now above the card -->
        <div class="card-body">
          <div class="report-content" v-html="renderedReport"></div>
        </div>
      </div>
    </div>
    
      <div v-if="error" class="alert alert-danger dark-alert-danger mt-3"> <!-- Custom class for dark alert -->
        {{ error }}
      </div>
    </div> <!-- Closing .container -->
  </div>
</template>

<script>
import { marked } from 'marked';
import axios from 'axios';

export default {
  name: 'MappingPage', // Changed component name
  data() {
    return {
      glueConfig: null,
      glueScript: null,
      glueConfigName: '',
      glueScriptName: '',
      report: null,
      isLoading: false,
      error: null,
      currentAction: null, // To track which button initiated loading
      activeReportTitle: 'Generated Output' // For dynamic report card header
    };
  },
  computed: {
    hasFiles() {
      return this.glueConfig && this.glueScript;
    },
    renderedReport() {
      return this.report ? marked(this.report) : '';
    },
    dynamicLoadingMessage() {
      if (!this.isLoading) return '';
      switch (this.currentAction) {
        case 'adfNotebook':
          return 'Generating ADF Notebook...';
        case 'mappingRef':
          return 'Generating Mapping Reference...';
        case 'doAll':
          return 'Generating Full Report & ARM/Manifest...'; // Updated text
        default:
          return 'Processing...';
      }
    }
  },
  methods: {
    handleGlueConfigChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.glueConfigName = file.name;
        this.glueConfig = file;
        this.error = null;
      }
    },
    handleGlueScriptChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.glueScriptName = file.name;
        this.glueScript = file;
        this.error = null;
      }
    },
    async generateMapping() { // This is for the "Do All & Generate Report" button
      if (!this.hasFiles) {
        this.error = "Please upload both AWS Glue configuration and script files.";
        return;
      }
      
      this.isLoading = true;
      this.error = null;
      this.currentAction = 'doAll'; 
      this.activeReportTitle = 'Overall Migration Report'; // Set title
      
      try {
        const formData = new FormData();
        formData.append('glue_config', this.glueConfig);
        formData.append('glue_script', this.glueScript);
        
        const response = await axios.post('/api/generate-mapping', formData);
        this.report = response.data.report;
      } catch (error) {
        this.error = `Error generating report: ${error.response?.data?.detail || error.message}`;
      } finally {
        this.isLoading = false;
        // this.currentAction = null; // Keep currentAction until new action or reset
      }
    },
    resetForm() {
      this.glueConfig = null;
      this.glueScript = null;
      this.glueConfigName = '';
      this.glueScriptName = '';
      this.report = null;
      this.error = null;
      
      // Reset file input elements after Vue has updated the DOM
      this.$nextTick(() => {
        const glueConfigInput = document.getElementById('glue-config');
        if (glueConfigInput) {
          glueConfigInput.value = '';
        }
        const glueScriptInput = document.getElementById('glue-script');
        if (glueScriptInput) {
          glueScriptInput.value = '';
        }
      });
    },
    downloadReport() {
      if (!this.report) return;
      
      const blob = new Blob([this.report], { type: 'text/markdown' }); // Assuming report is markdown or plain text
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      // Determine filename based on what was generated, or keep generic
      // For simplicity, keeping generic for now. Could be enhanced if 'type' is stored.
      a.download = 'generated-output.txt'; 
      if (this.report && this.report.startsWith("--- MAPPING REPORT ---")) { // Heuristic
          a.download = 'mapping_report.md';
      } else if (this.report && (this.report.includes("def ") || this.report.includes("import "))) { // Heuristic for python
          a.download = 'databricks_notebook.py';
      }
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    },

    async fetchAdfNotebook() {
      if (!this.hasFiles) {
        this.error = "Please upload both AWS Glue configuration and script files.";
        return;
      }
      this.isLoading = true;
      this.error = null;
      this.report = null; 
      this.currentAction = 'adfNotebook';
      this.activeReportTitle = 'ADF Notebook'; // Set title

      try {
        const formData = new FormData();
        formData.append('glue_config', this.glueConfig);
        formData.append('glue_script', this.glueScript);
        
        console.log("Fetching ADF Notebook...");
        const response = await axios.post('/api/generate-adf-notebook', formData);
        this.report = response.data.report; 
        console.log("ADF Notebook fetched.");
      } catch (error) {
        this.error = `Error generating ADF Notebook: ${error.response?.data?.detail || error.message}`;
        console.error("Error fetching ADF notebook:", error);
      } finally {
        this.isLoading = false;
        // this.currentAction = null;
      }
    },

    async fetchMappingReference() {
      if (!this.hasFiles) {
        this.error = "Please upload both AWS Glue configuration and script files.";
        return;
      }
      this.isLoading = true;
      this.error = null;
      this.report = null; 
      this.currentAction = 'mappingRef';
      this.activeReportTitle = 'Mapping Reference'; // Set title

      try {
        const formData = new FormData();
        formData.append('glue_config', this.glueConfig);
        formData.append('glue_script', this.glueScript);

        console.log("Fetching Mapping Reference...");
        const response = await axios.post('/api/generate-mapping-reference', formData);
        this.report = response.data.report; // Expecting markdown string
        // this.reportType = response.data.type;
        console.log("Mapping Reference fetched.");
      } catch (error) {
        this.error = `Error generating Mapping Reference: ${error.response?.data?.detail || error.message}`;
        console.error("Error fetching mapping reference:", error);
      } finally {
        this.isLoading = false;
        // this.currentAction = null; 
      }
    }
  }
};
</script>

<style scoped>
.dark-theme-page {
  /* Base styling for the page, inherits dark background from App.vue */
  color: #e0e0e0; /* Default light text */
  padding-top: 1rem; /* Add some padding if needed, or rely on mt-4 from App.vue's main-content-area */
  padding-bottom: 2rem; /* Add some padding at the bottom */
}

.page-content-container {
  /* max-width: 1200px; /* Example for wider content on large screens */
}

.interaction-area {
  /* Styles for the combined input and action button area if needed */
  /* For example, add a border or different background if desired */
  /* background-color: #1f1f1f; */
  /* padding: 2rem; */
  /* border-radius: 0.5rem; */
}

.report-section-title {
  color: #e0e0e0;
  font-weight: 600;
}

.page-title {
  color: #ffffff;
  font-weight: 700;
}

.column-title {
  color: #e0e0e0;
  font-size: 1.4rem;
  font-weight: 600;
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
}

.file-input-card {
  background-color: #2a2a2a; /* Similar to dark-card */
  border: 1px solid #383838;
  /* Removed 'rounded' from template, add border-radius here if needed */
  border-radius: 0.375rem; /* Bootstrap's default rounded amount */
}

.file-selected-text {
  font-size: 0.875em;
  /* color: #00aeff; /* Using text-light from template for now */
}

.action-buttons-grid .btn {
  padding-top: 0.8rem;
  padding-bottom: 0.8rem;
  font-size: 0.9rem; /* Slightly smaller for grid buttons */
  height: 100%; /* Make buttons in a row same height */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Button Styles for the new action grid */
.btn-action-main { /* Main action button, e.g., "Do All & Generate Report" */
  background-color: #00aeff;
  border-color: #00aeff;
  color: #ffffff;
  font-weight: 600; /* Make it stand out */
  /* General button grid styles like padding, font-size are in .action-buttons-grid .btn */
}
.btn-action-main:hover {
  background-color: #0095e0;
  border-color: #0095e0;
  transform: translateY(-2px); /* Added hover effect */
}
.btn-action-main:disabled {
  background-color: #3a3f44 !important; 
  border-color: #3a3f44 !important;
  color: #777 !important;
  cursor: not-allowed;
}

.btn-action { /* For the other 5 buttons in the grid */
  background-color: #343a40; 
  border-color: #495057;
  color: #e0e0e0;
  font-weight: 500;
  /* General button grid styles like padding, font-size are in .action-buttons-grid .btn */
}
.btn-action:hover {
  background-color: #495057;
  border-color: #5a6268;
  color: #ffffff;
  transform: translateY(-2px); /* Added hover effect */
}
.btn-action:disabled {
  background-color: #2c3034 !important;
  border-color: #2c3034 !important;
  color: #666 !important;
  cursor: not-allowed;
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

.form-label {
  color: #c0c0c0; /* Lighter label text */
}

.form-control-dark {
  background-color: #1e1e1e;
  color: #e0e0e0;
  border: 1px solid #444;
}
.form-control-dark:focus {
  background-color: #2a2a2a;
  color: #e0e0e0;
  border-color: #00aeff; /* Accent color on focus */
  box-shadow: 0 0 0 0.25rem rgba(0, 174, 255, 0.25);
}
.form-control-dark::file-selector-button { /* Style file input button */
  background-color: #00aeff;
  color: white;
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
}
.form-control-dark::file-selector-button:hover {
  background-color: #0095e0;
}


/* Button Styles for Mapping Page */
.btn-action-main { /* Main action button, e.g., "Do All & Generate Report" */
  background-color: #00aeff;
  border-color: #00aeff;
  color: #ffffff;
  /* padding, font-size, etc., inherited from .action-buttons-grid .btn or define here */
  font-weight: 600; /* Make it stand out */
}
.btn-action-main:hover {
  background-color: #0095e0;
  border-color: #0095e0;
}
.btn-action-main:disabled {
  background-color: #3a3f44 !important; /* Use important if needed to override Bootstrap */
  border-color: #3a3f44 !important;
  color: #777 !important;
  cursor: not-allowed;
}

.btn-action { /* For the other 5 buttons */
  background-color: #343a40; 
  border-color: #495057;
  color: #e0e0e0;
  /* padding, font-size, etc., inherited from .action-buttons-grid .btn or define here */
}
.btn-action:hover {
  background-color: #495057;
  border-color: #5a6268;
  color: #ffffff;
}
.btn-action:disabled {
  background-color: #2c3034 !important;
  border-color: #2c3034 !important;
  color: #666 !important;
  cursor: not-allowed;
}

/* Keep .btn-cta-primary and .btn-cta-secondary for report section buttons if they are different */
.btn-cta-primary { /* Used for Download Report */
  background-color: #00aeff;
  border-color: #00aeff;
  color: #ffffff;
  padding: 0.5rem 1.5rem; 
  font-size: 1rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-cta-primary:hover {
  background-color: #0095e0;
  border-color: #0095e0;
  transform: translateY(-2px);
}
.btn-cta-primary:disabled { /* This style might not be hit if :disabled is on btn-action-main */
  background-color: #555;
  border-color: #555;
  color: #999;
}


.btn-cta-secondary { /* Used for Upload New Files */
  padding: 0.5rem 1.5rem; /* Adjusted padding */
  font-size: 1rem;
  font-weight: 600;
  border-radius: 50px;
  color: #00aeff;
  background-color: transparent;
  border: 2px solid #00aeff;
  transition: all 0.3s ease;
}
.btn-cta-secondary:hover {
  background-color: #00aeff;
  color: #1e1e1e; 
  transform: translateY(-2px);
}

.text-accent { /* For spinner */
  color: #00aeff !important;
}
.text-muted-dark {
  color: #a0a0a0 !important;
}

.dark-alert-danger {
  background-color: #4a272b; /* Darker red background */
  color: #f8d7da; /* Light red text */
  border-color: #f5c6cb;
}


/* Report Content Dark Theme */
.report-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 1.5rem;
  background-color: #1e1e1e; /* Dark background for report area */
  border-radius: 0.25rem;
  color: #e0e0e0; /* Default light text for report */
  border: 1px solid #333;
}

.report-content :deep(h1),
.report-content :deep(h2),
.report-content :deep(h3),
.report-content :deep(h4),
.report-content :deep(h5),
.report-content :deep(h6) {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #ffffff; /* Brighter headings */
}

.report-content :deep(table) {
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
}

.report-content :deep(table th),
.report-content :deep(table td) {
  padding: 0.75rem; /* Increased padding */
  border: 1px solid #444; /* Darker borders */
  color: #c0c0c0; /* Lighter cell text */
}

.report-content :deep(table th) {
  background-color: #343a40; /* Dark header for table */
  color: #ffffff;
  font-weight: 600;
}

.report-content :deep(pre) {
  background-color: #2a2a2a; /* Dark background for code blocks */
  color: #f8f8f2; /* Light code text (Solarized-like) */
  padding: 1rem;
  border-radius: 0.25rem;
  overflow-x: auto;
  border: 1px solid #333;
}

.report-content :deep(code) {
  font-family: 'SFMono-Regular', Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.9em; /* Slightly larger for readability */
  background-color: #2a2a2a; /* Match pre or be slightly different if inline */
  color: #f8f8f2; 
  padding: 0.2em 0.4em; /* Padding for inline code */
  border-radius: 3px;
}
.report-content :deep(pre code) { /* Code specifically within pre should not have extra padding/bg */
    padding: 0;
    background-color: transparent;
}

.report-content :deep(a) {
  color: #00aeff; /* Accent color for links */
}
.report-content :deep(a:hover) {
  color: #3cc8ff;
}

.report-content :deep(p) {
  color: #c0c0c0;
  line-height: 1.7;
}

.report-content :deep(ul),
.report-content :deep(ol) {
  padding-left: 2rem;
  color: #c0c0c0;
}

.report-content :deep(li) {
  margin-bottom: 0.5rem;
}

.report-content :deep(blockquote) {
  border-left: 4px solid #00aeff;
  padding-left: 1rem;
  margin-left: 0;
  color: #a0a0a0;
  font-style: italic;
}
</style>
