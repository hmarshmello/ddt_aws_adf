<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">AWS to Azure Migration Mapping Tool</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/mapping">Mapping Tool</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about">About</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="main-content-area mt-4"> <!-- Removed .container class -->
      <router-view/>
    </div>

    <footer class="app-footer text-center mt-5"> <!-- Changed classes for dark theme -->
      <div class="container">
        <p class="p-3 mb-0">&copy; {{ new Date().getFullYear() }} AWS to Azure Migration Mapping Tool</p>
      </div>
    </footer>
  </div>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #121212; /* Ensure body background is dark */
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* Consistent font with Home.vue */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #e0e0e0; /* Default light text color for dark theme */
  background-color: #121212; /* Dark background for the entire app */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content-area { /* Styles now apply directly to this class */
  flex: 1;
  width: 100%; /* Ensure it takes full width if not by default */
  /* background-color: transparent; /* Or specific dark color if needed, but usually inherits from #app */
}

.app-footer {
  margin-top: auto;
  background-color: #1e1e1e; /* Dark footer background */
  color: #a0a0a0; /* Muted light text for footer */
  border-top: 1px solid #333; /* Subtle top border */
}

.app-footer p {
  color: #a0a0a0; /* Ensure text color is applied */
}

/* Ensure router links in navbar are visible on dark bg (Bootstrap usually handles this with navbar-dark) */
.navbar-dark .navbar-nav .nav-link {
  color: rgba(255, 255, 255, 0.75); /* Lighter than default for better visibility */
}
.navbar-dark .navbar-nav .nav-link:hover,
.navbar-dark .navbar-nav .nav-link:focus {
  color: #ffffff;
}
.navbar-dark .navbar-brand {
  color: #ffffff;
}
</style>
