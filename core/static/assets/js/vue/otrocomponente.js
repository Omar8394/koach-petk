// my-component.js
const otro= {
  delimiters: ['[[', ']]'],
    data() {
      return { count: 10 }
    },methods:{
      gethola(){
        fetch("/security/testdata")
  .then(function(response) {
    return response.json()
  })
  .then(function(data) {
    // Example:
    // where 'title' is a key
    console.log(data.hola)
  })
      }
    },
    template: `<div @click="gethola()" class="alert alert-danger" role="alert">
        <strong>[[count]]</strong>
    </div>`
  }

 const combo={
  delimiters: ['[[', ']]'],
    props:['nombre','data', 'selected'],
    data(){
      return {seleccionado:-1}
    },methods:{
      onChange(event) {
        this.seleccionado=event.target.value
        console.log(this.seleccionado)
        this.$emit("ComboSeleccionado",this.seleccionado)
    },
      parseObjectToArray:function(item,index){
          return Object.values(item)[index]
      },
      

    },created:function (params) {
      this.seleccionado = this.selected
    }, template :`<div class="form-group">
      <label for="">[[nombre]]</label>
      <select class="form-control" name="" id="" v-model="seleccionado" @change="onChange($event)">
      <option :value="'-1'" >Seleccione un elemento</option>
      <template v-for="item in data">
      <option :value="parseObjectToArray(item,0)">[[parseObjectToArray(item,1)]]</option>
      </template >
      </select>
    </div>`
   
  }
  export {otro,combo}