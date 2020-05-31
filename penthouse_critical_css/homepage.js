const penthouse = require('penthouse')
const fs = require('fs')

penthouse({
  url: 'http://localhost:8000',
  css: '/Users/Nikhil/Desktop/noobtronicsdjango/mysite/static/dist/css/app.519ad3ac.css',
  width: 1366,
  height: 768,
  renderWaitTime: 5000,
  keepLargerMediaQueries: true,
  blockJSRequests: false,
  screenshots: {
    basePath: 'homepage', // absolute or relative; excluding file extension
    type: 'jpeg', // jpeg or png, png default
    quality: 80 // only applies for jpeg type
  }
})
.then(criticalCss => {
  // use the critical css
  fs.writeFileSync('homepage.min.css', criticalCss);
})
