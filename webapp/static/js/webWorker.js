onmessage = function(e) {
    console.log('Message received from main script');
    console.log(e.data*10);
    postMessage(e.data*10);
  }