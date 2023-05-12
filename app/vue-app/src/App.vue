<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink class="app-link" :class="{active: $route.path=='/'}"  :to="{name: 'home'}">  
          <font-awesome-icon :icon="['fas', 'house']"/> Home 
        </RouterLink>
        <RouterLink class="app-link" :class="{active: $route.path.includes('/create')}" :to="{name: 'create'}">
          <font-awesome-icon :icon="['fas', 'pen-to-square']" /> Create
        </RouterLink>
        <RouterLink class="app-link" :class="{active: $route.path.includes('/dashboards')}" :to="{name: 'dashboards'}">
          <font-awesome-icon :icon="['fas', 'chalkboard']"/> Dashboards
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
