const penthouse = require('penthouse')
const fs = require('fs')

penthouse({
  url: 'http://localhost:8000/arduino-microcontrollers/arduino-uno',
  css: '/Users/Nikhil/Desktop/noobtronicsdjango/mysite/static/css/bulma/header2.min.css',
  width: 414,
  height: 736,
  screenshots: {
    basePath: 'products', // absolute or relative; excluding file extension
    type: 'jpeg', // jpeg or png, png default
    quality: 80 // only applies for jpeg type
  }
})
.then(criticalCss => {
  // use the critical css
  fs.writeFileSync('product.min.css', criticalCss);
})
