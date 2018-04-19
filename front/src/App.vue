<template>
  <div id="app">
    <router-view/>
    <vue-particles 
      color="#dedede"
       :particleOpacity="0.7"
       :particlesNumber="80"
       shapeType="circle"
       :particleSize="4"
       linesColor="#dedede"
       :linesWidth="1"
       :lineLinked="true"
       :lineOpacity="0.4"
       :linesDistance="150"
       :moveSpeed="3"
       :hoverEffect="true"
       hoverMode="grab"
       :clickEffect="true"
       clickMode="push"
     >
     </vue-particles>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
