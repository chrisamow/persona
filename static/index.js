function deepclone(o) { //handy way to clone, naturally passes the JSON.stringify cmp
  return (JSON.parse(JSON.stringify(o)))
}

var modal = {
  props: {
    shown: { type: Boolean, required: true },
  },
  template: `
    <div id="modalid" class="c-Modal-Holder">
      <div class="c-Modal-Shade" v-if="shown" transition  @click.self="$emit('closed')">
      <div class="c-Modal-Container">
        <slot></slot>
      </div>
      </div>
    </div>
  `,
  mounted: function() {
    //document.getElementById('modalmount').appendChild(this.$el)
  },
};

var app = new Vue({ // MAIN APP -----------------------------
  el: '#app',
  components: { modal: modal },
  data: function() {
    return {
      modalTitle: '',
      modalShown: false,
      modalCounter: 0,
      modalPerson: {lastname:'',firstname:'',dateofbirth:'',zipcode:''},
      modalOrigPerson: {lastname:'',firstname:'',dateofbirth:'',zipcode:''},
      personadebug: false,
      api: '',
      zipcode: '',
      city: '',
      appstatus: 'ok',
      searchterm: '',
      thisistrue: true,
      selected: '',
      selectedStates: [],
      letters: ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
      persons: []
    }
  },
  computed: {
    isSearchEmpty: function() {
      return ! (this.searchterm.length > 0)
    },
    isSaveAllowed: function() {
      return this.isModalPersonChanged && this.isValidModalPerson
    },
    isValidModalPerson: function() {
      var p = this.modalPerson
      if((p.lastname.length<1) || (p.firstname.length<1)||(p.dateofbirth.length<10)||(p.zipcode.length<5))
        return false;
      if(! parseInt(p.zipcode)) //'33333-2222' would pass, todo: more validation would be useful
        return false;
      var ts=Date.parse(p.dateofbirth) //note years way into the future allowed (e.g +50000 years)
      if(isNaN(ts))
        return false;
      return true;  //seems ok
    },
    isModalPersonChanged: function() {
      return ! (JSON.stringify(this.modalOrigPerson) === JSON.stringify(this.modalPerson))
    },
  },
  watch: {
    zipcode: function() {
      this.city = ''
      if(this.zipcode.length == 5) {
        this.lookupzip()
      }
    }
  },
  created: function () {
    api = 'http://' + window.location.host + '/api/'
    //window.addEventListener('scroll', this.handleScroll)
    this.fetchpersons()
  },
  mounted: function() {
        setInterval(function() {
        this.modalCounter += 1;
    }.bind(this), 1000);
    //document.getElementById('modalmount').appendChild(this.$el)
  },
  destroyed: function () {
    //window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    modalSave: function() { //only Save button gets here, e.g. click on shade will not
      this.modalShown = false
      var app = this;
      if(this.modalPerson.id) { //edit existing person
        dt = new Date(this.modalPerson.dateofbirth)
        this.modalPerson.dateofbirth = dt.toISOString()
        var u = api + 'person/' + this.modalPerson.id.toString()
        app.appstatus = "REST:" + u
        axios.put(u, this.modalPerson).then(function (response) {
          //console.log(response)
          //vue model must get the changes now that we confirmed
          var p = response.data
          app.modalOrigPerson.lastname = p.lastname
          app.modalOrigPerson.firstname = p.firstname
          app.modalOrigPerson.dateofbirth = p.dateofbirth.substring(0,10)
          app.modalOrigPerson.zipcode = p.zipcode
        })
        .catch(function (error) {
          a.searchterm = "Invalid Data"
        })
      } else { //new person
        dt = new Date(this.modalPerson.dateofbirth)
        this.modalPerson.dateofbirth = dt.toISOString()
        var u = api + 'persons'
        app.appstatus = "REST:" + u
        axios.post(u, this.modalPerson).then(function (response) {
          //console.log(response)
          //vue model must get the changes now that we confirmed
          var p = response.data
          p.dateofbirth = p.dateofbirth.substring(0,10)
          app.persons.unshift(p)
        })
        .catch(function (error) {
          app.searchterm = "Invalid Data"
        })
      }
    },
    modalChild: function() {
      this.modalCounter = 0;
      //document.getElementById('modalmount').appendChild(document.getElementById('modalid'))
      this.modalShown = true
    },
    jumpto: function() {
      window.alert("jumping to " + this.selected)
    },
    search: function() {
      if (! this.isSearchEmpty) {
        //window.alert("searching for: " + this.searchterm)
        var a = this; //app
        u = api + 'persons'
        a.appstatus = "REST:" + u
        axios.get(u, { params: { search: this.searchterm }})
          .then(function (response) {
            console.log(response)
            a.persons = response.data
            if (a.persons.length > 0) {
            }
            for (var p of a.persons) {
              p.dateofbirth = p.dateofbirth.substring(0,10)
              console.log(p)
            }
            //response.data.error  //error code here tbd
          })
          .catch(function (error) {
            a.searchterm = "Invalid Data"
          })
      }
    },
    editrow: function(person) {
      //window.alert("edit row " + this.personRepr(person))
      //was going to pass in $event, but easier and better to just pass in a person object
      this.modalPerson = deepclone(person) //dont mod the original before its time
      this.modalOrigPerson = person
      this.modalTitle = 'Editing person #' + person.id
      this.modalChild()
    },
    newrow: function() {
      this.modalOrigPerson = { id:'', lastname:'', firstname:'', dateofbirth:'', zipcode:'' }
      this.modalPerson = deepclone(this.modalOrigPerson) //dont mod the original before its time
      this.modalTitle = 'New person'
      this.modalChild()
    },
    selectrow: function(e) {
      //window.alert("selected: " + e.currentTarget.id)
      this.selected =  e.currentTarget.id
      var id = parseInt(e.currentTarget.id)
      this.selectedStates[id] = ! (this.selectedStates[id]);
    },
    deleterow: function() {
      var app = this;
      for(s in this.selectedStates) {
        if(this.selectedStates[s]) {
          var u = api + 'person/' + s
          app.appstatus = "REST:" + u
          axios.delete(u).then(function (response) {
            //console.log(response)
            var personid = response.data
            var prevLen = app.persons.length
            app.persons = app.persons.filter(function(p){return !(p.id == personid) })
            if((app.persons.length+1) != prevLen)
              window.alert("delete problem " + personid)
          })
          .catch(function (error) {
            a.searchterm = "Invalid Data"
          })
        }//if
      }
    },
    refresh: function(e) {
      //manual refresh
      this.selectedStates = []
      this.searchterm = ''
      this.fetchpersons()
    },
    handleScroll: function () {
      this.scrollPos = document.body.scrollHeight - window.innerHeight - document.body.scrollTop;   
      if (document.body.scrollHeight - window.innerHeight - document.body.scrollTop == 0) {
        // load more data here...
      }
    },
    personRepr: function(person) {
      return 'person: ' + person.id.toString()+' '+person.lastname.toString()
    },
    fetchpersons: function() {
      var a = this; //app
      var u = api + 'persons'
      a.appstatus = "REST:" + u
      axios.get(u).then(function (response) {
        console.log(response)
        a.persons = response.data
        if (a.persons.length > 0) {
        }
        for (var p of a.persons) {
          p.dateofbirth = p.dateofbirth.substring(0,10)
          console.log(p)
        }
        //response.data.error  //error code here tbd
      })
      .catch(function (error) {
        a.searchterm = "Invalid Data"
      })
    }, 
  }//methods
})

