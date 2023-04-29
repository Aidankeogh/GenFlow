<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink class="app-link" :class="{active: $route.path=='/'}"  :to="{name: 'home'}">  
          Home        
        </RouterLink>
        <RouterLink class="app-link" :class="{active: $route.path.includes('/pca')}" :to="{name: 'pca'}">
          PCA
        </RouterLink>
        <RouterLink class="app-link" :class="{active: $route.path.includes('/regression')}" :to="{name: 'regression'}">
          Regression
        </RouterLink>
        <RouterLink class="app-link" :class="{active: $route.path.includes('/classifier')}" :to="{name: 'classifier'}">
          Classifier
        </RouterLink>
        
      </nav>
    </div>
  </header>
  <div>
    <RouterView />
  </div>
  
</template>

<script>
  import { RouterLink, RouterView } from 'vue-router';
  

  export default {
    name: 'App',
    created(){
      this.axios.defaults.baseURL = 'http://localhost:5001';
      window.GOOGLE_API_KEY = 'AIzaSyDJW4jsPlNKgv6jFm3B5Edp5ywgdqLWdmc';
    }
  }
</script>


<style lang="scss">

  .wrapper {
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  .app-link {
    color: $secondary;
    border: 2px solid $light_border_color;
    padding: 0.5rem 1rem;
    margin-left: 0.5rem;
    cursor: pointer;
    text-decoration: none;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
  }

  .app-link:focus, .app-link:hover, .app-link.active{
      color: $primary;
      border-color: rgba($primary, .4)
  }

</style>
