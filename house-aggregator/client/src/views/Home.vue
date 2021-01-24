<template>

<main role="main">
  <div class="home">
    <!--<img alt="Vue logo" src="../assets/house.png">-->
    <div class="jumbotron">
      <b-jumbotron header="Housing App">
      <p class="lead text-muted">
        One-stop shop for student housing in Kingston, ON. The Kayak/Expedia of houses.
      </p>
      </b-jumbotron>
    </div>
    <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <iframe width="700" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.openstreetmap.org/export/embed.html?bbox=-76.50848865509035%2C44.22078412502047%2C-76.48840427398683%2C44.23153222957561&amp;layer=mapnik" style="border: 3px solid #212529"></iframe>
    <div>
      <b-card no-body class="overflow-hidden"> 
        <template #header>
          <h4 class="mb-0">Title</h4>
        </template>
        <b-row no-gutters>
          <b-col md="3">
            <img src="../assets/house.png" alt="Image" class="rounded-0">
          </b-col>
          <b-col md="6">
            <b-card-body sub-title="Address">
              <b-card-text>
                <span><strong>Rent: </strong></span>
                <span><strong>Date Available: </strong></span>
              </b-card-text>
            </b-card-body>
          </b-col>
        </b-row>
      </b-card>
    </div>
  </div>
</main>
</template>





<!--
<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>-->




<style scoped>

.jumbotron {
  background-color: #ffffff;
  color: #212529;
  
}

.card {
  background-color: #f8f9fa;
}

span {
  display: block;
}

iframe {
  margin-top: 50px;
  margin-bottom: 75px;
}
</style>
