<template>
  <div class="modern-home dark-theme">
    <!-- Hero Section -->
    <section class="hero text-center">
      <div class="hero-overlay"></div> <!-- Overlay for better text readability if bg is complex -->
      <div class="container-fluid hero-content">
        <h1 class="hero-title">Migrate with Clarity.</h1>
        <h2 class="hero-subtitle">AWS Glue to Azure. Effortlessly.</h2>
        <p class="hero-description">
          Leverage AI for a seamless transition of your ETL workloads to Azure Data Factory and Databricks.
          Our intelligent tool analyzes your existing setup and provides a comprehensive migration blueprint.
        </p>
        <router-link to="/mapping" class="btn btn-hero mt-4">Start Your Migration Analysis</router-link>
      </div>
    </section>

    <!-- Value Proposition Section -->
    <section class="value-prop py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">The Intelligent Path to Azure</h2>
          <p class="lead section-subtitle-muted">Transform complexity into clarity with our AI-driven approach.</p>
        </div>
        <div class="row">
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="value-item">
              <div class="value-icon">✨</div>
              <h5 class="value-title">AI-Powered Precision</h5>
              <p class="value-text">Our engine deciphers your Glue jobs for accurate Azure mapping, minimizing manual oversight.</p>
            </div>
          </div>
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="value-item">
              <div class="value-icon">🗺️</div>
              <h5 class="value-title">Comprehensive Blueprints</h5>
              <p class="value-text">Receive detailed, actionable plans for Azure Data Factory and Databricks implementation.</p>
            </div>
          </div>
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="value-item">
              <div class="value-icon">⏱️</div>
              <h5 class="value-title">Accelerated Transition</h5>
              <p class="value-text">Reduce manual effort and significantly speed up your cloud migration timeline.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Process Overview Section -->
    <section class="process-overview py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Your Migration Journey, Simplified</h2>
        </div>
        <div class="row text-center">
          <div class="col-md-4 mb-4">
            <div class="process-step">
              <div class="step-icon-wrapper"><span class="step-number">1</span></div>
              <h5 class="step-title mt-3">Submit Assets</h5>
              <p class="step-text">Securely upload your AWS Glue job configuration (JSON) and Python scripts.</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="process-step">
              <div class="step-icon-wrapper"><span class="step-number">2</span></div>
              <h5 class="step-title mt-3">Intelligent Mapping</h5>
              <p class="step-text">Our AI analyzes dependencies, transformations, and settings for a precise Azure plan.</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="process-step">
              <div class="step-icon-wrapper"><span class="step-number">3</span></div>
              <h5 class="step-title mt-3">Azure Roadmap</h5>
              <p class="step-text">Download your tailored migration report, ready for Azure implementation.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final Call to Action -->
    <section class="final-cta text-center py-5">
      <div class="container">
        <h2 class="cta-title mb-3">Ready to Transform Your ETL?</h2>
        <p class="lead section-subtitle-muted mb-4">
          Begin your seamless migration to Azure today.
        </p>
        <router-link to="/mapping" class="btn btn-cta-primary btn-lg me-md-2 mb-2 mb-md-0">Go to Mapping Tool</router-link>
        <router-link to="/about" class="btn btn-cta-secondary btn-lg">Discover More</router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home', // This is the new, redesigned Home page
};
</script>

<style scoped>
@keyframes animatedGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.modern-home.dark-theme {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #121212; /* Very dark background for the page, sections will layer on this */
  color: #e0e0e0; /* Light text */
  line-height: 1.7;
}

/* Hero Section */
.hero {
  position: relative; /* For overlay */
  color: white;
  padding: 8rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f2c3a, #2c3e50, #3498db, #2980b9); /* Restored local gradient */
  background-size: 400% 400%; 
  animation: animatedGradient 25s ease infinite; /* Restored local animation */
  overflow: hidden; 
}

.hero-overlay { 
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3); 
  z-index: 1;
}

.hero-content {
  max-width: 800px;
  position: relative; 
  z-index: 2;
}
.hero-title {
  font-size: 3.8rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  letter-spacing: -1.5px;
  color: #ffffff;
}
.hero-subtitle {
  font-size: 2.2rem;
  font-weight: 300;
  margin-bottom: 1.5rem;
  color: #ecf0f1; 
  opacity: 0.9;
}
.hero-description {
  font-size: 1.15rem;
  max-width: 650px;
  margin: 0 auto 2.5rem auto;
  color: #bdc3c7; 
  opacity: 0.9;
}
.btn-hero {
  padding: 0.9rem 2.8rem;
  font-size: 1.15rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  background-color: #00aeff; 
  color: #ffffff;
  border: 2px solid #00aeff;
  box-shadow: 0 4px 15px rgba(0, 174, 255, 0.3);
}
.btn-hero:hover {
  background-color: #0095e0;
  border-color: #0095e0;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 174, 255, 0.4);
}

/* Section Titles & Subtitles */
.section-title {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #ffffff; 
}
.section-subtitle-muted {
  color: #bdc3c7; 
}

/* Value Proposition Section */
.value-prop {
  background-color: #1e1e1e; 
}
.value-item {
  text-align: center;
  padding: 2rem 1rem; 
  border-radius: 10px;
  transition: transform 0.3s ease; 
}
.value-icon {
  font-size: 3rem; 
  margin-bottom: 1.5rem;
  color: #00aeff; 
}
.value-title {
  font-size: 1.35rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #f0f0f0; 
}
.value-text {
  font-size: 1rem;
  color: #a0a0a0; 
}

/* Process Overview Section */
.process-overview {
  background-color: #121212; 
  padding-top: 6rem; 
  padding-bottom: 6rem; 
}
.process-step {
  padding: 1.5rem; 
}
.step-icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: #00aeff; 
  color: #121212; 
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem auto;
  font-size: 1.8rem;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(0, 174, 255, 0.2);
}
.step-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #f0f0f0;
}
.step-text {
  color: #a0a0a0;
}

/* Final CTA Section */
.final-cta {
  background-color: #1e1e1e; 
}
.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
}
.btn-cta-primary {
  background-color: #00aeff;
  border-color: #00aeff;
  color: #ffffff;
  padding: 0.8rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-cta-primary:hover {
  background-color: #0095e0;
  border-color: #0095e0;
  transform: translateY(-3px);
}
.btn-cta-secondary {
  padding: 0.8rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
  color: #00aeff;
  border-color: #00aeff;
  transition: all 0.3s ease;
}
.btn-cta-secondary:hover {
  background-color: #00aeff;
  color: #1e1e1e; 
  transform: translateY(-3px);
}

/* General Responsive Adjustments */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.8rem;
  }
  .hero-subtitle {
    font-size: 1.8rem;
  }
  .section-title {
    font-size: 2.2rem;
  }
  .value-item, .process-step {
    padding: 2rem 1rem;
  }
}
</style>
