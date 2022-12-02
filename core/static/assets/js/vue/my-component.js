// my-component.js
import {otro,combo} from '/static/assets/js/vue/otrocomponente.js'
export default {
  components: {
    otro,combo
  },
  delimiters: ['[[', ']]'],
  data() {
    return {count:0,ruta:"defecto", 
    data:[{id:0,nombre:'freddy'},
    {id:1,nombre:'ramon'},
    {id:2,nombre:'carlos'}], 
    selected:2}
  }, methods:{
    getcombo: function(data){
      this.selected=data
      console.log("from children"+data)
    }
  },
  template: `<div class="alert alert-primary" role="alert" >
    <strong>[[selected]]</strong>
  </div>
  <combo nombre="combo" v-bind:data="data" v-bind:selected="selected" v-on:ComboSeleccionado="getcombo"></combo>
  
  `
}

