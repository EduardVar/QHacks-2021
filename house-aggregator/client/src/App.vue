<template>
  <div id="app">
    <div id="nav">
      <b-navbar>
        <b-navbar-brand href="#">
          <img src="./assets/house.png" alt="icon" width="60px" class="d-inline-block">
          <!--<router-link to="/"> -->
          Student Housing
          <!--</router-link> -->
        </b-navbar-brand>
      </b-navbar>
    </div>
    <router-view/>
  </div>
</template>

<style>

* {
  margin: 0px;
  border: 0px;
}

*, *::before, *::after {

  box-sizing: border-box;
}

img {
    margin-right: 15px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #182430;
  background-color: #f8f9fa;
}

#nav {
  padding: 15px;
  background-color: #054050;
  color: white;
  margin-right: auto;
  margin-left: auto;
  width: auto;
  flex-wrap: nowrap;
}

#nav a {
  font-weight: bold;
  color: #adc8e6;
  text-decoration: none;
}

#nav a.router-link-exact-active {
  color: #42b983;
  text-decoration: none;
}
</style>
