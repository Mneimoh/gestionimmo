

// PAGINATOR CODE BELLOW

function paginate_table(page,$event) {
    document.getElementById('templatemo_search_box').value = '';
  if(page > 1) {
    document.getElementById('prev').classList = '';
  }

  if(page == 1) {
    document.getElementById('prev').classList = 'disabled'
  }



  //  Write Logic to change current active button
  
    all_childrens = event.target.parentElement.parentElement.children
    for(let i = 0; i < all_childrens.length; i++){
        if(all_childrens[i].classList.contains('active')){
          all_childrens[i].classList = '';
        }
    }
   
    event.target.parentElement.classList = 'active'

    // Total Pages Calculation Bellow
    let total = all_childrens.length - 2;

    if(page == total) {
      document.getElementById('next').classList = 'disabled'
    }

    if(page < total) {
      document.getElementById('next').classList = ''
    }

    let param = `page=${page}`
    send_paginate_request(param)
}

function next($event) {
  let all_childrens = event.target.parentElement.parentElement.children
  let setactive = 0;
  prevactive = 0;

  for(let i = 0; i < all_childrens.length; i++){
        if(all_childrens[i].classList.contains('active')){
          prevactive = i;
          all_childrens[i].classList = '';
          setactive = i+1;
        }
    }

    
  let total = all_childrens.length - 2;
  
  if(setactive > total) {
    console.log('SET ACTIVE IS GREATER THAN TOTAL')
    all_childrens[prevactive].classList = 'active';

  }else {

    if(setactive > 1) {
      document.getElementById('prev').classList = '';
    }


    if(setactive == total) {
      document.getElementById('next').classList = 'disabled'
    }


    all_childrens[setactive].classList = 'active';
    let param = `page=${setactive}`
    send_paginate_request(param)
  }

}


function prev($event) {
  let all_childrens = event.target.parentElement.parentElement.children
  let setactive = 0;
  let prevactive = 0;

  for(let i = 0; i < all_childrens.length; i++){
        if(all_childrens[i].classList.contains('active')){
          prevactive = i;
          all_childrens[i].classList = '';
          setactive = i-1;
        }
    }

    
  let total = all_childrens.length - 2;
  
  if(setactive < 1) {
    console.log('SET ACTIVE IS LESSER THAN ONE')
    all_childrens[prevactive].classList = 'active';

  }else {

    if(setactive < total) {
      document.getElementById('next').classList = '';
    }

    if(setactive == 1) {
      document.getElementById('prev').classList = 'disabled'
    }


    all_childrens[setactive].classList = 'active';
    let param = `page=${setactive}`
    send_paginate_request(param)
  }

}


function send_paginate_request(param) {
    $.ajax({
        method: 'GET',
        url: 'accueuil/api/paginate_appointments?' + param,
        beforeSend: function() {
            console.log('Before Send')
        },

        success: function(result) {
          console.log('after send')
            update_table_paginate(result);
            
        },

        error: function() {
            console.log('error')
        }
    })
}

function update_table_paginate(data) {
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = `<tr><td> ${elem['nom']} </td> <td>${elem['prenom']}</td> <td>${elem['num_client']}</td> <td>${elem['telephone']}</td> <td>${elem['date_dappel']}</td> <td>${elem['heure_dappel']}</td> <td>${elem['article_dinteret']}</td> <td>${elem['how_connu']}</td> <td>${elem['date_redezvous']}</td> <td>${elem['heure_redezvous']}</td> </tr>`
        all_rows = all_rows + row;
    });

    $("#appointmentTable tbody").html(all_rows)
}

// END OF PAGINATOR


function sort_appointments(sort_type) {
    document.getElementById('templatemo_search_box').value = '';
    let param = `${sort_type}=${sort_type}`
    send_request(param);
}

function find_appointment() {
    let nom = document.getElementById('templatemo_search_box').value;
    let param = `search_nom=${nom}`
    send_request(param);
}

function appointment_tocome() {
    document.getElementById('templatemo_search_box').value = '';
    let param = `date_tocome=True`
    send_request(param);
}

function appointment_pass() {
    document.getElementById('templatemo_search_box').value = '';
    let param = `date_pass=True`
    send_request(param)
}

function send_request(param) {
    $.ajax({
        method: 'GET',
        url: 'accueuil/api/get_appointments?' + param,
        beforeSend: function() {
            console.log('Before Send')
        },

        success: function(result) {
            update_table(result);
            console.log('after send')
        },

        error: function() {
            console.log('error')
        }
    })
}

function update_table(data) {
    console.log('Table Update')
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = `<tr><td> ${elem['nom']} </td> <td>${elem['prenom']}</td> <td>${elem['num_client']}</td> <td>${elem['telephone']}</td> <td>${elem['date_dappel']}</td> <td>${elem['heure_dappel']}</td> <td>${elem['article_dinteret']}</td> <td>${elem['how_connu']}</td> <td>${elem['date_redezvous']}</td> <td>${elem['heure_redezvous']}</td> </tr>`
        all_rows = all_rows + row;
    });

    $("#appointmentTable tbody").html(all_rows)
}
   