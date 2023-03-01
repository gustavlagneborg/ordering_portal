function toggle_display(){
    el = document.querySelector('.examination_form');
    button = document.querySelector(".toggle_visablility")
    
    if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
        el.style.display = "block"
        button.style.visibility = "hidden"
        button.style.display = "none"
    }else{
       el.style.visibility = 'hidden'
    }
  }