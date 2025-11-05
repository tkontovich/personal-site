document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#contact-form').addEventListener('submit', contact);

  });

function contact() {
  const email = document.querySelector('#email').value;
  const name = document.querySelector('#name').value;
  const message = document.querySelector('#message').value;

  fetch('/contact/', {
    headers: {
      'Content-Type': 'application/json'
    }, 
    method: 'POST', 
    body: JSON.stringify({
      email: email, 
      name: name, 
      message: message
    })
  })
  .then(response => {
    response.json();
  })
  .then(result => {
    console.log(result);
    alert('Thanks for reaching out. I will be in touch soon!');
    document.querySelector('#email').value = '';
    document.querySelector('#name').value = '';
    document.querySelector('#message').value = '';
  })
}